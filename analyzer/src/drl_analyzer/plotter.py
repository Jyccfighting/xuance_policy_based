"""
plotter.py

DRL Experiment Plotter

Author : yyJ
Version : 1.0
"""

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


class Plotter:

    def __init__(self, output_dir: Path):

        self.output_dir = output_dir

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        
    def get_env_dir(
        self,
        env_name: str
    ) -> Path:

        path = self.output_dir / env_name

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    def reward_curve(
        self,
        history: pd.DataFrame,
        algorithm: str,
        environment: str
    ):

        reward_columns = [

            "train/episode_reward",

            "episode_reward",

            "reward",

            "Reward"

        ]

        reward = None

        for col in reward_columns:

            if col in history.columns:

                reward = history[col]

                break

        if reward is None:

            print("Reward column not found.")

            return

        plt.figure(figsize=(8,5))

        plt.plot(
            reward,
            label=algorithm
        )

        plt.xlabel("Training Step")

        plt.ylabel("Reward")

        plt.title(
            f"{algorithm} - {environment}"
        )

        plt.grid(True)

        plt.legend()

        save_dir = self.get_env_dir(
            environment
        )

        plt.savefig(

            save_dir /
            "reward_curve.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()
        
    def loss_curve(
        self,
        history: pd.DataFrame,
        algorithm: str,
        environment: str
    ):

        loss_columns = [

            "loss",

            "Loss",

            "train/loss"

        ]

        loss = None

        for col in loss_columns:

            if col in history.columns:

                loss = history[col]

                break

        if loss is None:

            return

        plt.figure(figsize=(8,5))

        plt.plot(loss)

        plt.xlabel("Training Step")

        plt.ylabel("Loss")

        plt.title(

            f"{algorithm} Loss"

        )

        plt.grid(True)

        save_dir = self.get_env_dir(
            environment
        )

        plt.savefig(

            save_dir /
            "loss_curve.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()
        
        
    def reward_bar(
        self,
        summary_df: pd.DataFrame,
        environment: str
    ):

        plt.figure(figsize=(10,6))

        plt.bar(

            summary_df["Algorithm"],

            summary_df["Final Reward"]

        )

        plt.ylabel("Reward")

        plt.title(

            f"{environment} Final Reward"

        )

        plt.xticks(rotation=30)

        plt.grid(axis="y")

        save_dir = self.get_env_dir(
            environment
        )

        plt.savefig(

            save_dir /
            "reward_bar.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()