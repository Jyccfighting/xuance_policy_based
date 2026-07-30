"""
models.py
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any


@dataclass
class Experiment:

    # ------------------------
    # 基本信息
    # ------------------------

    algorithm: str

    environment: str

    run_name: str

    run_path: Path

    config_path: Path

    summary_path: Path

    wandb_file: Path

    # ------------------------
    # 解析后的数据
    # ------------------------

    config: Dict[str, Any] = field(default_factory=dict)

    summary: Dict[str, Any] = field(default_factory=dict)

    metrics: Dict[str, Any] = field(default_factory=dict)

    # ------------------------

    def get(self, key, default=None):

        if key in self.metrics:
            return self.metrics[key]

        if key in self.summary:
            return self.summary[key]

        if key in self.config:
            return self.config[key]

        return default