"""
logger.py

统一日志管理：
1. 创建控制台 Logger
2. 可选创建文件 Logger（自动建目录）
3. 防止重复添加 Handler
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

# 默认日志级别与格式
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(
    name: str,
    log_dir: Optional[Path] = None,
    level: int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """
    创建或获取一个配置好的 logger。

    参数
    ----
    name : str
        logger 名称。
    log_dir : Path | None
        日志目录；传了才会写 analyzer.log 文件。
    level : int
        日志级别。
    """

    logger = logging.getLogger(name)

    # 已初始化过，直接返回，避免重复 handler
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
    )

    # 控制台 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 文件 handler（可选）
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            log_dir / "analyzer.log",
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# 模块级默认 logger
logger = get_logger("DRLAnalyzer")