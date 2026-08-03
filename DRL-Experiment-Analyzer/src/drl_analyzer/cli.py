"""
cli.py

命令行入口：
    drl-analyzer --log-root logs --output results [--no-wandb]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from drl_analyzer.analyzer import Analyzer
from drl_analyzer.config import AnalyzerConfig, WandBConfig
from drl_analyzer.logger import get_logger
from drl_analyzer.process_analyzer import analyze_process, build_process_report
from drl_analyzer.report import ReportGenerator
from drl_analyzer.summary import SummaryGenerator
from drl_analyzer.utils import load_yaml
from drl_analyzer.visualization.summary_plot import SummaryPlotter


def parse_args(argv=None):
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="DRL Experiment Analyzer")
    parser.add_argument("--log-root", default="logs", help="实验日志根目录")
    parser.add_argument("--output", default="results", help="输出目录")
    parser.add_argument("--config", default=None, help="YAML 配置文件")
    parser.add_argument("--no-wandb", action="store_true", help="禁用 WandB 在线获取")
    parser.add_argument("--no-plots", action="store_true", help="不生成图表")
    parser.add_argument("--process-report", default=None, help="过程分析 Markdown 输出路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出 DEBUG 日志")
    return parser.parse_args(argv)


def build_config(args) -> AnalyzerConfig:
    """根据命令行参数和可选 YAML 构建配置，命令行参数优先。"""
    config = AnalyzerConfig()
    if args.config:
        data = load_yaml(Path(args.config))
        if "log_root" in data:
            config.log_root = Path(data["log_root"])
        if "output_dir" in data:
            config.output_dir = Path(data["output_dir"])
        wandb_data = data.get("wandb", {}) or {}
        config.wandb = WandBConfig(
            enabled=bool(wandb_data.get("enabled", True)),
            entity=wandb_data.get("entity"),
            project=wandb_data.get("project"),
            timeout=float(wandb_data.get("timeout", 30.0)),
            retries=int(wandb_data.get("retries", 2)),
            cache_history=bool(wandb_data.get("cache_history", True)),
        )

    # 命令行参数优先
    config.log_root = Path(args.log_root)
    config.output_dir = Path(args.output)
    if args.no_wandb:
        config.wandb.enabled = False
    return config


def main(argv=None) -> int:
    """CLI 主函数：分析 + 导出 + 报告 + 图表 + 可选过程分析。"""
    args = parse_args(argv)
    get_logger("DRLAnalyzer", level=logging.DEBUG if args.verbose else logging.INFO)
    config = build_config(args)

    analyzer = Analyzer(config)
    experiments = analyzer.analyze()
    analyzer.export(experiments)

    # Markdown 摘要与 HTML 报告
    benchmark_csv = config.output_dir / "benchmark.csv"
    SummaryGenerator().generate(benchmark_csv, config.output_dir / "summary.md")
    ReportGenerator().generate(
        benchmark_csv,
        figure_dir=config.output_dir / "figures",
        output=config.output_dir / "report.html",
    )

    # 图表
    if config.save_figures and not args.no_plots:
        plotter = SummaryPlotter(config.output_dir / "figures")
        plotter.plot_all(benchmark_csv)

    # 过程分析报告
    if args.process_report:
        sections = []
        for exp in experiments:
            if exp.history is None or exp.history.empty:
                continue
            analysis = analyze_process(exp.history)
            sections.append(build_process_report(exp, analysis))
        output_path = Path(args.process_report)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n\n".join(sections), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())