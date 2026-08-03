"""summary_plot.py 单元测试：只验证图片文件能生成。"""

from drl_analyzer.visualization.summary_plot import SummaryPlotter


def test_plot_all_generates_pngs(sample_benchmark, tmp_path):
    plotter = SummaryPlotter(tmp_path / "figures")
    plotter.plot_all(sample_benchmark)
    names = {p.name for p in (tmp_path / "figures").glob("*.png")}
    assert "average_reward.png" in names
    assert "average_runtime.png" in names
    assert "overall_score.png" in names
    assert "win_count.png" in names


def test_plot_learning_curve(sample_history, tmp_path):
    plotter = SummaryPlotter(tmp_path / "figures")
    plotter.plot_learning_curve(
        [{"algorithm": "PPO", "history": sample_history}],
        "CartPole-v1",
    )
    assert (tmp_path / "figures" / "CartPole-v1_smooth_learning_curve.png").exists()


def test_plot_process_timeline(sample_history, tmp_path):
    plotter = SummaryPlotter(tmp_path / "figures")
    plotter.plot_process_timeline(
        sample_history,
        [{"type": "change_point", "step": 30, "message": "x"}],
        name="demo",
    )
    assert (tmp_path / "figures" / "demo_process_timeline.png").exists()