from pathlib import Path

from drl_analyzer.analyzer import Analyzer


analyzer = Analyzer(

    Path(
        r"D:\\document\\coding\\policy\\logs"
    )

)

experiments = analyzer.analyze()

print()

print("=" * 60)

print("Experiments:", len(experiments))

print("=" * 60)

for exp in experiments:

    print()

    print(exp.algorithm)

    print(exp.environment)

    print(exp.metrics.final_reward)

    print(exp.metrics.best_reward)

    print(exp.metrics.mean_reward)

    print(exp.metrics.runtime)