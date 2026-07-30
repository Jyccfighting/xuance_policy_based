"""
scanner.py

扫描整个logs目录
"""

from pathlib import Path
from typing import List

from models import Experiment


class ExperimentScanner:

    def __init__(self, logs_dir: Path):

        self.logs_dir = Path(logs_dir)

    def scan(self) -> List[Experiment]:

        experiments = []

        if not self.logs_dir.exists():

            raise FileNotFoundError(
                f"{self.logs_dir} 不存在"
            )

        # algorithm
        for algorithm_dir in sorted(self.logs_dir.iterdir()):

            if not algorithm_dir.is_dir():
                continue

            algorithm = algorithm_dir.name

            # environment
            for env_dir in sorted(algorithm_dir.iterdir()):

                if not env_dir.is_dir():
                    continue

                environment = env_dir.name

                wandb_dir = env_dir / "wandb"

                if not wandb_dir.exists():
                    continue

                # run
                for run_dir in sorted(wandb_dir.iterdir()):

                    if not run_dir.is_dir():
                        continue

                    if not run_dir.name.startswith("run-"):
                        continue

                    files_dir = run_dir / "files"

                    config_path = files_dir / "config.yaml"

                    summary_path = (
                        files_dir /
                        "wandb-summary.json"
                    )

                    wandb_files = list(
                        run_dir.glob("*.wandb")
                    )

                    wandb_file = (
                        wandb_files[0]
                        if wandb_files
                        else Path()
                    )

                    experiment = Experiment(

                        algorithm=algorithm,

                        environment=environment,

                        run_name=run_dir.name,

                        run_path=run_dir,

                        config_path=config_path,

                        summary_path=summary_path,

                        wandb_file=wandb_file

                    )

                    experiments.append(experiment)

        return experiments