# """
# ===========================================================
# DRL Experiment Analyzer
# Main Entrance

# Author : yyJ & ChatGPT
# Version: 1.0
# ===========================================================
# """

from pathlib import Path
from collections import defaultdict

from config import (
    LOGS_DIR,
)

from scanner import ExperimentScanner
from parser import ExperimentParser
from manager import ExperimentManager

from excel_writer import ExcelWriter
from config import EXCEL_DIR

from plotter import Plotter

from config import PLOT_DIR

# self.plotter = Plotter(PLOT_DIR)

# class Analyzer:
#     """
#     DRL Experiment Analyzer
#     """

#     def __init__(self):

#         self.scanner = ExperimentScanner(LOGS_DIR)

#         self.parser = ExperimentParser()

#         self.experiments = []

#     # ---------------------------------------------------
#     # Scan
#     # ---------------------------------------------------

#     def scan(self):

#         print("\nScanning logs...\n")

#         self.experiments = self.scanner.scan()

#         print(f"Found {len(self.experiments)} experiments.\n")
        
#         experiments = self.scanner.scan()

#         self.manager.add_many(experiments)

#     # ---------------------------------------------------
#     # Parse
#     # ---------------------------------------------------

#     def parse(self):

#         print("Loading config & summary...\n")

#         for exp in self.experiments:

#             self.parser.parse(exp)

#         print("Done.\n")

#     # ---------------------------------------------------
#     # Show Overview
#     # ---------------------------------------------------

#     def overview(self):

#         print("=" * 80)

#         print("Experiment Overview")

#         print("=" * 80)

#         table = defaultdict(list)

#         for exp in self.experiments:

#             table[exp.algorithm].append(exp.environment)

#         total_env = set()

#         for algo in sorted(table.keys()):

#             envs = sorted(set(table[algo]))

#             total_env.update(envs)

#             print(f"\n{algo}")

#             for env in envs:

#                 count = sum(
#                     1
#                     for e in self.experiments
#                     if e.algorithm == algo
#                     and e.environment == env
#                 )

#                 print(f"    {env:<25} {count} run(s)")

#         print("\n" + "-" * 80)

#         print(f"Algorithms   : {len(table)}")

#         print(f"Environments : {len(total_env)}")

#         print(f"Runs         : {len(self.experiments)}")

#         print("-" * 80)

#     # ---------------------------------------------------
#     # Detail
#     # ---------------------------------------------------

#     def detail(self):

#         print("\n")

#         print("=" * 80)

#         print("Experiment Detail")

#         print("=" * 80)

#         for exp in self.experiments:

#             print()

#             print(f"Algorithm   : {exp.algorithm}")

#             print(f"Environment : {exp.environment}")

#             print(f"Run         : {exp.run_name}")

#             print(f"Config      : {exp.config_path.exists()}")

#             print(f"Summary     : {exp.summary_path.exists()}")

#             print(f"WandB File  : {exp.wandb_file.exists()}")

#     # ---------------------------------------------------
#     # Parameter Check
#     # (后面升级)
#     # ---------------------------------------------------

#     def parameter_check(self):

#         print("\nParameter Check")

#         print("---------------------------")

#         print("Coming Soon...")

#     # ---------------------------------------------------
#     # Export
#     # (后面升级)
#     # ---------------------------------------------------

#     def export(self):

#         print("\nExport")

#         print("---------------------------")

#         print("Coming Soon...")

#     # ---------------------------------------------------
#     # Plot
#     # (后面升级)
#     # ---------------------------------------------------

#     def plot(self):

#         print("\nPlot")

#         print("---------------------------")

#         print("Coming Soon...")

#     # ---------------------------------------------------
#     # Report
#     # (后面升级)
#     # ---------------------------------------------------

#     def report(self):

#         print("\nReport")

#         print("---------------------------")

#         print("Coming Soon...")



#     # ---------------------------------------------------
#     # Excel
#     # ---------------------------------------------------

#     def export_excel(self):

#         print("\nGenerating Excel...")

#         self.writer.export(

#         self.manager.get_all()

#     )
        
        
        
#     # ---------------------------------------------------
#     # Run
#     # ---------------------------------------------------

#     def run(self):

#         self.scan()

#         self.parse()

#         self.overview()

#         self.detail()
        
#         self.export_excel()

#         # v2
#         # self.parameter_check()

#         # v3
#         # self.export()

#         # v4
#         # self.plot()

#         # v5
#         # self.report()


# # ===========================================================
# # Main
# # ===========================================================

# def print_logo():

#     print("=" * 80)

#     print("DRL Experiment Analyzer")

#     print("Version 1.0")

#     print("=" * 80)


# def main():

#     print_logo()

#     analyzer = Analyzer()

#     analyzer.run()


# if __name__ == "__main__":

#     main()
#     self.writer = ExcelWriter(EXCEL_DIR)

class Analyzer:

    def __init__(self):

        self.scanner = ExperimentScanner(LOGS_DIR)

        self.manager = ExperimentManager()

        self.parser = ExperimentParser()

        self.history_loader = HistoryLoader()

        self.metrics_calculator = MetricsCalculator()

        self.excel_writer = ExcelWriter(EXCEL_DIR)

        self.plotter = Plotter(PLOT_DIR)
        
        
def run(self):

    print("=" * 80)
    print("DRL Experiment Analyzer")
    print("=" * 80)

    # 1 扫描实验
    experiments = self.scanner.scan()

    self.manager.add_many(experiments)

    print(f"Found {self.manager.count()} experiments.\n")

    # 2 解析 Config 和 Summary
    for exp in self.manager.get_all():

        self.parser.parse(exp)

    # 3 加载 History
    for exp in self.manager.get_all():

        if exp.history_csv_path:

            exp.history = self.history_loader.load(
                exp.history_csv_path
            )

    # 4 计算 Metrics
    for exp in self.manager.get_all():

        if exp.history is not None:

            exp.metrics = self.metrics_calculator.calculate(
                exp.history
            )

    # 5 导出 Excel
    self.excel_writer.export(
        self.manager.get_all()
    )

    # 6 画图
    for exp in self.manager.get_all():

        if exp.history is None:
            continue

        self.plotter.reward_curve(
            exp.history,
            exp.algorithm,
            exp.environment
        )

        self.plotter.loss_curve(
            exp.history,
            exp.algorithm,
            exp.environment
        )

    print("\nAnalysis Finished.")