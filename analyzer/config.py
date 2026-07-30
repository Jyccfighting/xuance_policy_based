"""
config.py
全局配置
"""

from pathlib import Path

# 项目根目录（policy）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# logs目录
LOGS_DIR = PROJECT_ROOT / "logs"

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "analyzer" / "output"

CSV_DIR = OUTPUT_DIR / "csv"
EXCEL_DIR = OUTPUT_DIR / "excel"
FIGURE_DIR = OUTPUT_DIR / "figures"

for folder in [CSV_DIR, EXCEL_DIR, FIGURE_DIR]:
    folder.mkdir(parents=True, exist_ok=True)