"""
metrics.py

Compute Metrics from History

Author : yyJ

Version : 1.0
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

from models import Metrics


logger = logging.getLogger(__name__)


class MetricsCalculator:
    """
    根据 History DataFrame

    自动计算所有统计指标
    """

    def __init__(self):

        pass

    # ---------------------------------

    def calculate(
        self,
        history: pd.DataFrame
    ) -> Metrics:

        metrics = Metrics()

        if history is None:

            return metrics

        if history.empty:

            return metrics

        reward = self.find_reward(history)

        loss = self.find_loss(history)

        runtime = self.find_runtime(history)

        if reward is not None:

            self.compute_reward(
                reward,
                metrics
            )

        if loss is not None:

            self.compute_loss(
                loss,
                metrics
            )

        if runtime is not None:

            metrics.runtime = runtime

        return metrics
    
    @staticmethod
    def find_reward(
        history: pd.DataFrame
    ) -> Optional[pd.Series]:

        candidates = [

            "train/episode_reward",

            "episode_reward",

            "reward",

            "Reward",

            "returns",

            "episode_return",

            "test/episode_reward",

            "eval/reward"

        ]

        for col in candidates:

            if col in history.columns:

                logger.info(
                    f"Reward Column : {col}"
                )

                return history[col]

        logger.warning(
            "Reward column not found."
        )

        return None
    
    @staticmethod
    def find_loss(
        history: pd.DataFrame
    ) -> Optional[pd.Series]:

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

                logger.info(
                    f"Loss Column : {col}"
                )

                return history[col]

        return None
    
    
    @staticmethod
    def find_runtime(
        history: pd.DataFrame
    ) -> Optional[float]:

        if "_runtime" in history.columns:

            return float(
                history["_runtime"].iloc[-1]
            )

        return None
    
    
    @staticmethod
    def compute_reward(
        reward: pd.Series,
        metrics: Metrics
    ):

        reward = reward.dropna()

        if len(reward) == 0:

            return

        metrics.final_reward = float(
            reward.iloc[-1]
        )

        metrics.best_reward = float(
            reward.max()
        )

        metrics.worst_reward = float(
            reward.min()
        )

        metrics.mean_reward = float(
            reward.mean()
        )

        metrics.median_reward = float(
            reward.median()
        )

        metrics.std_reward = float(
            reward.std()
        )

        metrics.reward_variance = float(
            reward.var()
        )

        metrics.auc_reward = float(
            np.trapz(reward.to_numpy())
        )

        metrics.total_steps = len(reward)
        
        self.compute_convergence(
            reward,
            metrics
        )

        self.compute_statistics(
            reward,
            metrics
        )
        self.compute_advanced_metrics(
            reward,
            metrics
            )
        
    
    @staticmethod
    def ema(
        reward: pd.Series,
        span: int = 20
    ) -> pd.Series:

        return reward.ewm(
            span=span,
            adjust=False
        ).mean()
        
        
    def compute_convergence(
        self,
        reward: pd.Series,
        metrics: Metrics
    ):

        target = metrics.best_reward * 0.95

        metrics.convergence_threshold = target

        index = reward[reward >= target]

        if len(index) == 0:

            return

        metrics.convergence_step = int(index.index[0])
        

    def compute_statistics(
        self,
        reward: pd.Series,
        metrics: Metrics
    ):

        reward = reward.dropna()

        if len(reward) == 0:

            return

        # ------------------------
        # Moving Average
        # ------------------------

        ma = self.moving_average(reward)

        metrics.moving_average_reward = float(
            ma.iloc[-1]
        )

        # ------------------------
        # EMA
        # ------------------------

        ema = self.ema(reward)

        metrics.ema_reward = float(
            ema.iloc[-1]
        )

        # ------------------------
        # CV
        # ------------------------

        mean = reward.mean()

        if mean != 0:

            metrics.reward_cv = float(
                reward.std() / mean
            )

        # ------------------------
        # Stability
        # ------------------------

        metrics.stability_score = float(
            1.0 / (1.0 + reward.std())
        )

        # ------------------------
        # Sample Efficiency
        # ------------------------

        metrics.sample_efficiency = float(
            metrics.best_reward /
            len(reward)
        )

        # ------------------------
        # 95% CI
        # ------------------------

        std = reward.std()

        n = len(reward)

        ci = 1.96 * std / np.sqrt(n)

        metrics.reward_ci95_low = float(
            mean - ci
        )

        metrics.reward_ci95_high = float(
            mean + ci
        )


def compute_advanced_metrics(
    self,
    reward: pd.Series,
    metrics: Metrics,
    window: int = 100
):

    reward = reward.dropna()

    if reward.empty:
        return

    # ---------- Last N ----------
    tail = reward.tail(min(window, len(reward)))

    metrics.last100_mean_reward = float(
        tail.mean()
    )

    metrics.last100_std_reward = float(
        tail.std()
    )

    # ---------- Peak ----------
    metrics.peak_reward = float(
        reward.max()
    )

    metrics.peak_step = int(
        reward.idxmax()
    )

    # ---------- Oscillation ----------
    metrics.reward_oscillation = float(
        tail.std()
    )

    # ---------- Reward Slope ----------
    if len(tail) > 1:

        x = np.arange(len(tail))

        slope = np.polyfit(
            x,
            tail.to_numpy(),
            1
        )[0]

        metrics.reward_slope = float(
            slope
        )

    # ---------- Plateau ----------
    if (
        metrics.reward_slope < 0.01
        and metrics.reward_oscillation < 5
    ):
        metrics.plateau = True


def stability_score(
    self,
    reward: pd.Series
):

    reward = reward.dropna()

    if reward.empty:

        return np.nan

    tail = reward.tail(
        min(100, len(reward))
    )

    mean = tail.mean()

    std = tail.std()

    if mean == 0:

        return np.nan

    return float(

        100 / (1 + std / abs(mean))

    )
    
    metrics.stability_score = self.stability_score(
    reward
    )
    
def learning_efficiency(
    self,
    reward: pd.Series
):

    reward = reward.dropna()

    if reward.empty:

        return np.nan

    auc = np.trapz(
        reward.to_numpy()
    )

    return float(

        auc / len(reward)

    )
    
def overall_score(
    self,
    metrics: Metrics
):

    score = 0

    score += metrics.last100_mean_reward * 0.45

    score += metrics.stability_score * 0.25

    score += metrics.sample_efficiency * 0.20

    score += (
        100
        if metrics.plateau
        else 60
    ) * 0.10

    return float(score)


    # ==========================
    # Curve Analysis
    # ==========================

    moving_average_reward: float = np.nan

    ema_reward: float = np.nan

    stability_score: float = np.nan

    sample_efficiency: float = np.nan

    reward_cv: float = np.nan

    reward_ci95_low: float = np.nan

    reward_ci95_high: float = np.nan
    
    convergence_threshold: float = np.nan