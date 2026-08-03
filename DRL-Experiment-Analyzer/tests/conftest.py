"""
conftest.py

pytest 共享 fixture：全部使用合成数据与临时目录，不访问网络。
"""

from __future__ import annotations

import pandas as pd
import pytest


@pytest.fixture
def sample_history() -> pd.DataFrame:
    """构造带 reward/loss/runtime 的合成训练历史。"""
    return pd.DataFrame({
        "step": list(range(50)),
        "reward": [float(i) for i in range(50)],
        "loss": [1.0 / (i + 1) for i in range(50)],
        "_runtime": [i * 0.1 for i in range(50)],
    })


@pytest.fixture
def sample_benchmark(tmp_path):
    """构造一个小的 benchmark.csv，写入临时目录。"""
    import pandas as pd
    df = pd.DataFrame({
        "algorithm": ["A2C", "PPO", "A2C", "PPO"],
        "environment": ["CartPole-v1", "CartPole-v1", "Pendulum-v1", "Pendulum-v1"],
        "seed": [10, 10, 10, 10],
        "run_name": ["r1", "r2", "r3", "r4"],
        "status": ["ok", "ok", "ok", "ok"],
        "final_reward": [100.0, 200.0, -300.0, -100.0],
        "runtime": [100.0, 50.0, 300.0, 150.0],
        "stability": [80.0, 90.0, 60.0, 70.0],
        "sample_efficiency": [100.0, 50.0, 500.0, 200.0],
    })
    path = tmp_path / "benchmark.csv"
    df.to_csv(path, index=False)
    return path