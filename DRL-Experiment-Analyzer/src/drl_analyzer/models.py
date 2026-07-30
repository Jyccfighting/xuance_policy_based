# """
# models.py
# """

# from dataclasses import dataclass, field
# from pathlib import Path
# from typing import Dict, Any
# import numpy as np


# @dataclass
# class Experiment:

#     # ------------------------
#     # 基本信息
#     # ------------------------

#     algorithm: str

#     environment: str

#     run_name: str

#     run_path: Path

#     config_path: Path

#     summary_path: Path

#     wandb_file: Path

#     # ------------------------
#     # 解析后的数据
#     # ------------------------

#     config: Dict[str, Any] = field(default_factory=dict)

#     summary: Dict[str, Any] = field(default_factory=dict)

#     metrics: Dict[str, Any] = field(default_factory=dict)

#     # ------------------------

#     def get(self, key, default=None):

#         if key in self.metrics:
#             return self.metrics[key]

#         if key in self.summary:
#             return self.summary[key]

#         if key in self.config:
#             return self.config[key]

#         return default


# @dataclass
# class Metrics:
#     """
#     保存一个实验计算出来的统计指标
#     """

#     # ==========================
#     # Reward
#     # ==========================
#     final_reward: float = np.nan
#     best_reward: float = np.nan
#     worst_reward: float = np.nan

#     mean_reward: float = np.nan
#     median_reward: float = np.nan
#     std_reward: float = np.nan

#     reward_variance: float = np.nan

#     # ==========================
#     # Loss
#     # ==========================
#     final_loss: float = np.nan
#     best_loss: float = np.nan
#     mean_loss: float = np.nan
#     std_loss: float = np.nan

#     # ==========================
#     # Runtime
#     # ==========================
#     runtime: float = np.nan

#     fps: float = np.nan

#     # ==========================
#     # Training
#     # ==========================
#     convergence_step: float = np.nan

#     auc_reward: float = np.nan

#     total_steps: float = np.nan

#     total_episode: float = np.nan
    
#     # ==========================
#     # Advanced Reward Metrics
#     # ==========================

#     last100_mean_reward: float = np.nan
#     last100_std_reward: float = np.nan

#     peak_reward: float = np.nan
#     peak_step: int = -1

#     reward_slope: float = np.nan

#     reward_oscillation: float = np.nan

#     plateau: bool = False
    
#     history_csv_path: Path | None = None

#     history: pd.DataFrame | None = None
    


# """
# models.py

# Data models used by DRL Experiment Analyzer.

# Author : yyJ
# Version : 1.0
# """

# from __future__ import annotations

# from dataclasses import dataclass, field
# from pathlib import Path

# import numpy as np
# import pandas as pd


# # ==========================================================
# # Metrics
# # ==========================================================

# @dataclass
# class Metrics:
#     """
#     Statistics calculated from one experiment.
#     """

#     # Reward
#     final_reward: float = np.nan
#     best_reward: float = np.nan
#     worst_reward: float = np.nan

#     mean_reward: float = np.nan
#     median_reward: float = np.nan
#     std_reward: float = np.nan
#     reward_variance: float = np.nan

#     # Loss
#     final_loss: float = np.nan
#     best_loss: float = np.nan
#     mean_loss: float = np.nan
#     std_loss: float = np.nan

#     # Runtime
#     runtime: float = np.nan
#     fps: float = np.nan

#     # Training
#     total_steps: int = 0
#     total_episode: int = 0

#     auc_reward: float = np.nan

#     convergence_step: float = np.nan
#     convergence_threshold: float = np.nan

#     # Curve Statistics
#     moving_average_reward: float = np.nan
#     ema_reward: float = np.nan

#     reward_cv: float = np.nan

#     stability_score: float = np.nan

#     sample_efficiency: float = np.nan

#     reward_ci95_low: float = np.nan
#     reward_ci95_high: float = np.nan

#     # Advanced Metrics
#     last100_mean_reward: float = np.nan
#     last100_std_reward: float = np.nan

#     peak_reward: float = np.nan
#     peak_step: int = -1

#     reward_slope: float = np.nan

#     reward_oscillation: float = np.nan

#     plateau: bool = False

#     overall_score: float = np.nan


# # ==========================================================
# # Experiment
# # ==========================================================

# @dataclass
# class Experiment:
#     """
#     Represents one training run.
#     """

#     # File Paths
#     root_dir: Path

#     config_path: Path | None = None

#     summary_path: Path | None = None

#     history_csv_path: Path | None = None

#     # Basic Information

#     algorithm: str = ""

#     environment: str = ""

#     project: str = ""

#     run_name: str = ""

#     seed: int = -1

#     # Parsed Data

#     config: dict = field(default_factory=dict)

#     summary: dict = field(default_factory=dict)

#     history: pd.DataFrame | None = None

#     metrics: Metrics = field(default_factory=Metrics)

#     # --------------------------------------------------

#     def has_history(self) -> bool:

#         return self.history is not None

#     # --------------------------------------------------

#     def has_summary(self) -> bool:

#         return len(self.summary) > 0

#     # --------------------------------------------------

#     def has_config(self) -> bool:

#         return len(self.config) > 0

#     # --------------------------------------------------

#     def __str__(self):

#         return (
#             f"{self.algorithm} | "
#             f"{self.environment} | "
#             f"{self.run_name}"
#         )




"""
models.py

Data models for DRL experiment analysis.

Contains:
- Experiment
- TrainingHistory
- Metrics
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
import numpy as np


# ============================================================
# Metrics
# ============================================================

@dataclass
class Metrics:
    """
    All calculated metrics of one experiment.
    """

    # =====================================================
    # Reward
    # =====================================================

    final_reward: float = np.nan

    best_reward: float = np.nan

    worst_reward: float = np.nan

    mean_reward: float = np.nan

    median_reward: float = np.nan

    std_reward: float = np.nan

    reward_variance: float = np.nan

    auc_reward: float = np.nan

    # =====================================================
    # Loss
    # =====================================================

    final_loss: float = np.nan

    mean_loss: float = np.nan

    # =====================================================
    # Runtime
    # =====================================================

    runtime: float = np.nan

    total_steps: int = 0

    episodes: int = 0

    # =====================================================
    # Curve Statistics
    # =====================================================

    moving_average_reward: float = np.nan

    ema_reward: float = np.nan

    reward_cv: float = np.nan

    reward_ci95_low: float = np.nan

    reward_ci95_high: float = np.nan

    # =====================================================
    # Convergence
    # =====================================================

    convergence_step: int = -1

    convergence_threshold: float = np.nan

    # =====================================================
    # Advanced Metrics
    # =====================================================

    last100_mean_reward: float = np.nan

    last100_std_reward: float = np.nan

    peak_reward: float = np.nan

    peak_step: int = -1

    reward_slope: float = np.nan

    reward_oscillation: float = np.nan

    stability_score: float = np.nan

    learning_efficiency: float = np.nan
    
    sample_efficiency: float = None

    overall_score: float = np.nan

    plateau: bool = False
    
    # =====================================================
    # 新增
    # =====================================================
    
    best_step: int = 0

    convergence_step: int = 0
    
    convergence_step: int = None

    convergence_threshold: float = None

    success_rate: float = None

    # =====================================================
    # Export
    # =====================================================

    def to_dict(self):

        return self.__dict__.copy()

# ============================================================
# Training History
# ============================================================

@dataclass
class TrainingHistory:
    """
    Training history data.

    Usually loaded from:
    - WandB history.csv
    - TensorBoard
    - CSV
    """

    dataframe: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )


# ============================================================
# Experiment
# ============================================================

@dataclass
class Experiment:
    """
    One DRL experiment.

    Example:

    C51 + CartPole-v1
    """

    algorithm: str | None = None

    environment: str | None = None

    seed: int | None = None


    # experiment directory

    path: Path | None = None
    
    
    project_name: str | None = None
    
    history=None


    # configuration

    config: dict[str, Any] = field(
        default_factory=dict
    )


    # training data

    history: TrainingHistory | None = None


    # evaluation result

    metrics: Metrics = field(
        default_factory=Metrics
    )