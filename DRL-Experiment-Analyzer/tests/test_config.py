from drl_analyzer.config import (
    AnalyzerConfig,
    ExperimentConfig,
)


def main():

    analyzer = AnalyzerConfig()

    print(analyzer)


    xuance_yaml = {

        "agent": "C51",

        "env_id": "CartPole-v1",

        "env_seed": 1,

        "gamma": 0.99,

        "learning_rate":0.001

    }


    exp_config = ExperimentConfig.from_dict(
        xuance_yaml
    )


    print(exp_config)


if __name__ == "__main__":
    main()