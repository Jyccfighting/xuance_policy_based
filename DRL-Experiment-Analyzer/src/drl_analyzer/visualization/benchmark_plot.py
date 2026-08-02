from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class BenchmarkPlotter:

    def plot_final_reward(
        self,
        csv_file,
        save_dir="plots"
    ):

        csv_file = Path(csv_file)

        save_dir = Path(save_dir)

        save_dir.mkdir(
            exist_ok=True
        )


        df = pd.read_csv(csv_file)


        plt.figure(
            figsize=(10,6)
        )


        plt.bar(
            df["algorithm"],
            df["final_reward"]
        )


        plt.title(
            "Final Reward"
        )

        plt.ylabel(
            "Reward"
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()


        plt.savefig(
            save_dir /
            "final_reward.png",
            dpi=300
        )


        plt.close()