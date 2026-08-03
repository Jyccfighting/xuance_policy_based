"""
config_cleaner.py

清洗 WandB 配置格式：
- 去掉 "_" 开头的 WandB 内部字段
- 递归解包 {"value": ...}
"""

from typing import Any


class ConfigCleaner:
    """把 WandB 配置转换为普通 dict。"""

    @staticmethod
    def clean(config: dict) -> dict:
        """
        清洗配置。

        参数
        ----
        config : dict
            原始配置。

        返回
        ----
        dict
            去掉内部字段并解包 value 的配置。
        """
        cleaned = {}
        for key, value in config.items():
            # 移除 wandb 内部数据
            if key.startswith("_"):
                continue
            cleaned[key] = ConfigCleaner._unwrap(value)
        return cleaned

    @staticmethod
    def _unwrap(value: Any) -> Any:
        """递归解包 {"value": xxx}。"""
        if isinstance(value, dict):
            if "value" in value:
                return value["value"]
            return {
                k: ConfigCleaner._unwrap(v)
                for k, v in value.items()
            }
        return value