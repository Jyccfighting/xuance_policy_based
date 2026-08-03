"""report.py 单元测试。"""

from drl_analyzer.report import ReportGenerator


def test_generate_html(sample_benchmark, tmp_path):
    output = tmp_path / "report.html"
    ReportGenerator().generate(sample_benchmark, figure_dir=tmp_path / "no-figures", output=output)
    text = output.read_text(encoding="utf-8")
    assert "DRL Benchmark Report" in text
    assert "A2C" in text