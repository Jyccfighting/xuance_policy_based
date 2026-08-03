"""models.py 单元测试。"""

from drl_analyzer.models import Experiment, Metrics


def test_metrics_defaults():
    """默认值必须是 NaN/-1/0，且没有重复字段错误。"""
    m = Metrics()
    assert m.convergence_step == -1
    assert m.convergence_threshold != m.convergence_threshold  # NaN
    assert m.sample_efficiency != m.sample_efficiency  # NaN
    assert m.episodes == 0
    assert m.total_steps == 0


def test_metrics_to_dict():
    """to_dict 应包含全部字段。"""
    m = Metrics(final_reward=1.0)
    d = m.to_dict()
    assert d["final_reward"] == 1.0
    assert "overall_score" in d


def test_experiment_has_history():
    """has_history 应正确处理 None / 空表。"""
    e = Experiment()
    assert not e.has_history
    import pandas as pd
    e.history = pd.DataFrame()
    assert not e.has_history