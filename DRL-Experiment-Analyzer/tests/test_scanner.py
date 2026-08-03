"""scanner.py 单元测试：全部使用临时目录。"""

import yaml

from drl_analyzer.scanner import Scanner


def _make_run(tmp_path, algo="ppo", env="CartPole-v1", run="run-abc", config=None):
    """构造一个最小 run 目录结构。"""
    run_dir = tmp_path / "logs" / algo / env / "wandb" / run
    files = run_dir / "files"
    files.mkdir(parents=True, exist_ok=True)
    if config is not None:
        (files / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    return run_dir


def test_scan_finds_run_and_reads_config(tmp_path):
    config = {"agent": "PPO", "env_id": "CartPole-v1", "env_seed": 1}
    _make_run(tmp_path, config=config)

    experiments = Scanner(tmp_path / "logs").scan()
    assert len(experiments) == 1
    exp = experiments[0]
    assert exp.algorithm == "PPO"
    assert exp.environment == "CartPole-v1"
    assert exp.seed == 1
    assert exp.run_name == "run-abc"


def test_scan_infers_from_path_when_no_config(tmp_path):
    _make_run(tmp_path)  # 不写 config

    experiments = Scanner(tmp_path / "logs").scan()
    assert len(experiments) == 1
    assert experiments[0].algorithm == "ppo"
    assert experiments[0].environment == "CartPole-v1"


def test_scan_missing_root_returns_empty(tmp_path):
    assert Scanner(tmp_path / "not-exists").scan() == []