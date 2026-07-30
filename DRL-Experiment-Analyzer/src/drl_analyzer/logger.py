"""
logger.py
~~~~~~~~~

统一日志管理模块。

功能：
1. 创建控制台 Logger
2. 创建文件 Logger
3. 自动创建日志目录
4. 防止重复添加 Handler
5. 所有模块统一调用

Author: yyJ
Version: 1.0
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

# =============================================================================
# Constants
# =============================================================================

DEFAULT_LOG_LEVEL = logging.INFO

DEFAULT_LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =============================================================================
# Logger Factory
# =============================================================================

def get_logger(
    name: str,
    log_dir: Optional[Path] = None,
    level: int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """
    Create or retrieve a configured logger.

    Parameters
    ----------
    name : str
        Logger name.
    log_dir : Path | None
        Directory used to save log files.
    level : int
        Logging level.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    # 已经初始化过，直接返回
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt=DEFAULT_LOG_FORMAT,
        datefmt=DEFAULT_DATE_FORMAT,
    )

    # -------------------------------------------------------------------------
    # Console Handler
    # -------------------------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(level)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # -------------------------------------------------------------------------
    # File Handler
    # -------------------------------------------------------------------------

    if log_dir is not None:

        log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        log_file = log_dir / "analyzer.log"

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        file_handler.setLevel(level)

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger


# =============================================================================
# Root Logger
# =============================================================================

logger = get_logger("DRLAnalyzer")