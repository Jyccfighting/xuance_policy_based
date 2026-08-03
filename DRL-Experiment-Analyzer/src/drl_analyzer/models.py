"""
models.py

数据模型定义。

包含：
- Metrics：单个实验计算出的统计指标
- TrainingHistory：训练历史（DataFrame 的薄封装）
- Experiment：一个实验（路径、配置、历史、指标）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass
class Metrics:
    """单个实验的所有统计指标，默认 NaN / -1 表示“未计算”。"""

    # ---------------- Reward ----------------
    final_reward: float = np.nan
    best_reward: float = np.nan
    worst_reward: float = np.nan
    mean_reward: float = np.nan
    median_reward: float = np.nan
    std_reward: float = np.nan
    reward_variance: float = np.nan
    auc_reward: float = np.nan

    # ---------------- Loss ----------------
    final_loss: float = np.nan
    mean_loss: float = np.nan

    # ---------------- 规模 ----------------
    episodes: int = 0       # 有 reward 的 episode 数
    total_steps: int = 0    # history 中的训练步数

    # ---------------- 运行时 ----------------
    runtime: float = np.nan

    # ---------------- 曲线统计 ----------------
    moving_average_reward: float = np.nan
    ema_reward: float = np.nan
    reward_cv: float = np.nan
    reward_ci95_low: float = np.nan
    reward_ci95_high: float = np.nan

    # ---------------- 收敛 ----------------
    convergence_step: int = -1           # 首次达到收敛阈值的步数，-1 表示未收敛
    convergence_threshold: float = np.nan

    # ---------------- 高级指标 ----------------
    last100_mean_reward: float = np.nan
    last100_std_reward: float = np.nan
    peak_reward: float = np.nan
    peak_step: int = -1
    best_step: int = -1
    reward_slope: float = np.nan
    reward_oscillation: float = np.nan
    stability_score: float = np.nan
    learning_efficiency: float = np.nan
    sample_efficiency: float = np.nan    # 达到收敛所需步数，越小越好
    plateau: bool = False
    success_rate: float = np.nan

    # 综合分由 scoring.compute_leaderboard 在全体实验层面计算，
    # 单实验内保持 NaN，避免不同环境直接比较。
    overall_score: float = np.nan

    def to_dict(self) -> dict[str, Any]:
        """导出为普通字典（用于 CSV/Excel）。"""
        return self.__dict__.copy()


@dataclass
class TrainingHistory:
    """训练历史数据（通常来自 history.csv / WandB API / 本地 .wandb）。"""

    dataframe: pd.DataFrame = field(default_factory=pd.DataFrame)


@dataclass
class Experiment:
    """一个 DRL 实验（对应一个 WandB run 目录）。"""

    algorithm: str | None = None
    environment: str | None = None
    seed: int | None = None

    path: Path | None = None              # run 目录
    project_name: str | None = None
    run_name: str | None = None

    # 本地数据源（由 scanner 填充）
    config_path: Path | None = None
    summary_path: Path | None = None
    history_csv_path: Path | None = None  # files/history.csv 缓存
    wandb_file: Path | None = None        # run-*.wandb 本地过程文件

    # 解析后的数据
    config: dict[str, Any] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)
    history: pd.DataFrame | None = None
    metrics: Metrics = field(default_factory=Metrics)

    @property
    def has_history(self) -> bool:
        """是否已加载过程历史。"""
        return self.history is not None and not self.history.empty

    def __str__(self) -> str:
        return f"{self.algorithm or '?'} | {self.environment or '?'} | {self.run_name or '?'}"