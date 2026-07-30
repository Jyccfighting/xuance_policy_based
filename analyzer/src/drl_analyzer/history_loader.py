"""
history_loader.py

Load WandB History CSV into pandas DataFrame.

Author : yyJ
Version : 1.0
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


class HistoryLoader:
    """
    Load WandB exported history CSV.

    Example
    -------
    loader = HistoryLoader()

    history = loader.load(
        Path("history.csv")
    )
    """

    def __init__(self):

        pass

    # ----------------------------------------------------
    # Public API
    # ----------------------------------------------------

    def load(
        self,
        csv_path: Path
    ) -> Optional[pd.DataFrame]:
        """
        Load one history csv.

        Parameters
        ----------
        csv_path : Path

        Returns
        -------
        DataFrame or None
        """

        csv_path = Path(csv_path)

        if not csv_path.exists():

            logger.warning(
                f"History file not found:\n{csv_path}"
            )

            return None

        try:

            history = pd.read_csv(csv_path)

        except Exception as e:

            logger.exception(e)

            return None

        history = self.clean(history)

        logger.info(
            "History loaded: %d rows × %d columns",
            len(history),
            len(history.columns)
        )

        return history

    # ----------------------------------------------------
    # Clean Data
    # ----------------------------------------------------

    def clean(
        self,
        history: pd.DataFrame
    ) -> pd.DataFrame:

        history = history.copy()

        history.columns = [

            str(c).strip()

            for c in history.columns

        ]

        history = history.drop_duplicates()

        history = history.reset_index(drop=True)

        return history
    
    # ----------------------------------------------------
    # Reward Column
    # ----------------------------------------------------

    @staticmethod
    def reward_column(history):

        candidates = [

            "train/episode_reward",

            "episode_reward",

            "reward",

            "Reward",

            "episode_return",

            "returns",

            "eval/reward"

        ]

        for col in candidates:

            if col in history.columns:

                return col

        return None

    # ----------------------------------------------------

    @staticmethod
    def loss_column(history):

        candidates = [

            "loss",

            "Loss",

            "train/loss",

            "critic_loss",

            "actor_loss",

            "q_loss"

        ]

        for col in candidates:

            if col in history.columns:

                return col

        return None

    # ----------------------------------------------------

    @staticmethod
    def step_column(history):

        candidates = [

            "_step",

            "global_step",

            "step",

            "train_step"

        ]

        for col in candidates:

            if col in history.columns:

                return col

        return None

    # ----------------------------------------------------

    @staticmethod
    def runtime_column(history):

        if "_runtime" in history.columns:

            return "_runtime"

        return None
    
    def reward(
        self,
        history
    ):

        col = self.reward_column(history)

        if col is None:

            return None

        return history[col]


    def loss(
        self,
        history
    ):

        col = self.loss_column(history)

        if col is None:

            return None

        return history[col]


    def steps(
        self,
        history
    ):

        col = self.step_column(history)

        if col is None:

            return pd.Series(
                range(len(history))
            )

        return history[col]