"""
Plot training reward curves
"""

from pathlib import Path
import matplotlib.pyplot as plt



class RewardPlotter:


    def __init__(
        self,
        save_dir="results/figures"
    ):

        self.save_dir = Path(save_dir)

        self.save_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def plot_single(
        self,
        experiment,
        reward
    ):

        plt.figure(
            figsize=(8,5)
        )


        plt.plot(
            reward
        )


        plt.xlabel(
            "Training Step"
        )

        plt.ylabel(
            "Reward"
        )


        plt.title(
            f"{experiment.algorithm}-{experiment.environment}"
        )


        plt.grid()


        path = (
            self.save_dir /
            f"{experiment.algorithm}_{experiment.environment}.png"
        )


        plt.savefig(
            path,
            dpi=300,
            bbox_inches="tight"
        )


        plt.close()



    def plot_compare(
        self,
        experiments
    ):


        plt.figure(
            figsize=(10,6)
        )


        for exp in experiments:


            if exp.history is None:
                continue


            reward = exp.history


            plt.plot(
                reward,
                label=exp.algorithm
            )


        plt.xlabel(
            "Training Step"
        )


        plt.ylabel(
            "Reward"
        )


        plt.legend()


        plt.grid()


        plt.savefig(
            self.save_dir /
            "algorithm_compare.png",
            dpi=300,
            bbox_inches="tight"
        )


        plt.close()