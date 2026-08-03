"""
exporter.py

把 Experiment 列表导出为 benchmark.csv 或 Excel。
无有效指标的实验会用 status 列标记，而不是静默丢弃。
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from drl_analyzer.utils import ensure_dir

logger = logging.getLogger(__name__)

# benchmark.csv 的固定列顺序，保证空数据时也有表头
CSV_COLUMNS = [
    "algorithm", "environment", "seed", "run_name", "status",
    "final_reward", "best_reward", "mean_reward", "std_reward",
    "runtime", "episodes", "stability", "sample_efficiency",
]


class BenchmarkExporter:
    """导出实验基准结果。"""

    def __init__(self, output_dir: Path = Path("results")):
        """output_dir 为输出目录，不存在时自动创建。"""
        self.output_dir = Path(output_dir)
        ensure_dir(self.output_dir)

    def export_csv(self, experiments) -> Path:
        """
        导出 benchmark.csv。

        参数
        ----
        experiments : List[Experiment]

        返回
        ----
        Path
        """
        rows = []
        for exp in experiments:
            row = {
                "algorithm": exp.algorithm,
                "environment": exp.environment,
                "seed": exp.seed,
                "run_name": exp.run_name,
                "status": "ok",
            }
            if exp.metrics is not None:
                row.update({
                    "final_reward": exp.metrics.final_reward,
                    "best_reward": exp.metrics.best_reward,
                    "mean_reward": exp.metrics.mean_reward,
                    "std_reward": exp.metrics.std_reward,
                    "runtime": exp.metrics.runtime,
                    "episodes": exp.metrics.episodes,
                    "stability": exp.metrics.stability_score,
                    "sample_efficiency": exp.metrics.sample_efficiency,
                })
                # 没有历史数据时 metrics 全是默认值，标记为 no_history
                if exp.metrics.episodes == 0:
                    row["status"] = "no_history"
            else:
                row["status"] = "no_metrics"
            rows.append(row)

        df = pd.DataFrame(rows, columns=CSV_COLUMNS)
        path = self.output_dir / "benchmark.csv"
        df.to_csv(path, index=False)
        logger.info("已导出 %s（%d 行）", path, len(df))
        return path

    def export_excel(self, experiments) -> Path:
        """
        导出 Excel：一个汇总 sheet + 每个环境一个 sheet。

        参数
        ----
        experiments : List[Experiment]

        返回
        ----
        Path
        """
        records = []
        for exp in experiments:
            if exp.metrics is None:
                continue
            record = {
                "algorithm": exp.algorithm,
                "environment": exp.environment,
                "seed": exp.seed,
                "run_name": exp.run_name,
            }
            record.update(exp.metrics.to_dict())
            records.append(record)

        df = pd.DataFrame(records)
        path = self.output_dir / "report.xlsx"
        with pd.ExcelWriter(path) as writer:
            # 空数据时仍写出一个空汇总 sheet
            if df.empty:
                pd.DataFrame(columns=["algorithm", "environment", "seed", "run_name"]).to_excel(
                    writer, sheet_name="benchmark", index=False
                )
            else:
                df.to_excel(writer, sheet_name="benchmark", index=False)
                if "environment" in df.columns:
                    for env in df.environment.dropna().unique():
                        env_df = df[df.environment == env]
                        env_df.to_excel(writer, sheet_name=str(env)[:30], index=False)

        logger.info("已导出 %s", path)
        return path