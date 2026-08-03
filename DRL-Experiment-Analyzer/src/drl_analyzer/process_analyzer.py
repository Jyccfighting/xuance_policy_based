"""
process_analyzer.py

过程分析：逐 step 曲线、突变/异常检测、失败事件提取。
用于回答“训练到哪一步突然变化 / 为什么失败”。
"""

from __future__ import annotations

import logging
import re
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def analyze_process(
    history: pd.DataFrame,
    reward_col: str | None = None,
    loss_col: str | None = None,
    window: int = 10,
    z_threshold: float = 2.0,
) -> dict[str, Any]:
    """
    分析训练过程，返回异常事件字典。

    参数
    ----
    history : pd.DataFrame
        训练历史。
    reward_col / loss_col : str | None
        指定列名；None 时自动猜测。
    window : int
        突变检测的滑动窗口大小。
    z_threshold : float
        判定突变的 z-score 阈值（默认 2.0，对阶跃/尖峰更敏感）。
    """
    if history is None or history.empty:
        return {"steps": 0, "events": [], "nan_columns": {}}

    reward_col = reward_col or _guess_reward_column(history)
    loss_col = loss_col or _guess_loss_column(history)
    events = []

    # 1. NaN 统计
    nan_columns = {
        col: int(history[col].isna().sum())
        for col in (reward_col, loss_col)
        if col is not None and col in history.columns
    }

    # 2. 突变点检测
    if reward_col in history.columns:
        events.extend(_detect_change_points(history[reward_col], "reward", window, z_threshold))
    if loss_col in history.columns:
        events.extend(_detect_change_points(history[loss_col], "loss", window, z_threshold))

    # 3. NaN / Inf 首次出现位置
    for col in (reward_col, loss_col):
        if col is None or col not in history.columns:
            continue
        numeric = pd.to_numeric(history[col], errors="coerce")
        bad = history[col].isna() | numeric.isna() | np.isinf(numeric)
        # 稀疏记录列（如测试奖励只在固定 step 记录）不算异常
        if bad.any() and bad.mean() < 0.9:
            step = int(bad.idxmax())
            events.append({
                "type": "nan_or_inf",
                "column": col,
                "step": step,
                "message": f"{col} 在 step {step} 首次出现 NaN/Inf",
            })

    # 4. 最佳 reward 之后回退
    if reward_col in history.columns:
        reward = pd.to_numeric(history[reward_col], errors="coerce").dropna()
        if len(reward) > window * 2:
            best_step = int(reward.idxmax())
            after = reward.iloc[best_step:]
            if len(after) > window:
                before_mean = reward.iloc[max(0, best_step - window):best_step].mean()
                after_mean = after.mean()
                if before_mean > 0 and after_mean < before_mean * 0.8:
                    events.append({
                        "type": "reward_regression",
                        "step": best_step,
                        "message": (
                            f"最佳 reward 之后明显回退 "
                            f"(best窗口均值={before_mean:.3f}, 之后均值={after_mean:.3f})"
                        ),
                    })

    return {
        "steps": len(history),
        "reward_column": reward_col,
        "loss_column": loss_col,
        "nan_columns": nan_columns,
        "events": _dedup_events(events),
    }


def extract_events(output_log: str) -> list[dict[str, Any]]:
    """
    从 output.log 文本中提取事件（error / Traceback / Best Model Score / Epoch）。

    参数
    ----
    output_log : str
        日志文本。
    """
    events = []
    lines = output_log.splitlines()
    for i, line in enumerate(lines):
        low = line.lower()
        if "error" in low or "traceback" in low or "exception" in low:
            events.append({"type": "error", "line": i + 1, "message": line.strip()[:200]})
        elif re.search(r"best model score", low):
            events.append({"type": "best_model", "line": i + 1, "message": line.strip()[:200]})
        elif re.match(r"^\s*epoch\s*[:：]", low):
            events.append({"type": "epoch", "line": i + 1, "message": line.strip()[:200]})
    return events


def build_process_report(experiment, analysis: dict[str, Any]) -> str:
    """把过程分析结果格式化成 Markdown 片段。"""
    lines = [
        f"## 过程分析：{experiment.run_name or ''}",
        "",
        f"- 历史步数: {analysis['steps']}",
        f"- reward 列: {analysis['reward_column']}",
        f"- loss 列: {analysis['loss_column']}",
        f"- NaN 统计: {analysis['nan_columns']}",
        "",
        "### 异常事件",
    ]
    if analysis["events"]:
        for e in analysis["events"]:
            lines.append(f"- `{e['type']}` @ step {e.get('step', '?')}: {e['message']}")
    else:
        lines.append("- 未检测到明显异常。")
    return "\n".join(lines)


def _guess_reward_column(history: pd.DataFrame) -> str | None:
    """自动猜测 reward 列。"""
    for col in ("rollout/ep_rew_mean", "charts/episodic_return", "reward", "episode_reward"):
        if col in history.columns:
            return col
    for col in history.columns:
        if "Rewards" in col or "reward" in col.lower():
            return col
    return None


def _guess_loss_column(history: pd.DataFrame) -> str | None:
    """自动猜测 loss 列。"""
    for col in ("loss", "train/loss", "critic_loss", "actor_loss", "q_loss"):
        if col in history.columns:
            return col
    for col in history.columns:
        if "loss" in col.lower():
            return col
    return None


def _detect_change_points(series, name, window, z_threshold):
    """
    用滑动平均的一阶差分做 z-score 突变检测。

    对阶跃信号（如 0 突然跳到 100）和尖峰都比较敏感；
    单调平滑曲线的一阶差分方差接近 0，不会误报。
    """
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) < window * 2 + 1:
        return []

    ma = s.rolling(window, min_periods=window).mean()
    diffs = ma.diff().dropna()
    if len(diffs) < 2:
        return []

    std = diffs.std()
    if std <= 1e-12:
        return []

    mean_diff = diffs.mean()
    events = []
    for i, value in diffs.items():
        z = (value - mean_diff) / std
        if abs(z) > z_threshold:
            events.append({
                "type": "change_point",
                "column": name,
                "step": int(i),
                "message": f"{name} 在 step {i} 发生突变 (Δ={value:.3f})",
            })
    return events


def _dedup_events(events: list[dict]) -> list[dict]:
    """按 (type, step) 去重并排序。"""
    seen = set()
    result = []
    for e in events:
        key = (e["type"], e.get("step"))
        if key in seen:
            continue
        seen.add(key)
        result.append(e)
    return sorted(result, key=lambda e: e.get("step", 0))