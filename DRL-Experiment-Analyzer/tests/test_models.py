from drl_analyzer.models import (
    Experiment,
    Metrics,
    TrainingHistory,
)


def main():

    metrics = Metrics(
        final_reward=500,
        mean_reward=450
    )

    exp = Experiment(
        algorithm="C51",
        environment="CartPole-v1",
        seed=1,
        metrics=metrics
    )


    print(exp)


if __name__ == "__main__":
    main()