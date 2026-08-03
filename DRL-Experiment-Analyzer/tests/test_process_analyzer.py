"""process_analyzer.py 单元测试。"""

import pandas as pd

from drl_analyzer.process_analyzer import analyze_process, extract_events


def test_change_point_detected():
    # reward 前 20 步 0，后 20 步 100，应检测到突变
    history = pd.DataFrame({"reward": [0.0] * 20 + [100.0] * 20})
    analysis = analyze_process(history, window=5)
    assert any(e["type"] == "change_point" for e in analysis["events"])


def test_nan_event():
    history = pd.DataFrame({"reward": [1.0, 2.0, None, 4.0]})
    analysis = analyze_process(history, window=1)
    assert any(e["type"] == "nan_or_inf" for e in analysis["events"])


def test_extract_events_from_log():
    log = "Epoch: 1/10\nTraceback (most recent call last):\n  File x.py\nBest Model Score: -500"
    events = extract_events(log)
    types = {e["type"] for e in events}
    assert "error" in types
    assert "best_model" in types
    assert "epoch" in types


def test_empty_history():
    analysis = analyze_process(pd.DataFrame())
    assert analysis["steps"] == 0