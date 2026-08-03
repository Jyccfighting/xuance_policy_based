"""
scanner.py

扫描 DRL 实验目录，识别 WandB run 并构造 Experiment 对象。

支持目录结构：
logs/
    algorithm/
        environment/
            wandb/
                run-xxx/
                    files/config.yaml
                    run-xxx.wandb
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from drl_analyzer.config import ExperimentConfig
from drl_analyzer.config_cleaner import ConfigCleaner
from drl_analyzer.models import Experiment
from drl_analyzer.utils import find_file, load_json, load_yaml

logger = logging.getLogger(__name__)


class Scanner:
    """扫描实验日志根目录，把每个 run 目录变成 Experiment 对象。"""

    def __init__(self, root_dir: Path):
        """root_dir 为日志根目录（如 logs/）。"""
        self.root_dir = Path(root_dir)

    # ---------------- 公共接口 ----------------

    def scan(self) -> List[Experiment]:
        """扫描全部实验，单个 run 失败不影响整批。"""
        experiments = []
        if not self.root_dir.exists():
            logger.warning("日志根目录不存在: %s", self.root_dir)
            return experiments

        for run_dir in self._find_run_dirs():
            try:
                experiment = self._parse_run(run_dir)
                if experiment is not None:
                    experiments.append(experiment)
            except Exception as exc:
                logger.warning("解析 run 失败 %s: %s", run_dir, exc)

        logger.info("扫描到 %d 个实验", len(experiments))
        return experiments

    # ---------------- 查找 run ----------------

    def _find_run_dirs(self):
        """
        查找所有 wandb run 目录。

        只遍历名为 wandb 的目录（比 rglob 全树快），
        兼容 algorithm/env/wandb/run-* 和任意深度嵌套。
        """
        for wandb_dir in self.root_dir.rglob("wandb"):
            if not wandb_dir.is_dir():
                continue
            for run_dir in sorted(wandb_dir.glob("run-*")):
                if run_dir.is_dir():
                    yield run_dir

    # ---------------- 解析单个 run ----------------

    def _parse_run(self, run_dir: Path) -> Experiment | None:
        """解析一个 run 目录：读取配置、填充数据源路径、构造 Experiment。"""
        # 路径推断的算法/环境（config 优先）
        algorithm, environment = self._infer_from_path(run_dir)

        # 读取配置（yaml 优先，summary 兜底）
        config = self._load_config(run_dir)
        exp_config = ExperimentConfig.from_dict(config) if config else ExperimentConfig()
        algorithm = exp_config.algorithm or algorithm
        environment = exp_config.environment or environment

        # 清洗后的参数
        clean_config = ConfigCleaner.clean(exp_config.parameters)

        # 本地数据源
        files_dir = run_dir / "files"
        history_csv = files_dir / "history.csv"
        wandb_files = list(run_dir.glob("*.wandb"))
        summary_path = find_file(run_dir, "wandb-summary.json")

        experiment = Experiment(
            algorithm=algorithm,
            environment=environment,
            seed=exp_config.seed,
            path=run_dir,
            run_name=run_dir.name,
            project_name=clean_config.get("project_name") or clean_config.get("wandb_project"),
            config_path=find_file(run_dir, "config.yaml") or find_file(run_dir, "config.yml"),
            summary_path=summary_path,
            history_csv_path=history_csv if history_csv.exists() else None,
            wandb_file=wandb_files[0] if wandb_files else None,
            config=clean_config,
        )

        # 加载 summary（供指标回退 / 调试）
        if summary_path is not None:
            try:
                experiment.summary = load_json(summary_path)
            except Exception as exc:
                logger.warning("读取 summary 失败 %s: %s", summary_path, exc)

        return experiment

    @staticmethod
    def _infer_from_path(run_dir: Path):
        """从路径 logs/<algorithm>/<environment>/wandb/run-* 推断元信息。"""
        parts = run_dir.parts
        try:
            index = parts.index("logs")
            return parts[index + 1], parts[index + 2]
        except (ValueError, IndexError):
            return None, None

    @staticmethod
    def _load_config(run_dir: Path):
        """
        读取配置，优先级：
        1. config.yaml / config.yml
        2. wandb-summary.json
        """
        for name in ("config.yaml", "config.yml"):
            file = find_file(run_dir, name)
            if file:
                try:
                    return load_yaml(file)
                except Exception as exc:
                    logger.warning("读取配置失败 %s: %s", file, exc)

        summary = find_file(run_dir, "wandb-summary.json")
        if summary:
            try:
                return load_json(summary)
            except Exception as exc:
                logger.warning("读取 summary 配置失败 %s: %s", summary, exc)

        return {}