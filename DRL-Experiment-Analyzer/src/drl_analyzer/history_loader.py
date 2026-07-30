"""
history_loader.py

Load WandB training history.
"""

from pathlib import Path

import pandas as pd



class HistoryLoader:


    def load(
        self,
        run_path: Path
    ) -> pd.DataFrame | None:


        run_path = Path(run_path)



        # ==================================
        # 1. history.csv
        # ==================================

        history_csv = (
            run_path /
            "files" /
            "history.csv"
        )


        if history_csv.exists():

            return pd.read_csv(
                history_csv
            )



        # ==================================
        # 2. WandB API
        # ==================================

        try:

            return self._load_from_wandb(
                run_path
            )


        except Exception as e:

            print(
                "WandB API loading failed:",
                e
            )



        return None



    def _load_from_wandb(
        self,
        run_path: Path
    ):
        """
        Load history using wandb API.
        """


        import wandb



        # 从目录获取run id

        run_id = (
            run_path.name
            .split("-")[-1]
        )


        # project路径

        parts = run_path.parts


        # 找 project

        # logs/a2c/Acrobot-v1/wandb/run-xxx

        algorithm = parts[-4]

        environment = parts[-3]


        project = (
            f"{algorithm}_{environment}"
        )



        api = wandb.Api()



        run = api.run(
            f"2797824480/{project}/{run_id}"
        )



        history = run.history(
            pandas=True
        )


        return history