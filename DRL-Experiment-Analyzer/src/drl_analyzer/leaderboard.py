from pathlib import Path

import pandas as pd


class LeaderBoard:

    def generate(
        self,
        csv_file,
        output="results/leaderboard.csv"
    ):

        df = pd.read_csv(csv_file)

        score = df.groupby(
            "algorithm"
        ).agg({

            "final_reward": "mean",

            "runtime": "mean",

            "stability": "mean",

            "sample_efficiency": "mean"

        })

        # -----------------------------
        # Normalize
        # -----------------------------

        reward = (

            score.final_reward -

            score.final_reward.min()

        ) / (

            score.final_reward.max()

            - score.final_reward.min()

            + 1e-6

        )

        runtime = (

            score.runtime.max()

            - score.runtime

        ) / (

            score.runtime.max()

            - score.runtime.min()

            + 1e-6

        )

        stability = (

            score.stability -

            score.stability.min()

        ) / (

            score.stability.max()

            - score.stability.min()

            + 1e-6

        )

        efficiency = (

            score.sample_efficiency -

            score.sample_efficiency.min()

        ) / (

            score.sample_efficiency.max()

            - score.sample_efficiency.min()

            + 1e-6

        )

        score["overall_score"] = (

            0.4 * reward +

            0.2 * runtime +

            0.2 * stability +

            0.2 * efficiency

        )

        score = score.sort_values(

            "overall_score",

            ascending=False

        )

        score.insert(

            0,

            "Rank",

            range(

                1,

                len(score)+1

            )

        )

        output = Path(output)

        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        score.to_csv(

            output,

            index=True

        )

        return output