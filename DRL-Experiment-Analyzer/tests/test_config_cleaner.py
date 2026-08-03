"""config_cleaner.py 单元测试。"""

from drl_analyzer.config_cleaner import ConfigCleaner


def test_clean_removes_private_and_unwraps():
    config = {
        "_wandb": {"value": {"cli": "0.28"}},
        "agent": {"value": "A2C"},
        "gamma": {"value": 0.98},
        "nested": {"inner": {"value": 1}},
    }
    cleaned = ConfigCleaner.clean(config)
    assert "_wandb" not in cleaned
    assert cleaned["agent"] == "A2C"
    assert cleaned["gamma"] == 0.98
    assert cleaned["nested"] == {"inner": 1}