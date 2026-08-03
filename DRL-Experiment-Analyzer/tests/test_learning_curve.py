from drl_analyzer.analyzer import Analyzer
from drl_analyzer.visualization.learning_curve import LearningCurvePlotter



analyzer = Analyzer(
    "D:/document/coding/policy/logs"
)


experiments = analyzer.analyze()



histories=[]


for exp in experiments:


    if exp.history is None:
        continue


    histories.append(
        {
            "algorithm":
                exp.algorithm,

            "history":
                exp.history
        }
    )



plotter=LearningCurvePlotter()


plotter.plot(
    histories,
    "Pendulum-v1",
    smooth_window=50
)