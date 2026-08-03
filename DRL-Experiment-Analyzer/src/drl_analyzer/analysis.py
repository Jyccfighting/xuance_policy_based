import pandas as pd


class ExperimentAnalyzer:


    def analyze(
        self,
        df: pd.DataFrame
    ):


        result = {}


        # ==========================
        # 最佳最终奖励
        # ==========================

        best_reward = df.loc[
            df.final_reward.idxmax()
        ]


        result["best_reward_algorithm"] = (
            best_reward.algorithm
        )


        result["best_reward_env"] = (
            best_reward.environment
        )


        result["best_reward_value"] = (
            round(
                best_reward.final_reward,
                3
            )
        )


        # ==========================
        # 最稳定算法
        # ==========================

        stable = df.loc[
            df.stability.idxmax()
        ]


        result["best_stability_algorithm"] = (
            stable.algorithm
        )


        result["best_stability_value"] = (
            round(
                stable.stability,
                3
            )
        )


        # ==========================
        # 最快算法
        # ==========================

        fastest = df.loc[
            df.runtime.idxmin()
        ]


        result["fastest_algorithm"] = (
            fastest.algorithm
        )


        result["fastest_time"] = (
            round(
                fastest.runtime,
                3
            )
        )


        return result