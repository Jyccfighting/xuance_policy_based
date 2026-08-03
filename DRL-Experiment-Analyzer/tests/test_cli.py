"""cli.py 冒烟测试：临时日志目录 + 禁用网络。"""

import yaml

from drl_analyzer.cli import main


def _make_logs(tmp_path):
    """构造一个带本地 history.csv 的实验目录，保证离线可跑。"""
    run_dir = tmp_path / "logs" / "ppo" / "CartPole-v1" / "wandb" / "run-abc"
    files = run_dir / "files"
    files.mkdir(parents=True, exist_ok=True)
    (files / "config.yaml").write_text(
        yaml.safe_dump({"agent": "PPO", "env_id": "CartPole-v1", "env_seed": 10}),
        encoding="utf-8",
    )
    import pandas as pd
    pd.DataFrame({
        "step": range(10),
        "reward": [float(i) for i in range(10)],
        "_runtime": [float(i) for i in range(10)],
    }).to_csv(files / "history.csv", index=False)
    return tmp_path / "logs"


def test_cli_offline_run(tmp_path):
    logs = _make_logs(tmp_path)
    out = tmp_path / "out"
    code = main([
        "--log-root", str(logs),
        "--output", str(out),
        "--no-wandb",
        "--process-report", str(tmp_path / "process.md"),
    ])
    assert code == 0
    assert (out / "benchmark.csv").exists()
    assert (out / "summary.md").exists()
    assert (out / "report.html").exists()
    assert (tmp_path / "process.md").exists()


def test_cli_empty_logs(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir()
    code = main(["--log-root", str(logs), "--output", str(tmp_path / "out2"), "--no-wandb", "--no-plots"])
    assert code == 0