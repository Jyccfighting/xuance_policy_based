"""scoring.py 单元测试。"""

import pandas as pd

from drl_analyzer.scoring import compute_leaderboard, normalize, weighted_score


def test_normalize_directions():
    s = pd.Series([1.0, 2.0, 3.0])
    higher = normalize(s, higher_is_better=True)
    lower = normalize(s, higher_is_better=False)
    assert higher.iloc[0] == 0.0 and higher.iloc[-1] == 1.0
    assert lower.iloc[0] == 1.0 and lower.iloc[-1] == 0.0


def test_weighted_score():
    df = pd.DataFrame({
        "final_reward": [0.0, 10.0],
        "runtime": [10.0, 0.0],
    })
    score = weighted_score(df)
    # 第一个指标 reward 低但 runtime 高，用默认权重后应低于第二个
    assert score.iloc[0] < score.iloc[1]


def test_compute_leaderboard_sample_efficiency_direction():
    """sample_efficiency 越小越好。"""
    df = pd.DataFrame({
        "algorithm": ["A", "B"],
        "final_reward": [100.0, 100.0],
        "runtime": [10.0, 10.0],
        "stability": [80.0, 80.0],
        "sample_efficiency": [10.0, 1000.0],
    })
    board = compute_leaderboard(df)
    assert board.index[0] == "A"