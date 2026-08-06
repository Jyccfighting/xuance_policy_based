"""
run.py

一键运行入口 —— 在 VS Code 中直接点击右上角 ▶ 即可运行全部功能。

调用大纲（对应下方 run_all 中的每一行）：
    1. step_analyze()    扫描实验并计算指标
    2. step_export()     导出 benchmark.csv / report.xlsx
    3. step_summary()    生成 summary.md
    4. step_report()     生成 report.html
    5. step_plots()      生成全部汇总图表
    6. step_process()    生成过程分析报告（可选）

跳过功能的方法：
    打开 run_all()，把不需要的那一行注释掉即可，例如：
        # step_plots(config, benchmark_csv)

日志目录自动检测：
    默认找项目内 logs；如果里面没有实验，会自动尝试项目上一级的 logs
    （例如 D:\\document\\coding\\policy\\logs），避免“未找到实验”。
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# 确保 src 目录在 sys.path 中，无需 pip install -e .
_src = Path(__file__).resolve().parent / "src"
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from drl_analyzer.analyzer import Analyzer
from drl_analyzer.config import AnalyzerConfig, WandBConfig
from drl_analyzer.exporter import BenchmarkExporter
from drl_analyzer.logger import get_logger
from drl_analyzer.process_analyzer import analyze_process, build_process_report
from drl_analyzer.report import ReportGenerator
from drl_analyzer.summary import SummaryGenerator
from drl_analyzer.utils import load_yaml
from drl_analyzer.visualization.summary_plot import SummaryPlotter

# ============================================================
# 默认配置（点击运行前可在这里改默认路径）
# ============================================================
DEFAULT_LOG_ROOT = "logs"
DEFAULT_OUTPUT_DIR = "results"
DEFAULT_CONFIG_FILE = "config.yaml"       # 可选，不存在则忽略
DEFAULT_PROCESS_REPORT = ""               # 留空则不生成过程报告
# ============================================================

TOTAL_STEPS = 6


def parse_args(argv=None):
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="DRL Experiment Analyzer —— 一键运行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py
  python run.py --log-root ./logs --output ./results
  python run.py --log-root ./logs --output ./results --config config.yaml
  python run.py --log-root ./logs --output ./results --process-report results/process.md
  python run.py --no-wandb --no-plots
        """.strip(),
    )
    parser.add_argument("--log-root", default=DEFAULT_LOG_ROOT, help="实验日志根目录")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_DIR, help="输出目录")
    parser.add_argument("--config", default=DEFAULT_CONFIG_FILE, help="YAML 配置文件（不存在则忽略）")
    parser.add_argument("--no-wandb", action="store_true", help="禁用 WandB 在线获取")
    parser.add_argument("--no-plots", action="store_true", help="不生成图表")
    parser.add_argument("--process-report", default=DEFAULT_PROCESS_REPORT, help="过程分析 Markdown 输出路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出 DEBUG 日志")
    return parser.parse_args(argv)


def build_config(args) -> AnalyzerConfig:
    """根据命令行参数和可选 YAML 构建配置，命令行参数优先。"""
    config = AnalyzerConfig()

    # 尝试加载 YAML 配置文件
    yaml_path = Path(args.config) if args.config else None
    if yaml_path and yaml_path.exists():
        print(f"[INFO] 加载配置文件: {yaml_path}")
        data = load_yaml(yaml_path)
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


# ============================================================
# 日志目录自动检测
# ============================================================

def _has_wandb_runs(root: Path) -> bool:
    """判断目录下是否至少存在一个 wandb run。"""
    root = Path(root)
    if not root.exists():
        return False
    return any(root.rglob("wandb/run-*"))


def resolve_log_root(log_root: Path, allow_fallback: bool = True) -> Path:
    """
    解析实际日志目录。

    规则：
    - 指定路径本身有实验，直接使用。
    - 默认路径（logs）没有实验时，自动尝试项目上一级 logs。
    - 显式传入 --log-root 时不自动替换，方便排查。
    """
    root = Path(log_root)
    if _has_wandb_runs(root):
        return root

    if allow_fallback:
        project = Path(__file__).resolve().parent
        candidates = [project / "logs", project.parent / "logs"]
        for candidate in candidates:
            if candidate != root and _has_wandb_runs(candidate):
                print(f"[INFO] {root} 中没有实验，自动使用: {candidate}")
                return candidate
    return root


# ============================================================
# 各功能步骤（每步独立，可单独调用）
# ============================================================

def step_analyze(config: AnalyzerConfig):
    """第 1 步：扫描实验并计算指标，返回 Experiment 列表。"""
    print(f"[1/{TOTAL_STEPS}] 扫描实验并计算指标 ...")
    analyzer = Analyzer(config)
    experiments = analyzer.analyze()
    if not experiments:
        print(f"[WARN] 未找到任何实验，请确认日志目录: {config.log_root}")
    else:
        print(f"[1/{TOTAL_STEPS}] 完成：共 {len(experiments)} 个实验")
    return experiments


def step_export(config: AnalyzerConfig, experiments):
    """第 2 步：导出 benchmark.csv / report.xlsx。"""
    print(f"[2/{TOTAL_STEPS}] 导出 CSV / Excel ...")
    exporter = BenchmarkExporter(config.output_dir)
    paths = []
    if config.save_csv:
        paths.append(exporter.export_csv(experiments))
    if config.save_excel:
        paths.append(exporter.export_excel(experiments))
    for p in paths:
        print(f"    - 已生成: {p}")
    return paths


def step_summary(config: AnalyzerConfig, benchmark_csv) -> Path:
    """第 3 步：生成 summary.md。"""
    print(f"[3/{TOTAL_STEPS}] 生成 Markdown 摘要 ...")
    output = config.output_dir / "summary.md"
    SummaryGenerator().generate(benchmark_csv, output)
    print(f"    - 已生成: {output}")
    return output


def step_report(config: AnalyzerConfig, benchmark_csv) -> Path:
    """第 4 步：生成 report.html。"""
    print(f"[4/{TOTAL_STEPS}] 生成 HTML 报告 ...")
    output = config.output_dir / "report.html"
    ReportGenerator().generate(
        benchmark_csv,
        figure_dir=config.output_dir / "figures",
        output=output,
    )
    print(f"    - 已生成: {output}")
    return output


def step_plots(config: AnalyzerConfig, benchmark_csv):
    """第 5 步：生成全部汇总图表。"""
    if not config.save_figures:
        print(f"[5/{TOTAL_STEPS}] 跳过图表（save_figures=False）")
        return None
    print(f"[5/{TOTAL_STEPS}] 生成图表 ...")
    plotter = SummaryPlotter(config.output_dir / "figures")
    plotter.plot_all(benchmark_csv)
    print(f"    - 已生成: {config.output_dir / 'figures'}")
    return config.output_dir / "figures"


def step_process(config: AnalyzerConfig, experiments, process_report: str | None) -> Path | None:
    """第 6 步（可选）：生成过程分析报告 process.md。"""
    if not process_report:
        print(f"[6/{TOTAL_STEPS}] 跳过过程分析（未指定 --process-report）")
        return None
    print(f"[6/{TOTAL_STEPS}] 生成过程分析报告 ...")
    sections = []
    for exp in experiments:
        if exp.history is None or exp.history.empty:
            continue
        analysis = analyze_process(exp.history)
        sections.append(build_process_report(exp, analysis))
    output_path = Path(process_report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n\n".join(sections), encoding="utf-8")
    print(f"    - 已生成: {output_path}")
    return output_path


# ============================================================
# 总调用：想跳过某一步，直接注释掉对应那一行
# ============================================================

def run_all(config: AnalyzerConfig, process_report: str | None = None) -> int:
    """按顺序运行全部功能步骤。"""
    experiments = step_analyze(config)                     # 1. 分析（建议保留）
    if not experiments:
        return 1

    step_export(config, experiments)                       # 2. 导出 CSV/Excel

    benchmark_csv = config.output_dir / "benchmark.csv"

    step_summary(config, benchmark_csv)                    # 3. Markdown 摘要
    step_report(config, benchmark_csv)                     # 4. HTML 报告
    step_plots(config, benchmark_csv)                      # 5. 图表
    step_process(config, experiments, process_report)      # 6. 过程分析（可选）

    return 0


# ============================================================
# 主入口
# ============================================================

def main(argv=None) -> int:
    """一键运行主函数。"""
    args = parse_args(argv)
    get_logger("DRLAnalyzer", level=logging.DEBUG if args.verbose else logging.INFO)
    config = build_config(args)

    # 自动检测日志目录：默认路径没数据时改用上一级 logs
    config.log_root = resolve_log_root(
        config.log_root,
        allow_fallback=(args.log_root == DEFAULT_LOG_ROOT),
    )
    if args.no_plots:
        config.save_figures = False

    _print_banner(config, args)
    code = run_all(config, process_report=args.process_report)
    _print_footer(config, args)
    return code


def _print_banner(config: AnalyzerConfig, args) -> None:
    """打印启动信息。"""
    print("=" * 60)
    print("  DRL Experiment Analyzer v2.0.0")
    print("=" * 60)
    print(f"  日志目录:     {config.log_root}")
    print(f"  输出目录:     {config.output_dir}")
    print(f"  WandB 在线:   {'启用' if config.wandb.enabled else '禁用'}")
    print(f"  生成图表:     {'是' if config.save_figures else '否'}")
    if args.process_report:
        print(f"  过程报告:     {args.process_report}")
    print("=" * 60)
    print()


def _print_footer(config: AnalyzerConfig, args) -> None:
    """打印完成信息与输出文件清单。"""
    print()
    print("=" * 60)
    print("  分析完成！")
    out = config.output_dir
    for name in ("benchmark.csv", "report.xlsx", "summary.md", "report.html"):
        if (out / name).exists():
            print(f"  已生成: {out / name}")
    if (out / "figures").exists():
        print(f"  已生成: {out / 'figures'}")
    if args.process_report and Path(args.process_report).exists():
        print(f"  已生成: {Path(args.process_report)}")
    print("=" * 60)


if __name__ == "__main__":
    sys.exit(main())