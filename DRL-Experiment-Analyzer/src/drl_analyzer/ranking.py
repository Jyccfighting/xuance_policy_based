import pandas as pd


class Ranking:


    def rank(
        self,
        csv_file
    ):


        df = pd.read_csv(csv_file)


        result={}


        for env in df.environment.unique():

            data=df[
                df.environment==env
            ]


            data=data.sort_values(
                "final_reward",
                ascending=False
            )


            result[env]=data[
                [
                    "algorithm",
                    "final_reward"
                ]
            ]


        return result