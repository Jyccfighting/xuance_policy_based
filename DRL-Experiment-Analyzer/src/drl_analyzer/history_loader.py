"""
history_loader.py

加载训练过程历史。加载优先级：
1. files/history.csv（缓存或训练端导出）
2. 本地 run-*.wandb（WandB 二进制过程文件，best-effort）
3. WandB API（带超时/重试，成功后写入缓存）
"""

from __future__ import annotations

import concurrent.futures
import json
import logging
import time
from pathlib import Path

import pandas as pd

from drl_analyzer.config import WandBConfig
from drl_analyzer.utils import ensure_dir

logger = logging.getLogger(__name__)


class HistoryLoader:
    """按优先级加载一个实验的逐 step 历史。"""

    def __init__(
        self,
        wandb_config: WandBConfig | None = None,
        cache_dir: Path | None = None,
    ):
        """
        参数
        ----
        wandb_config : WandBConfig | None
            在线获取配置；不传则使用默认（开启、30s 超时）。
        cache_dir : Path | None
            历史缓存目录；不传则写入 run 目录 files/history.csv。
        """
        self.wandb_config = wandb_config or WandBConfig()
        self.cache_dir = Path(cache_dir) if cache_dir else None

    # ---------------- 主入口 ----------------

    def load(self, experiment) -> pd.DataFrame | None:
        """
        加载训练历史。

        参数
        ----
        experiment : Experiment

        返回
        ----
        pd.DataFrame | None
        """
        # 1. 本地 history.csv（最快）
        history = self._load_csv(experiment)
        if history is not None:
            logger.info("使用本地 history.csv: %s", experiment.run_name)
            return history

        # 2. 本地 run-*.wandb（无需网络）
        history = self._load_local_wandb(experiment)
        if history is not None:
            logger.info("解析本地 .wandb: %s", experiment.run_name)
            return history

        # 3. WandB API（带超时与缓存）
        if not self.wandb_config.enabled:
            logger.info("未启用 WandB API，跳过在线获取: %s", experiment.run_name)
            return None
        return self._load_from_wandb(experiment)

    # ---------------- 本地 CSV ----------------

    @staticmethod
    def _load_csv(experiment) -> pd.DataFrame | None:
        """读取 files/history.csv；缺失或为空返回 None。"""
        path = experiment.history_csv_path
        if path is None or not Path(path).exists():
            return None
        try:
            df = pd.read_csv(path)
            return df if not df.empty else None
        except Exception as exc:
            logger.warning("读取 history.csv 失败 %s: %s", path, exc)
            return None

    # ---------------- 本地 .wandb ----------------

    def _load_local_wandb(self, experiment) -> pd.DataFrame | None:
        """
        用 wandb 内部 DataStore 解析本地 run-*.wandb。

        该 API 随 wandb 版本变化，失败时自动降级（返回 None）。
        """
        wandb_file = experiment.wandb_file
        if wandb_file is None or not Path(wandb_file).exists():
            return None

        try:
            from wandb.proto import wandb_internal_pb2
            from wandb.sdk.internal.datastore import DataStore

            ds = DataStore()
            ds.open_for_scan(str(wandb_file))
            rows = {}
            try:
                while True:
                    data = ds.scan_data()
                    if data is None:
                        break
                    record = wandb_internal_pb2.Record()
                    record.ParseFromString(data)
                    if record.WhichOneof("record_type") != "history":
                        continue
                    row = self._history_record_to_row(record.history)
                    if row:
                        # 优先用 _step，缺失时退回 step
                        key = row.get("_step", row.get("step", len(rows)))
                        rows[key] = row
            finally:
                ds.close()

            if not rows:
                return None
            df = pd.DataFrame.from_dict(rows, orient="index")
            # 按 step 排序并重建索引
            return df.sort_index().reset_index(drop=True)
        except Exception as exc:
            logger.warning("解析本地 .wandb 失败 %s: %s", wandb_file, exc)
            return None

    @staticmethod
    def _history_record_to_row(history_record) -> dict:
        """把一个 HistoryRecord 转成 dict（兼容不同 wandb 版本）。"""
        row = {}
        # step 字段在不同版本可能是 int 或 HistoryStep(num=...)
        step = history_record.step
        if hasattr(step, "num"):
            row["step"] = step.num
        elif isinstance(step, int):
            row["step"] = step

        for item in history_record.item:
            key = item.key or ".".join(item.nested_key)
            value = item.value_json
            try:
                row[key] = json.loads(value) if value else None
            except Exception:
                row[key] = value
        return row

    # ---------------- WandB API ----------------

    def _load_from_wandb(self, experiment) -> pd.DataFrame | None:
        """在线获取完整历史，成功后写本地缓存。"""
        if experiment.path is None:
            return None

        run_id = experiment.path.name.split("-")[-1]
        entity = self.wandb_config.entity or experiment.config.get("wandb_user_name")
        project = (
            self.wandb_config.project
            or experiment.project_name
            or experiment.config.get("project_name")
        )
        if not entity or not project:
            logger.warning("缺少 WandB entity/project，无法在线获取: %s", experiment.run_name)
            return None

        path = f"{entity}/{project}/{run_id}"
        for attempt in range(self.wandb_config.retries + 1):
            try:
                history = self._api_history(path)
                if history is None or history.empty:
                    logger.warning("WandB 返回空历史: %s", path)
                    return None
                self._save_cache(experiment, history)
                return history
            except Exception as exc:
                logger.warning(
                    "WandB 获取失败(%d/%d) %s: %s",
                    attempt + 1,
                    self.wandb_config.retries + 1,
                    path,
                    exc,
                )
                if attempt < self.wandb_config.retries:
                    time.sleep(1.0 * (attempt + 1))
        return None

    def _api_history(self, path: str) -> pd.DataFrame | None:
        """带超时地调用 WandB API，避免离线时无限挂起。"""
        def fetch():
            import wandb
            api = wandb.Api()
            run = api.run(path)
            return run.history(pandas=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(fetch)
            return future.result(timeout=self.wandb_config.timeout)

    def _save_cache(self, experiment, history: pd.DataFrame) -> None:
        """把在线获取的历史写入本地缓存（history.csv）。"""
        if not self.wandb_config.cache_history:
            return
        try:
            if self.cache_dir is not None:
                target = self.cache_dir / experiment.run_name / "history.csv"
            else:
                target = Path(experiment.path) / "files" / "history.csv"
            ensure_dir(target.parent)
            history.to_csv(target, index=False)
            logger.info("已缓存历史: %s", target)
            experiment.history_csv_path = target
        except Exception as exc:
            logger.warning("缓存 history 失败: %s", exc)