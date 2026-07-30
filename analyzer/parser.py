"""
parser.py

读取config.yaml
读取wandb-summary.json
"""

import json
import yaml

from models import Experiment


class ExperimentParser:

    def parse(self, experiment: Experiment):

        self.load_config(experiment)

        self.load_summary(experiment)

        return experiment

    @staticmethod
    def load_config(experiment):

        if experiment.config_path.exists():

            with open(
                experiment.config_path,
                "r",
                encoding="utf-8"
            ) as f:

                experiment.config = yaml.safe_load(f)

    @staticmethod
    def load_summary(experiment):

        if experiment.summary_path.exists():

            with open(
                experiment.summary_path,
                "r",
                encoding="utf-8"
            ) as f:

                experiment.summary = json.load(f)