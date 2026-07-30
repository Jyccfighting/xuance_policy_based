# """
# history_loader.py

# Load WandB training history.
# """

# from pathlib import Path

# import pandas as pd

# import yaml

# class HistoryLoader:


#     def load(
#         self,
#         experiment
#     ):


#         run_path = experiment.path



#         # ==================================
#         # 1. history.csv
#         # ==================================

#         history_csv = (
#             run_path /
#             "files" /
#             "history.csv"
#         )


#         if history_csv.exists():

#             return pd.read_csv(
#                 history_csv
#             )



#         # ==================================
#         # 2. WandB API
#         # ==================================

#         try:

#             return self._load_from_wandb(
#                 run_path
#             )


#         except Exception as e:

#             print(
#                 "WandB API loading failed:",
#                 e
#             )



#         return None



#     def _load_from_wandb(
#         self,
#         experiment
#     ):
#         """
#         Load history using wandb API.
#         """

#         import wandb


#         run_path = experiment.path


#         # -------------------------
#         # get wandb run id
#         # -------------------------

#         run_id = (
#             run_path.name
#             .split("-")[-1]
#         )


#         # -------------------------
#         # get project name
#         # -------------------------

#         project = experiment.config.get(
#             "project_name",
#             None
#         )


#         if project is None:

#             raise ValueError(
#                 "project_name not found"
#             )


#         # -------------------------
#         # wandb api
#         # -------------------------

#         api = wandb.Api()
        
#         entity = experiment.config.get(
#             "wandb_user_name"
#         )


#         run = api.run(
#             f"{entity}/{project}/{run_id}"
#         )


#         history = run.history(
#             pandas=True
#         )


#         return history


"""
history_loader.py

Load WandB training history.
"""

from pathlib import Path

import pandas as pd



class HistoryLoader:


    def load(
        self,
        experiment
    ):
        """
        Load training history.

        Parameters
        ----------
        experiment:
            Experiment object

        Returns
        -------
        pandas.DataFrame | None
        """


        run_path = experiment.path



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
                experiment
            )


        except Exception as e:

            print(
                "WandB API loading failed:",
                e
            )



        return None



    def _load_from_wandb(
        self,
        experiment
    ):
        """
        Load history using wandb API.
        """


        import wandb



        run_path = experiment.path



        # -------------------------
        # get wandb run id
        # -------------------------

        run_id = (
            run_path.name
            .split("-")[-1]
        )



        # -------------------------
        # get wandb project
        # -------------------------

        project = (
            experiment.config
            .get(
                "project_name",
                None
            )
        )


        if project is None:

            raise ValueError(
                "project_name not found in config"
            )



        # -------------------------
        # get wandb entity
        # -------------------------

        entity = (
            experiment.config
            .get(
                "wandb_user_name",
                None
            )
        )


        if entity is None:

            raise ValueError(
                "wandb_user_name not found in config"
            )



        # -------------------------
        # WandB API
        # -------------------------

        api = wandb.Api()



        run = api.run(
            f"{entity}/{project}/{run_id}"
        )



        history = run.history(
            pandas=True
        )


        return history