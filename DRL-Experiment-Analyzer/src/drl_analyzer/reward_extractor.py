"""
reward_extractor.py

Extract reward from different DRL frameworks.
"""

import pandas as pd


class RewardExtractor:


    @staticmethod
    def extract(
        history: pd.DataFrame
    ):

        columns = history.columns



        # ==========================
        # Xuance
        # ==========================

        xuance_cols = [
            c for c in columns
            if "Train-Episode-Rewards" in c
        ]


        if xuance_cols:


            reward = (
                history[xuance_cols]
                .mean(axis=1)
            )

            return reward



        # ==========================
        # Stable Baselines3
        # ==========================

        sb3_candidates = [

            "rollout/ep_rew_mean",

            "episode_reward"

        ]


        for key in sb3_candidates:

            if key in columns:

                return history[key]



        # ==========================
        # CleanRL
        # ==========================

        cleanrl_candidates=[

            "charts/episodic_return",

            "charts/episode_return"

        ]


        for key in cleanrl_candidates:

            if key in columns:

                return history[key]



        # ==========================
        # generic
        # ==========================

        if "reward" in columns:

            return history["reward"]



        return None