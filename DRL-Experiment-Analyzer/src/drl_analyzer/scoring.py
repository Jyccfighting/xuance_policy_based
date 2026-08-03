"""
scoring.py

公共评分/归一化工具：leaderboard、report、summary_plot 全部从这里取归一化与加权逻辑，
避免多套实现方向不一致。
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# 指标方向：True = 越大越好，False = 越小越好
METRIC_DIRECTIONS = {
    "final_reward": True,
    "stability": True,
    "sample_efficiency": False,  # 达到收敛所需步数，越小越好
    "runtime": False,
}

# 综合分权重（和为 1）
DEFAULT_WEIGHTS = {
    "final_reward": 0.4,
    "runtime": 0.2,
    "stability": 0.2,
    "sample_efficiency": 0.2,
}


def normalize(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """
    min-max 归一化到 [0, 1]。

    参数
    ----
    series : pd.Series
    higher_is_better : bool
        True 表示值越大得分越高，False 表示越小越高。

    返回
    ----
    pd.Series
        全 NaN 或常数列返回 0.5，避免除零。
    """
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0:
        return s.fillna(0.5)
    vmin = s.min()
    vmax = s.max()
    if np.isclose(vmax - vmin, 0.0):
        return s.fillna(0.5)
    normalized = (s - vmin) / (vmax - vmin)
    if not higher_is_better:
        normalized = 1.0 - normalized
    return normalized


def weighted_score(df: pd.DataFrame, weights: dict | None = None) -> pd.Series:
    """
    按权重计算综合分（0-1）。

    参数
    ----
    df : pd.DataFrame
        应包含 final_reward/runtime/stability/sample_efficiency 等列。
    weights : dict | None
        默认使用 DEFAULT_WEIGHTS。
    """
    weights = weights or DEFAULT_WEIGHTS
    total = pd.Series(0.0, index=df.index)
    weight_sum = 0.0
    for col, w in weights.items():
        if col not in df.columns:
            continue
        direction = METRIC_DIRECTIONS.get(col, True)
        normalized = normalize(df[col], higher_is_better=direction)
        total = total + normalized.fillna(0.0) * w
        weight_sum += w
    return total / weight_sum if weight_sum > 0 else total


def compute_leaderboard(df: pd.DataFrame, weights: dict | None = None) -> pd.DataFrame:
    """
    按算法聚合四个指标，计算归一化综合分并排序。

    参数
    ----
    df : pd.DataFrame
        benchmark 数据（建议只传 status == ok 的行）。
    weights : dict | None

    返回
    ----
    pd.DataFrame
        含 Rank / overall_score 的算法排行榜。
    """
    if df.empty:
        return pd.DataFrame(columns=["Rank", "algorithm", "overall_score"])

    score = df.groupby("algorithm").agg({
        "final_reward": "mean",
        "runtime": "mean",
        "stability": "mean",
        "sample_efficiency": "mean",
    })
    score["overall_score"] = weighted_score(score, weights)
    score = score.sort_values("overall_score", ascending=False)
    score.insert(0, "Rank", range(1, len(score) + 1))
    return score