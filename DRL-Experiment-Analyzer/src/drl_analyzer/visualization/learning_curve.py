from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd



class LearningCurvePlotter:


    def plot(
        self,
        histories,
        env_name,
        save_dir="results/figures",
        smooth_window=50
    ):


        Path(
            save_dir
        ).mkdir(
            exist_ok=True
        )


        plt.figure(
            figsize=(10,6)
        )


        for item in histories:


            algorithm = item["algorithm"]

            history = item["history"]



            reward = self.extract_reward(
                history
            )


            if reward is None:
                continue



            # ======================
            # Moving Average
            # ======================

            smooth_reward = (
                reward
                .rolling(
                    smooth_window
                )
                .mean()
            )


            plt.plot(
                smooth_reward,
                label=algorithm
            )



        plt.xlabel(
            "Training Steps"
        )


        plt.ylabel(
            "Average Episode Reward"
        )


        plt.title(
            f"{env_name} Learning Curve"
        )


        plt.legend()


        plt.grid()


        plt.tight_layout()



        plt.savefig(
            Path(save_dir)
            /
            f"{env_name}_smooth_learning_curve.png",
            dpi=300
        )


        plt.close()



    def extract_reward(
        self,
        history
    ):


        columns=[

            c

            for c in history.columns

            if 
            "Train-Episode-Rewards"
            in c

        ]


        if len(columns)==0:


            columns=[

                c

                for c in history.columns

                if
                "Test-Episode-Rewards"
                in c

            ]


        if len(columns)==0:

            return None



        reward=(

            history[columns]

            .mean(axis=1)

        )


        reward=(

            reward

            .dropna()

        )


        return reward