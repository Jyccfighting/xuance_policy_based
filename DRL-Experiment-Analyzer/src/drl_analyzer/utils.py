"""
utils.py

通用工具函数：目录/文件、JSON/YAML/CSV、数值平滑、时间格式化。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


def ensure_dir(path: Path) -> Path:
    """创建目录（递归），已存在则忽略，返回该目录。"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_file(directory: Path, filename: str) -> Path | None:
    """在 directory 下递归查找第一个名为 filename 的文件。"""
    for file in directory.rglob(filename):
        return file
    return None


def load_json(path: Path) -> dict[str, Any]:
    """读取 UTF-8 JSON 文件。"""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict[str, Any], path: Path) -> None:
    """保存 JSON 文件（自动创建父目录）。"""
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_yaml(path: Path) -> dict[str, Any]:
    """读取 YAML 文件，空文件返回空字典。"""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_csv(path: Path) -> pd.DataFrame:
    """读取 CSV 文件。"""
    return pd.read_csv(path)


def moving_average(values, window: int = 100) -> np.ndarray:
    """简单滑动平均；窗口大于数据长度时原样返回。"""
    values = np.asarray(values, dtype=float)
    if len(values) < window:
        return values
    return np.convolve(values, np.ones(window) / window, mode="valid")


def exponential_moving_average(values, alpha: float = 0.1) -> np.ndarray:
    """指数滑动平均（EWMA）。"""
    values = np.asarray(values, dtype=float)
    ema = np.zeros_like(values)
    ema[0] = values[0]
    for i in range(1, len(values)):
        ema[i] = alpha * values[i] + (1 - alpha) * ema[i - 1]
    return ema


def format_seconds(seconds: float) -> str:
    """把秒格式化为 hh:mm:ss。"""
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"