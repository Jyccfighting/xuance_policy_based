from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class SummaryPlotter:

    def __init__(self):

        self.save_dir = Path("results/figures")

        self.save_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================
    # Average Final Reward
    # =====================================

    def plot_average_reward(
        self,
        csv_file
    ):

        df = pd.read_csv(csv_file)

        data = (

            df.groupby("algorithm")["final_reward"]

            .mean()

            .sort_values(
                ascending=False
            )

        )

        plt.figure(figsize=(8,5))

        plt.bar(
            data.index,
            data.values
        )

        plt.ylabel(
            "Average Final Reward"
        )

        plt.title(
            "Average Final Reward"
        )

        plt.tight_layout()

        plt.savefig(
            self.save_dir /
            "average_reward.png"
        )

        plt.close()

    # =====================================
    # Average Runtime
    # =====================================

    def plot_average_runtime(
        self,
        csv_file
    ):

        df = pd.read_csv(csv_file)

        data = (

            df.groupby("algorithm")["runtime"]

            .mean()

            .sort_values()

        )

        plt.figure(figsize=(8,5))

        plt.bar(
            data.index,
            data.values
        )

        plt.ylabel(
            "Average Runtime (s)"
        )

        plt.title(
            "Average Runtime"
        )

        plt.tight_layout()

        plt.savefig(
            self.save_dir /
            "average_runtime.png"
        )

        plt.close()

    # =====================================
    # Average Stability
    # =====================================

    def plot_average_stability(
        self,
        csv_file
    ):

        df = pd.read_csv(csv_file)

        df = df.dropna(
            subset=["stability"]
        )

        data = (

            df.groupby("algorithm")["stability"]

            .mean()

            .sort_values(
                ascending=False
            )

        )

        plt.figure(figsize=(8,5))

        plt.bar(
            data.index,
            data.values
        )

        plt.ylabel(
            "Average Stability (%)"
        )

        plt.title(
            "Average Stability"
        )

        plt.tight_layout()

        plt.savefig(
            self.save_dir /
            "average_stability.png"
        )

        plt.close()

    # =====================================
    # Average Sample Efficiency
    # =====================================

    def plot_average_efficiency(
        self,
        csv_file
    ):

        df = pd.read_csv(csv_file)

        data = (

            df.groupby("algorithm")["sample_efficiency"]

            .mean()

            .sort_values(
                ascending=False
            )

        )

        plt.figure(figsize=(8,5))

        plt.bar(
            data.index,
            data.values
        )

        plt.ylabel(
            "Average Sample Efficiency"
        )

        plt.title(
            "Average Sample Efficiency"
        )

        plt.tight_layout()

        plt.savefig(
            self.save_dir /
            "average_sample_efficiency.png"
        )

        plt.close()

    # =====================================
    # Win Count
    # =====================================

    def plot_win_count(
        self,
        csv_file
    ):

        df = pd.read_csv(csv_file)

        winner = (

            df.loc[
                df.groupby(
                    "environment"
                )[
                    "final_reward"
                ].idxmax()
            ]

        )

        data = (

            winner["algorithm"]

            .value_counts()

            .sort_values(
                ascending=False
            )

        )

        plt.figure(figsize=(8,5))

        plt.bar(
            data.index,
            data.values
        )

        plt.ylabel(
            "Number of Wins"
        )

        plt.title(
            "Algorithm Win Count"
        )

        plt.tight_layout()

        plt.savefig(
            self.save_dir /
            "win_count.png"
        )

        plt.close()

    # =====================================
    # Overall Score
    # =====================================

    def plot_overall_score(
        self,
        csv_file
    ):

        df = pd.read_csv(csv_file)

        score = (

            df.groupby("algorithm")[

                [
                    "final_reward",
                    "stability",
                    "sample_efficiency"

                ]

            ]

            .mean()

        )

        reward = (

            score.final_reward -

            score.final_reward.min()

        ) / (

            score.final_reward.max() -

            score.final_reward.min() +

            1e-6

        )

        stability = (

            score.stability -

            score.stability.min()

        ) / (

            score.stability.max() -

            score.stability.min() +

            1e-6

        )

        efficiency = (

            score.sample_efficiency -

            score.sample_efficiency.min()

        ) / (

            score.sample_efficiency.max() -

            score.sample_efficiency.min() +

            1e-6

        )

        runtime = (

            df.groupby("algorithm")["runtime"]

            .mean()

        )

        runtime = (

            runtime.max() -

            runtime

        ) / (

            runtime.max() -

            runtime.min() +

            1e-6

        )

        total = (

            0.4 * reward +

            0.2 * runtime +

            0.2 * stability +

            0.2 * efficiency

        )

        total = total.sort_values(
            ascending=False
        )

        plt.figure(figsize=(8,5))

        plt.bar(
            total.index,
            total.values
        )

        plt.ylabel(
            "Overall Score"
        )

        plt.title(
            "Overall Algorithm Ranking"
        )

        plt.tight_layout()

        plt.savefig(
            self.save_dir /
            "overall_score.png"
        )

        plt.close()