"""
parser.py

Read

config.yaml

wandb-summary.json

Generate metrics
"""

import json
import yaml

from models import Experiment


class ExperimentParser:

    def parse(self, exp: Experiment):

        self.load_config(exp)

        self.load_summary(exp)

        self.extract_metrics(exp)

        return exp

    # ----------------------------------

    @staticmethod
    def load_config(exp):

        if exp.config_path.exists():

            with open(
                exp.config_path,
                "r",
                encoding="utf-8"
            ) as f:

                exp.config = yaml.safe_load(f)

    # ----------------------------------

    @staticmethod
    def load_summary(exp):

        if exp.summary_path.exists():

            with open(
                exp.summary_path,
                "r",
                encoding="utf-8"
            ) as f:

                exp.summary = json.load(f)

    # ----------------------------------

    @staticmethod
    def extract_metrics(exp):

        metrics = {}

        metrics["learning_rate"] = exp.config.get(
            "learning_rate"
        )

        metrics["gamma"] = exp.config.get(
            "gamma"
        )

        metrics["seed"] = exp.config.get(
            "seed"
        )

        metrics["batch_size"] = exp.config.get(
            "batch_size"
        )

        metrics["running_steps"] = exp.config.get(
            "running_steps"
        )

        # summary里面所有指标

        metrics.update(exp.summary)

        exp.metrics = metrics
        
    
    
    loader = HistoryLoader()

    if exp.history_csv_path is not None:

        exp.history = loader.load(
            exp.history_csv_path
    )
