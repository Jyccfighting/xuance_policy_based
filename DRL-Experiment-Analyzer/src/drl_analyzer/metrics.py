"""
metrics.py

从训练历史 DataFrame 计算统计指标。

支持列名：Xuance、Stable-Baselines3、CleanRL、通用 reward/loss。
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

from drl_analyzer.models import Metrics

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """计算一个实验的统计指标。"""

    # =====================================================
    # 主入口
    # =====================================================

    def calculate(self, history: Optional[pd.DataFrame]) -> Metrics:
        """
        主入口：输入历史，输出 Metrics。

        参数
        ----
        history : pd.DataFrame | None

        返回
        ----
        Metrics
        """
        metrics = Metrics()
        if history is None or history.empty:
            logger.warning("历史为空，跳过指标计算。")
            return metrics

        reward = self.extract_reward(history)
        loss = self.extract_loss(history)
        runtime = self.extract_runtime(history)

        metrics.episodes = len(reward) if reward is not None else 0
        metrics.total_steps = len(history)
        if runtime is not None:
            metrics.runtime = runtime

        if reward is not None:
            self.compute_reward(reward, metrics)
        if loss is not None:
            self.compute_loss(loss, metrics)
        return metrics

    # =====================================================
    # 列提取
    # =====================================================

    def extract_reward(self, history: pd.DataFrame) -> Optional[pd.Series]:
        """按框架优先级提取 reward 序列（去空、重建索引）。"""
        if history is None:
            return None

        # Xuance 测试奖励
        test_columns = [
            c for c in history.columns
            if "Test-Episode-Rewards/Mean-Score" in c
        ]
        if test_columns:
            logger.info("检测到 Xuance 测试奖励列: %s", test_columns[0])
            return history[test_columns[0]].dropna().reset_index(drop=True)

        # Xuance 训练奖励（多列求均值）
        train_columns = [
            c for c in history.columns
            if "Train-Episode-Rewards" in c
        ]
        if train_columns:
            logger.info("检测到 Xuance 训练奖励列: %s", train_columns[0])
            return history[train_columns].mean(axis=1).dropna().reset_index(drop=True)

        # Stable-Baselines3
        for col in ("rollout/ep_rew_mean", "episode_reward"):
            if col in history.columns:
                logger.info("检测到 SB3 奖励列: %s", col)
                return history[col].dropna().reset_index(drop=True)

        # CleanRL
        for col in ("charts/episodic_return", "charts/episode_return"):
            if col in history.columns:
                logger.info("检测到 CleanRL 奖励列: %s", col)
                return history[col].dropna().reset_index(drop=True)

        # 通用候选列
        for col in (
            "reward", "Reward", "episode_reward", "episode_return",
            "returns", "train/episode_reward", "test/episode_reward", "eval/reward",
        ):
            if col in history.columns:
                logger.info("检测到通用奖励列: %s", col)
                return history[col].dropna().reset_index(drop=True)

        logger.warning("未找到奖励列。")
        return None

    def extract_loss(self, history: pd.DataFrame) -> Optional[pd.Series]:
        """提取 loss 序列。"""
        if history is None:
            return None
        for col in (
            "loss", "Loss", "train/loss", "critic-loss", "actor-loss",
            "critic_loss", "actor_loss", "q_loss",
        ):
            if col in history.columns:
                return history[col]
        logger.info("未找到 loss 列。")
        return None

    def extract_runtime(self, history: pd.DataFrame) -> Optional[float]:
        """提取总运行时长（秒）。"""
        if history is None or "_runtime" not in history.columns:
            return None
        try:
            return float(history["_runtime"].iloc[-1])
        except Exception:
            return None

    # =====================================================
    # 指标计算
    # =====================================================

    def compute_reward(self, reward: pd.Series, metrics: Metrics) -> None:
        """计算 reward 基础统计。"""
        reward = reward.dropna().astype(float)
        if reward.empty:
            return

        metrics.final_reward = float(reward.iloc[-1])
        metrics.best_reward = float(reward.max())
        metrics.best_step = int(reward.idxmax())
        metrics.worst_reward = float(reward.min())
        metrics.mean_reward = float(reward.mean())
        metrics.median_reward = float(reward.median())
        metrics.std_reward = float(reward.std() if len(reward) > 1 else 0.0)
        metrics.reward_variance = float(reward.var() if len(reward) > 1 else 0.0)
        metrics.auc_reward = float(np.trapz(reward.to_numpy()))

        self.compute_statistics(reward, metrics)
        self.compute_convergence(reward, metrics)
        self.compute_sample_efficiency(metrics)
        self.compute_advanced_metrics(reward, metrics)

    def compute_loss(self, loss: pd.Series, metrics: Metrics) -> None:
        """计算 loss 统计。"""
        loss = loss.dropna().astype(float)
        if loss.empty:
            return
        metrics.final_loss = float(loss.iloc[-1])
        metrics.mean_loss = float(loss.mean())

    def compute_statistics(self, reward: pd.Series, metrics: Metrics) -> None:
        """计算滑动平均、EMA、变异系数、稳定性、置信区间等。"""
        reward = reward.dropna()
        if reward.empty:
            return

        ma = reward.rolling(window=20, min_periods=1).mean()
        metrics.moving_average_reward = float(ma.iloc[-1])

        ema = reward.ewm(span=20, adjust=False).mean()
        metrics.ema_reward = float(ema.iloc[-1])

        mean = reward.mean()
        std = reward.std() if len(reward) > 1 else 0.0
        if mean != 0:
            metrics.reward_cv = float(std / abs(mean))

        metrics.stability_score = self.stability_score(reward)
        metrics.learning_efficiency = float(np.trapz(reward.to_numpy()) / len(reward))

        ci = 1.96 * std / np.sqrt(len(reward))
        metrics.reward_ci95_low = float(mean - ci)
        metrics.reward_ci95_high = float(mean + ci)

    def compute_convergence(self, reward: pd.Series, metrics: Metrics) -> None:
        """计算收敛阈值与首次达到收敛的步数。"""
        if reward.empty:
            return
        best = float(reward.max())
        worst = float(reward.min())
        threshold = worst + 0.95 * (best - worst)
        metrics.convergence_threshold = float(threshold)

        reached = reward[reward >= threshold]
        metrics.convergence_step = int(reached.index[0]) if len(reached) > 0 else -1

    def compute_sample_efficiency(self, metrics: Metrics) -> None:
        """
        样本效率统一为“达到收敛所需的步数”，越小越好。

        未收敛（convergence_step=-1）或步数为 0 时置 NaN。
        """
        if metrics.convergence_step is None or metrics.convergence_step <= 0:
            metrics.sample_efficiency = np.nan
        else:
            metrics.sample_efficiency = float(metrics.convergence_step)

    def compute_advanced_metrics(
        self,
        reward: pd.Series,
        metrics: Metrics,
        window: int = 100,
    ) -> None:
        """计算尾部窗口指标、峰值、斜率、振荡与 plateau。"""
        reward = reward.dropna()
        if reward.empty:
            return

        tail = reward.tail(min(window, len(reward)))
        metrics.last100_mean_reward = float(tail.mean())
        metrics.last100_std_reward = float(tail.std() if len(tail) > 1 else 0.0)
        metrics.peak_reward = float(reward.max())
        metrics.peak_step = int(reward.idxmax())

        if len(tail) > 1:
            x = np.arange(len(tail))
            slope = np.polyfit(x, tail.to_numpy(), 1)[0]
            metrics.reward_slope = float(slope)
        else:
            metrics.reward_slope = 0.0

        # 相对振荡：标准差相对均值，避免不同量纲不可比
        tail_mean = abs(tail.mean())
        metrics.reward_oscillation = float(
            (tail.std() / tail_mean) if tail_mean > 1e-9 else 0.0
        )

        # plateau：尾部斜率接近 0 且相对振荡小
        span = float(reward.max() - reward.min())
        metrics.plateau = bool(
            len(tail) > 5
            and abs(metrics.reward_slope) < 0.01 * (span + 1e-9)
            and metrics.reward_oscillation < 0.05
        )

    # =====================================================
    # 工具方法
    # =====================================================

    @staticmethod
    def stability_score(reward: pd.Series) -> float:
        """稳定性得分：100 / (1 + 尾部 CV)，越大越稳定。"""
        reward = reward.dropna()
        if reward.empty:
            return np.nan
        tail = reward.tail(min(100, len(reward)))
        mean = tail.mean()
        std = tail.std() if len(tail) > 1 else 0.0
        if mean == 0:
            return np.nan
        return float(100.0 / (1.0 + std / abs(mean)))