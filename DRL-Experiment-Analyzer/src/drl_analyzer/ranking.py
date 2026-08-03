import pandas as pd


class Ranking:


    def rank(
        self,
        csv_file,
        env_name
    ):


        df = pd.read_csv(csv_file)


        df=df[
            df.environment==env_name
        ]


        metrics=[
            "final_reward",
            "stability",
            "sample_efficiency"
        ]


        df["rank_score"]=(
            df.final_reward.rank(
                ascending=False
            )
            +
            df.stability.rank(
                ascending=False
            )
            +
            df.sample_efficiency.rank(
                ascending=False
            )
        )


        return df.sort_values(
            "rank_score"
        )