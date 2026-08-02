from drl_analyzer.analyzer import Analyzer
from drl_analyzer.visualization.reward_plot import RewardPlotter


analyzer = Analyzer(
    "D:/document/coding/policy/logs"
)


experiments = analyzer.analyze()


print(
    "experiments:",
    len(experiments)
)


plotter = RewardPlotter()


for exp in experiments:

    plotter = RewardPlotter()


    for exp in experiments:


        print(
            exp.algorithm,
            exp.environment
        )


        plotter.plot_reward_curve(
            exp.reward_history,
            title=
            f"{exp.algorithm}-{exp.environment}"
        )