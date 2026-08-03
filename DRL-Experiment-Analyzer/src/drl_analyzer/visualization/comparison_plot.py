from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

class ComparisonPlotter:

    def plot_heatmap(
        self,
        csv_file,
        env_name,
        save_dir="results"
    ):

        df = pd.read_csv(csv_file)

        df = df[
            df.environment == env_name
        ]

        if df.empty:
            return

        metrics = [

            "final_reward",
            "runtime",
            "stability"

        ]

        table = df.set_index(
            "algorithm"
        )[metrics]

        plt.figure(figsize=(8,5))

        plt.imshow(
            table,
            aspect="auto"
        )

        plt.xticks(
            range(len(metrics)),
            metrics
        )

        plt.yticks(
            range(len(table.index)),
            table.index
        )

        plt.colorbar()

        Path(save_dir).mkdir(
            exist_ok=True
        )

        plt.savefig(
            Path(save_dir) /
            f"{env_name}_heatmap.png"
        )

        plt.close()
    def plot_score(
        self,
        csv_file,
        env_name,
        save_dir="results"
    ):

        df = pd.read_csv(csv_file)

        df = df[
            df.environment == env_name
        ].copy()

        if df.empty:
            return

        reward = (
            df.final_reward -
            df.final_reward.min()
        ) / (
            df.final_reward.max() -
            df.final_reward.min() +
            1e-6
        )

        runtime = (
            df.runtime.max() -
            df.runtime
        ) / (
            df.runtime.max() -
            df.runtime.min() +
            1e-6
        )

        stability = (
            df.stability -
            df.stability.min()
        ) / (
            df.stability.max() -
            df.stability.min() +
            1e-6
        )

        efficiency = (
            df.sample_efficiency -
            df.sample_efficiency.min()
        ) / (
            df.sample_efficiency.max() -
            df.sample_efficiency.min() +
            1e-6
        )

        score = (

            0.4 * reward +

            0.2 * runtime +

            0.2 * stability +

            0.2 * efficiency

        )

        plt.figure(figsize=(8,5))

        plt.bar(
            df.algorithm,
            score
        )

        plt.ylabel(
        "Overall Score"
    )

    plt.tight_layout()

    Path(save_dir).mkdir(
        exist_ok=True
    )

    plt.savefig(
        Path(save_dir) /
        f"{env_name}_score.png"
    )

    plt.close()