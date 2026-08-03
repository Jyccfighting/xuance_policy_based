from drl_analyzer.visualization.summary_plot import SummaryPlotter

plotter = SummaryPlotter()

csv = "results/benchmark.csv"

plotter.plot_average_reward(csv)

plotter.plot_average_runtime(csv)

plotter.plot_average_stability(csv)

plotter.plot_average_efficiency(csv)

plotter.plot_win_count(csv)

plotter.plot_overall_score(csv)

print("Finished.")