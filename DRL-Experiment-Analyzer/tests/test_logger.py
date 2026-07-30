from pathlib import Path

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

from drl_analyzer.logger import get_logger


def main():

    logger = get_logger(
        "TestLogger",
        log_dir=Path("./logs")
    )

    logger.debug("Debug Message")

    logger.info("Info Message")

    logger.warning("Warning Message")

    logger.error("Error Message")

    logger.critical("Critical Message")


if __name__ == "__main__":
    main()