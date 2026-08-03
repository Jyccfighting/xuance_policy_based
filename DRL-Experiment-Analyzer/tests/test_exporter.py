"""exporter.py 单元测试。"""

import pandas as pd

from drl_analyzer.exporter import BenchmarkExporter
from drl_analyzer.models import Experiment, Metrics


def _experiment(algorithm="A2C", env="CartPole-v1", with_metrics=True):
    exp = Experiment(algorithm=algorithm, environment=env, seed=10, run_name=f"{algorithm}-{env}")
    if with_metrics:
        exp.metrics = Metrics(final_reward=100.0, episodes=5, runtime=10.0)
    return exp


def test_export_csv_status(tmp_path):
    experiments = [_experiment("A2C"), _experiment("PPO", with_metrics=False)]
    path = BenchmarkExporter(tmp_path).export_csv(experiments)
    df = pd.read_csv(path)
    assert len(df) == 2
    assert (df["status"] == ["ok", "no_history"]).all()


def test_export_excel(tmp_path):
    experiments = [_experiment("A2C", "CartPole-v1"), _experiment("PPO", "Pendulum-v1")]
    path = BenchmarkExporter(tmp_path).export_excel(experiments)
    assert path.exists()


def test_export_excel_empty(tmp_path):
    path = BenchmarkExporter(tmp_path).export_excel([])
    assert path.exists()