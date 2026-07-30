# """
# config.py
# 全局配置
# """

# from pathlib import Path

# # 项目根目录（policy）
# PROJECT_ROOT = Path(__file__).resolve().parent.parent

# # logs目录
# LOGS_DIR = PROJECT_ROOT / "logs"

# # 输出目录
# OUTPUT_DIR = PROJECT_ROOT / "analyzer" / "output"

# CSV_DIR = OUTPUT_DIR / "csv"
# EXCEL_DIR = OUTPUT_DIR / "excel"
# FIGURE_DIR = OUTPUT_DIR / "figures"

# OUTPUT_DIR = Path("output")

# EXCEL_DIR = OUTPUT_DIR / "excel"

# CSV_DIR = OUTPUT_DIR / "csv"

# PLOT_DIR = OUTPUT_DIR / "plots"

# REPORT_DIR = OUTPUT_DIR / "reports"

# for folder in [CSV_DIR, EXCEL_DIR, FIGURE_DIR]:
#     folder.mkdir(parents=True, exist_ok=True)


"""
config.py

Global configuration for DRL Experiment Analyzer.

Author : yyJ
Version : 1.0
"""

from pathlib import Path

# ==========================================================
# Project Directory
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_DIR = PROJECT_ROOT / "output"

# ==========================================================
# Output Directory
# ==========================================================

EXCEL_DIR = OUTPUT_DIR / "excel"

CSV_DIR = OUTPUT_DIR / "csv"

PLOT_DIR = OUTPUT_DIR / "plots"

REPORT_DIR = OUTPUT_DIR / "reports"

# ==========================================================
# Supported File Names
# ==========================================================

CONFIG_FILE = "config.yaml"

SUMMARY_FILE = "wandb-summary.json"

HISTORY_FILE = "history.csv"

# ==========================================================
# Plot Settings
# ==========================================================

FIGURE_DPI = 300

FIGURE_SIZE = (10, 6)

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# Auto Create Output Directories
# ==========================================================

for directory in (
    OUTPUT_DIR,
    EXCEL_DIR,
    CSV_DIR,
    PLOT_DIR,
    REPORT_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)