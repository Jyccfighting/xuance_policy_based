"""
analyzer.py

主流程：扫描实验 -> 加载过程历史 -> 计算指标 -> 返回 Experiment 列表。
"""

from __future__ import annotations

import logging

from drl_analyzer.config import AnalyzerConfig
from drl_analyzer.exporter import BenchmarkExporter
from drl_analyzer.history_loader import HistoryLoader
from drl_analyzer.metrics import MetricsCalculator
from drl_analyzer.scanner import Scanner

logger = logging.getLogger(__name__)


class Analyzer:
    """DRL 实验分析器。"""

    def __init__(self, config: AnalyzerConfig | None = None):
        """
        参数
        ----
        config : AnalyzerConfig | None
            不传则使用默认配置（logs -> results，WandB 开启）。
        """
        self.config = config or AnalyzerConfig()
        self.scanner = Scanner(self.config.log_root)
        self.history_loader = HistoryLoader(
            wandb_config=self.config.wandb,
            cache_dir=self.config.resolved_cache_dir(),
        )
        self.metrics_calculator = MetricsCalculator()

    def analyze(self):
        """
        执行完整分析。

        返回
        ----
        List[Experiment]
            已填充 history 与 metrics 的实验列表。
        """
        logger.info("扫描实验目录: %s", self.config.log_root)
        experiments = self.scanner.scan()
        logger.info("找到 %d 个实验", len(experiments))

        ok = 0
        for i, experiment in enumerate(experiments, 1):
            logger.info("[%d/%d] %s", i, len(experiments), experiment)
            try:
                # 先加载历史，None/空直接跳过，再计算指标
                history = self.history_loader.load(experiment)
                if history is None or history.empty:
                    logger.warning("无过程历史，跳过: %s", experiment.run_name)
                    continue
                experiment.history = history
                experiment.metrics = self.metrics_calculator.calculate(history)
                ok += 1
            except Exception as exc:
                logger.warning("分析失败 %s: %s", experiment.run_name, exc)
                continue

        logger.info("分析完成，成功 %d/%d", ok, len(experiments))
        return experiments

    def export(self, experiments):
        """
        导出 benchmark.csv / Excel。

        返回
        ----
        List[Path]
        """
        exporter = BenchmarkExporter(self.config.output_dir)
        paths = []
        if self.config.save_csv:
            paths.append(exporter.export_csv(experiments))
        if self.config.save_excel:
            paths.append(exporter.export_excel(experiments))
        return paths