# import logging
# from typing import Optional

# import numpy as np
# import pandas as pd

# from drl_analyzer.models import Metrics

# logger = logging.getLogger(__name__)

"""
metrics.py

Calculate metrics from WandB History DataFrame.

Supported Frameworks
--------------------
- Xuance
- Stable-Baselines3
- CleanRL
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

from drl_analyzer.models import Metrics

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """
    Calculate all metrics from a training history.
    """

    # =====================================================
    # Main Entrance
    # =====================================================

    def calculate(
        self,
        history: Optional[pd.DataFrame]
    ) -> Metrics:

        metrics = Metrics()

        if history is None:
            logger.warning("History is None.")
            return metrics

        if history.empty:
            logger.warning("History is empty.")
            return metrics

        reward = self.extract_reward(history)
        loss = self.extract_loss(history)
        runtime = self.extract_runtime(history)

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

    # =====================================================
    # Reward
    # =====================================================

    def extract_reward(
        self,
        history: pd.DataFrame
    ) -> Optional[pd.Series]:

        # -----------------------------
        # Xuance
        # -----------------------------
        
        # -----------------------------
        # Xuance Test Reward
        # -----------------------------

        test_columns = [

            c

            for c in history.columns

            if "Test-Episode-Rewards" in c

        ]


        if len(test_columns) > 0:

            logger.info(
                "Xuance test reward detected."
            )

            return history[test_columns[0]]
        
        # -----------------------------
        # Xuance Train Reward
        # -----------------------------

        
        xuance_columns = [

            c

            for c in history.columns

            if "Train-Episode-Rewards" in c

        ]

        if len(xuance_columns) > 0:

            logger.info(
                "Xuance reward detected."
            )

            reward = history[
                xuance_columns
            ].mean(axis=1)

            return reward

        # -----------------------------
        # Stable-Baselines3
        # -----------------------------

        sb3_columns = [

            "rollout/ep_rew_mean"

        ]

        for col in sb3_columns:

            if col in history.columns:

                logger.info(
                    f"Reward : {col}"
                )

                return history[col]

        # -----------------------------
        # CleanRL
        # -----------------------------

        cleanrl_columns = [

            "charts/episodic_return"

        ]

        for col in cleanrl_columns:

            if col in history.columns:

                logger.info(
                    f"Reward : {col}"
                )

                return history[col]

        # -----------------------------
        # Generic
        # -----------------------------

        candidates = [

            "reward",

            "Reward",

            "episode_reward",

            "episode_return",

            "returns",

            "train/episode_reward",

            "test/episode_reward",

            "eval/reward"

        ]

        for col in candidates:

            if col in history.columns:

                logger.info(
                    f"Reward : {col}"
                )

                return history[col]

        logger.warning(
            "Reward column not found."
        )

        return None

    # =====================================================
    # Loss
    # =====================================================

    def extract_loss(
        self,
        history: pd.DataFrame
    ) -> Optional[pd.Series]:

        candidates = [

            "loss",

            "Loss",

            "train/loss",

            "critic-loss",

            "actor-loss",

            "critic_loss",

            "actor_loss",

            "q_loss"

        ]

        for col in candidates:

            if col in history.columns:

                logger.info(
                    f"Loss : {col}"
                )

                return history[col]

        logger.info(
            "Loss column not found."
        )

        return None

    # =====================================================
    # Runtime
    # =====================================================

    def extract_runtime(
        self,
        history: pd.DataFrame
    ) -> Optional[float]:

        if "_runtime" in history.columns:

            return float(

                history["_runtime"].iloc[-1]

            )

        return None

    # =====================================================
    # Reward Metrics
    # =====================================================

    def compute_reward(
        self,
        reward: pd.Series,
        metrics: Metrics
    ):

        reward = reward.dropna()

        if reward.empty:

            return

        reward = reward.astype(float)

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

            np.trapz(
                reward.to_numpy()
            )

        )

        metrics.total_steps = len(reward)

        # More statistics

        self.compute_statistics(

            reward,
            metrics

        )

        self.compute_convergence(

            reward,
            metrics

        )

        self.compute_advanced_metrics(

            reward,
            metrics

        )

    # =====================================================
    # Loss Metrics
    # =====================================================

    def compute_loss(
        self,
        loss: pd.Series,
        metrics: Metrics
    ):

        loss = loss.dropna()

        if loss.empty:

            return

        loss = loss.astype(float)

        metrics.final_loss = float(

            loss.iloc[-1]

        )

        metrics.mean_loss = float(

            loss.mean()

        )
    # =====================================================
    # Statistics
    # =====================================================

    def compute_statistics(
        self,
        reward: pd.Series,
        metrics: Metrics
    ):

        reward = reward.dropna()

        if reward.empty:
            return

        # Moving Average
        ma = self.moving_average(reward)

        metrics.moving_average_reward = float(
            ma.iloc[-1]
        )

        # EMA
        ema = self.ema(reward)

        metrics.ema_reward = float(
            ema.iloc[-1]
        )

        mean = reward.mean()

        std = reward.std()

        # Coefficient of Variation
        if mean != 0:

            metrics.reward_cv = float(
                std / abs(mean)
            )

        # Stability Score
        metrics.stability_score = self.stability_score(
            reward
        )

        # Sample Efficiency
        metrics.sample_efficiency = float(
            metrics.best_reward /
            len(reward)
        )

        # Learning Efficiency
        metrics.learning_efficiency = self.learning_efficiency(
            reward
        )

        # 95% Confidence Interval
        ci = 1.96 * std / np.sqrt(len(reward))

        metrics.reward_ci95_low = float(
            mean - ci
        )

        metrics.reward_ci95_high = float(
            mean + ci
        )

    # =====================================================
    # Convergence
    # =====================================================

    def compute_convergence(
        self,
        reward: pd.Series,
        metrics: Metrics
    ):

        if reward.empty:
            return

        target = metrics.best_reward * 0.95

        metrics.convergence_threshold = float(
            target
        )

        idx = reward[reward >= target]

        if len(idx) > 0:

            metrics.convergence_step = int(
                idx.index[0]
            )

    # =====================================================
    # Advanced Metrics
    # =====================================================

    def compute_advanced_metrics(
        self,
        reward: pd.Series,
        metrics: Metrics,
        window: int = 100
    ):

        reward = reward.dropna()

        if reward.empty:
            return

        tail = reward.tail(
            min(window, len(reward))
        )

        metrics.last100_mean_reward = float(
            tail.mean()
        )

        metrics.last100_std_reward = float(
            tail.std()
        )

        metrics.peak_reward = float(
            reward.max()
        )

        metrics.peak_step = int(
            reward.idxmax()
        )

        metrics.reward_oscillation = float(
            tail.std()
        )

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

        metrics.plateau = bool(

            metrics.reward_slope < 0.01

            and

            metrics.reward_oscillation < 5

        )

        metrics.overall_score = self.overall_score(
            metrics
        )

    # =====================================================
    # Helper Functions
    # =====================================================

    @staticmethod
    def moving_average(
        reward: pd.Series,
        window: int = 20
    ) -> pd.Series:

        return reward.rolling(
            window=window,
            min_periods=1
        ).mean()

    @staticmethod
    def ema(
        reward: pd.Series,
        span: int = 20
    ) -> pd.Series:

        return reward.ewm(
            span=span,
            adjust=False
        ).mean()

    @staticmethod
    def stability_score(
        reward: pd.Series
    ) -> float:

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

            100.0 /

            (1.0 + std / abs(mean))

        )

    @staticmethod
    def learning_efficiency(
        reward: pd.Series
    ) -> float:

        reward = reward.dropna()

        if reward.empty:
            return np.nan

        auc = np.trapz(
            reward.to_numpy()
        )

        return float(

            auc /

            len(reward)

        )

    @staticmethod
    def overall_score(
        metrics: Metrics
    ) -> float:

        score = 0.0

        if not np.isnan(metrics.last100_mean_reward):

            score += (
                metrics.last100_mean_reward
                * 0.45
            )

        if not np.isnan(metrics.stability_score):

            score += (
                metrics.stability_score
                * 0.25
            )

        if not np.isnan(metrics.sample_efficiency):

            score += (
                metrics.sample_efficiency
                * 0.20
            )

        score += (

            100

            if metrics.plateau

            else 60

        ) * 0.10

        return float(score)