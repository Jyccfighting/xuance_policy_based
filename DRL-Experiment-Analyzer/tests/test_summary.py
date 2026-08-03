"""summary.py 单元测试。"""

import pandas as pd

from drl_analyzer.summary import SummaryGenerator


def test_generate_markdown(sample_benchmark, tmp_path):
    output = tmp_path / "summary.md"
    SummaryGenerator().generate(sample_benchmark, output)
    text = output.read_text(encoding="utf-8")
    assert "A2C" in text
    assert "PPO" in text
    assert "实验数量" in text


def test_generate_empty(tmp_path):
    csv = tmp_path / "empty.csv"
    pd.DataFrame(columns=["algorithm", "environment", "final_reward", "runtime", "stability"]).to_csv(csv, index=False)
    output = tmp_path / "summary.md"
    SummaryGenerator().generate(csv, output)
    assert "暂无有效实验数据" in output.read_text(encoding="utf-8")