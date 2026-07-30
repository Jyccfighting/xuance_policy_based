"""
utils.py

公共工具函数模块。

功能：
- 文件/目录操作
- JSON/YAML/CSV 读取
- 数值处理
- 时间格式化
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml


# =============================================================================
# File Utilities
# =============================================================================

def ensure_dir(path: Path) -> Path:
    """
    Create directory if it does not exist.

    Parameters
    ----------
    path : Path

    Returns
    -------
    Path
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def find_file(directory: Path, filename: str) -> Path | None:
    """
    Recursively search for a file.

    Parameters
    ----------
    directory : Path
    filename : str

    Returns
    -------
    Path | None
    """
    for file in directory.rglob(filename):
        return file
    return None


# =============================================================================
# JSON Utilities
# =============================================================================

def load_json(path: Path) -> dict[str, Any]:
    """
    Load JSON file.

    Parameters
    ----------
    path : Path

    Returns
    -------
    dict
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict[str, Any], path: Path) -> None:
    """
    Save dictionary to JSON.
    """
    ensure_dir(path.parent)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =============================================================================
# YAML Utilities
# =============================================================================

def load_yaml(path: Path) -> dict[str, Any]:
    """
    Load YAML file.
    """
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# =============================================================================
# CSV Utilities
# =============================================================================

def load_csv(path: Path) -> pd.DataFrame:
    """
    Load CSV file.

    Returns
    -------
    pandas.DataFrame
    """
    return pd.read_csv(path)


# =============================================================================
# Numeric Utilities
# =============================================================================

# def moving_average(values, window: int = 100) -> np.ndarray:
#     """
#     Calculate moving average.

#     Parameters
#     ----------
#     values
#     window

#     Returns
#     -------
#     ndarray
#     """
#     values = np.asarray(values, dtype=float)

#     if len(values) < window:
#         return values

#     kernel = np.ones(window) / window

#     return np.convolve(values, kernel, mode="same")

def moving_average(values, window: int = 100):
    """
    Calculate moving average.
    """

    values = np.asarray(values, dtype=float)

    if len(values) < window:
        return values

    result = np.convolve(
        values,
        np.ones(window) / window,
        mode="valid"
    )

    return result


def exponential_moving_average(values, alpha: float = 0.1) -> np.ndarray:
    """
    Calculate exponential moving average.
    """
    values = np.asarray(values, dtype=float)

    ema = np.zeros_like(values)

    ema[0] = values[0]

    for i in range(1, len(values)):
        ema[i] = alpha * values[i] + (1 - alpha) * ema[i - 1]

    return ema


# =============================================================================
# Time Utilities
# =============================================================================

def format_seconds(seconds: float) -> str:
    """
    Convert seconds to hh:mm:ss.

    Example
    -------
    3661 -> 01:01:01
    """
    seconds = int(seconds)

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02d}:{m:02d}:{s:02d}"