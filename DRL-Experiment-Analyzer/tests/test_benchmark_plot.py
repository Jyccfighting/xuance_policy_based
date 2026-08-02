from pathlib import Path

from drl_analyzer.visualization.benchmark_plot import BenchmarkPlotter


ROOT = Path(__file__).resolve().parents[1]


csv_file = (
    ROOT /
    "results" /
    "benchmark.csv"
)


plotter = BenchmarkPlotter()


plotter.plot_final_reward(
    csv_file
)