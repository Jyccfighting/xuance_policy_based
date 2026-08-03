"""metrics.py 单元测试。"""

import numpy as np
import pandas as pd

from drl_analyzer.metrics import MetricsCalculator


def test_calculate_basic(sample_history):
    metrics = MetricsCalculator().calculate(sample_history)
    assert metrics.final_reward == 49.0
    assert metrics.episodes == 50
    assert metrics.total_steps == 50
    assert metrics.runtime == pytest.approx(4.9)
    assert metrics.convergence_step == 47
    assert metrics.sample_efficiency == 47.0
    assert metrics.stability_score > 0


def test_calculate_none_and_empty():
    calc = MetricsCalculator()
    m = calc.calculate(None)
    assert m.episodes == 0
    m2 = calc.calculate(pd.DataFrame())
    assert m2.episodes == 0


def test_extract_reward_none_returns_none():
    assert MetricsCalculator().extract_reward(None) is None


def test_extract_reward_xuance():
    history = pd.DataFrame({
        "Train-Episode-Rewards/0": [1.0, 2.0],
        "Train-Episode-Rewards/1": [3.0, 4.0],
    })
    reward = MetricsCalculator().extract_reward(history)
    assert reward.tolist() == [2.0, 3.0]


def test_no_reward_column():
    history = pd.DataFrame({"step": [0, 1]})
    assert MetricsCalculator().extract_reward(history) is None


import pytest