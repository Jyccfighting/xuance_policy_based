"""config.py 单元测试。"""

from drl_analyzer.config import AnalyzerConfig, ExperimentConfig, WandBConfig


def test_from_dict_unwrap():
    """应解包 {"value": ...} 并读取 agent/env_id/env_seed。"""
    data = {
        "agent": {"value": "C51"},
        "env_id": {"value": "CartPole-v1"},
        "env_seed": {"value": 1},
    }
    cfg = ExperimentConfig.from_dict(data)
    assert cfg.algorithm == "C51"
    assert cfg.environment == "CartPole-v1"
    assert cfg.seed == 1


def test_env_seed_zero_not_overridden():
    """env_seed=0 时不能错误落到 seed。"""
    cfg = ExperimentConfig.from_dict({"env_seed": 0, "seed": 7})
    assert cfg.seed == 0


def test_analyzer_config_cache_dir():
    """resolved_cache_dir 默认使用 log_root/.cache。"""
    cfg = AnalyzerConfig(log_root="logs")
    assert cfg.resolved_cache_dir().as_posix().endswith("logs/.cache")


def test_wandb_config_defaults():
    cfg = WandBConfig()
    assert cfg.enabled is True
    assert cfg.timeout == 30.0