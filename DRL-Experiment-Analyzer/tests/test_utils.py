"""utils.py 单元测试。"""

from pathlib import Path

from drl_analyzer.utils import ensure_dir, format_seconds, moving_average


def test_ensure_dir(tmp_path):
    target = tmp_path / "a" / "b"
    assert ensure_dir(target) == target
    assert target.exists()


def test_format_seconds():
    assert format_seconds(3661) == "01:01:01"


def test_moving_average_short_input():
    """窗口大于长度时原样返回。"""
    result = moving_average([1, 2, 3], window=10)
    assert len(result) == 3