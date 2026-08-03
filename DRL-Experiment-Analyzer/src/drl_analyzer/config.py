"""
config.py

全局配置模型。

包含：
- AnalyzerConfig：分析器整体配置（输入/输出目录、导出开关、WandB 配置）
- WandBConfig：WandB 在线获取配置（开关、超时、重试、缓存）
- ExperimentConfig：单个实验的元信息（算法、环境、种子、原始参数）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class WandBConfig:
    """WandB 在线获取配置。"""

    enabled: bool = True          # 是否允许通过 WandB API 获取过程数据
    entity: str | None = None     # WandB 用户名/实体
    project: str | None = None    # WandB 项目名
    timeout: float = 30.0         # 单次 API 请求超时（秒）
    retries: int = 2              # 失败后的重试次数
    cache_history: bool = True    # 获取成功后是否写入本地 history.csv 缓存


@dataclass
class AnalyzerConfig:
    """分析器全局配置。"""

    log_root: Path = Path("./logs")       # 实验日志根目录
    output_dir: Path = Path("./results")  # 输出目录
    cache_dir: Path | None = None         # 历史数据缓存目录，None 时使用 log_root/.cache
    save_csv: bool = True                 # 是否导出 benchmark.csv
    save_excel: bool = True               # 是否导出 Excel
    save_figures: bool = True             # 是否保存图表
    wandb: WandBConfig = field(default_factory=WandBConfig)

    def resolved_cache_dir(self) -> Path:
        """返回实际使用的缓存目录。"""
        if self.cache_dir is not None:
            return Path(self.cache_dir)
        return Path(self.log_root) / ".cache"


@dataclass
class ExperimentConfig:
    """单个实验的元信息（从 config.yaml / wandb-summary.json 提取）。"""

    algorithm: str | None = None
    environment: str | None = None
    seed: int | None = None
    parameters: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExperimentConfig":
        """从原始配置构造，兼容 WandB 的 {"value": ...} 包装格式。"""

        def unwrap(value: Any) -> Any:
            if isinstance(value, dict) and "value" in value:
                return value["value"]
            return value

        env_seed = unwrap(data.get("env_seed"))
        seed = unwrap(data.get("seed"))
        return cls(
            algorithm=unwrap(data.get("agent")) or unwrap(data.get("algorithm")),
            environment=unwrap(data.get("env_id")) or unwrap(data.get("environment")),
            # env_seed=0 时不能使用 or，否则会错误落到 seed
            seed=env_seed if env_seed is not None else seed,
            parameters=data,
        )