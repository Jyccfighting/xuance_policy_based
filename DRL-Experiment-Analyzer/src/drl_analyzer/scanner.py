# """
# scanner.py

# 扫描整个logs目录
# """

# from pathlib import Path
# from typing import List

# from models import Experiment


# class ExperimentScanner:

#     def __init__(self, logs_dir: Path):

#         self.logs_dir = Path(logs_dir)

#     def scan(self) -> List[Experiment]:

#         experiments = []

#         if not self.logs_dir.exists():

#             raise FileNotFoundError(
#                 f"{self.logs_dir} 不存在"
#             )

#         # algorithm
#         for algorithm_dir in sorted(self.logs_dir.iterdir()):

#             if not algorithm_dir.is_dir():
#                 continue

#             algorithm = algorithm_dir.name

#             # environment
#             for env_dir in sorted(algorithm_dir.iterdir()):

#                 if not env_dir.is_dir():
#                     continue

#                 environment = env_dir.name

#                 wandb_dir = env_dir / "wandb"

#                 if not wandb_dir.exists():
#                     continue

#                 # run
#                 for run_dir in sorted(wandb_dir.iterdir()):

#                     if not run_dir.is_dir():
#                         continue

#                     if not run_dir.name.startswith("run-"):
#                         continue

#                     files_dir = run_dir / "files"

#                     config_path = files_dir / "config.yaml"

#                     summary_path = (
#                         files_dir /
#                         "wandb-summary.json"
#                     )

#                     wandb_files = list(
#                         run_dir.glob("*.wandb")
#                     )

#                     wandb_file = (
#                         wandb_files[0]
#                         if wandb_files
#                         else Path()
#                     )

#                     experiment = Experiment(

#                         algorithm=algorithm,

#                         environment=environment,

#                         run_name=run_dir.name,

#                         run_path=run_dir,

#                         config_path=config_path,

#                         summary_path=summary_path,

#                         wandb_file=wandb_file

#                     )

#                     experiments.append(experiment)

#         return experiments


"""
scanner.py

Scan all experiment logs and build Experiment objects.

Author : yyJ
Version : 1.0
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from config import (
    CONFIG_FILE,
    HISTORY_FILE,
    LOG_DIR,
    SUMMARY_FILE,
)

from models import Experiment

logger = logging.getLogger(__name__)


class ExperimentScanner:
    """
    Scan experiment directories.
    """

    def __init__(self, log_dir: Path = LOG_DIR):

        self.log_dir = Path(log_dir)

    # --------------------------------------------------

    def scan(self) -> List[Experiment]:

        experiments = []

        if not self.log_dir.exists():

            logger.warning(
                "Log directory does not exist:\n%s",
                self.log_dir
            )

            return experiments

        logger.info(
            "Scanning %s ...",
            self.log_dir
        )

        for algorithm_dir in sorted(self.log_dir.iterdir()):

            if not algorithm_dir.is_dir():

                continue

            experiments.extend(

                self.scan_algorithm(
                    algorithm_dir
                )

            )

        logger.info(
            "Found %d experiments.",
            len(experiments)
        )

        return experiments

    # --------------------------------------------------

    def scan_algorithm(
        self,
        algorithm_dir: Path
    ) -> List[Experiment]:

        experiments = []

        for env_dir in sorted(algorithm_dir.iterdir()):

            if not env_dir.is_dir():

                continue

            experiments.extend(

                self.scan_environment(
                    algorithm_dir.name,
                    env_dir
                )

            )

        return experiments

    # --------------------------------------------------

    def scan_environment(
        self,
        algorithm: str,
        env_dir: Path
    ) -> List[Experiment]:

        experiments = []

        wandb_dir = env_dir / "wandb"

        if not wandb_dir.exists():

            return experiments

        for run_dir in sorted(wandb_dir.glob("run-*")):

            exp = self.scan_run(
                algorithm,
                env_dir.name,
                run_dir
            )

            if exp is not None:

                experiments.append(exp)

        return experiments
    

    # --------------------------------------------------
    # Scan One Run
    # --------------------------------------------------

    def scan_run(
        self,
        algorithm: str,
        environment: str,
        run_dir: Path
    ) -> Experiment | None:
        """
        Scan one WandB run directory.

        Example
        -------
        run-20260729_152317-bmpn9afc
        """

        logger.info(
            "Scanning run: %s",
            run_dir.name
        )

        files_dir = run_dir / "files"

        if not files_dir.exists():

            logger.warning(
                "Missing files directory: %s",
                run_dir
            )

            return None

        experiment = Experiment(
            root_dir=run_dir
        )

        experiment.algorithm = algorithm

        experiment.environment = environment

        experiment.run_name = run_dir.name

        experiment.config_path = self.find_config(
            files_dir
        )

        experiment.summary_path = self.find_summary(
            files_dir
        )

        experiment.history_csv_path = self.find_history(
            files_dir
        )

        self.validate(
            experiment
        )

        return experiment
    

    # --------------------------------------------------

    def find_config(
        self,
        files_dir: Path
    ) -> Path | None:

        path = files_dir / CONFIG_FILE

        if path.exists():

            return path

        logger.warning(
            "config.yaml not found:\n%s",
            files_dir
        )

        return None
    

    # --------------------------------------------------

    def find_summary(
        self,
        files_dir: Path
    ) -> Path | None:

        path = files_dir / SUMMARY_FILE

        if path.exists():

            return path

        logger.warning(
            "wandb-summary.json not found:\n%s",
            files_dir
        )

        return None
    
    
    # --------------------------------------------------

    def find_history(
        self,
        files_dir: Path
    ) -> Path | None:

        path = files_dir / HISTORY_FILE

        if path.exists():

            return path

        logger.warning(
            "history.csv not found:\n%s",
            files_dir
        )

        return None
    
    
    # --------------------------------------------------

    def validate(
        self,
        experiment: Experiment
    ) -> None:

        logger.info(
            "Validate experiment: %s",
            experiment.run_name
        )

        if experiment.config_path is None:

            logger.warning(
                "Missing config."
            )

        if experiment.summary_path is None:

            logger.warning(
                "Missing summary."
            )

        if experiment.history_csv_path is None:

            logger.warning(
                "Missing history csv."
            )
            
            
    # --------------------------------------------------

    @staticmethod
    def print_experiment(
        experiment: Experiment
    ):

        print("=" * 60)

        print(
            f"Algorithm : {experiment.algorithm}"
        )

        print(
            f"Environment : {experiment.environment}"
        )

        print(
            f"Run : {experiment.run_name}"
        )

        print(
            f"Config : {experiment.config_path}"
        )

        print(
            f"Summary : {experiment.summary_path}"
        )

        print(
            f"History : {experiment.history_csv_path}"
        )

        print("=" * 60)