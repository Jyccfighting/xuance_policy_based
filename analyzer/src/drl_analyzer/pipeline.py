"""
pipeline.py

Experiment Processing Pipeline
"""

from history_loader import HistoryLoader
from metrics import MetricsCalculator


class ExperimentPipeline:

    def __init__(self):

        self.history_loader = HistoryLoader()

        self.metrics_calculator = MetricsCalculator()

    # -------------------------------------------------

    def process(self, experiment):

        # 1 Load History

        if experiment.history_csv_path is not None:

            experiment.history = self.history_loader.load(
                experiment.history_csv_path
            )

        # 2 Calculate Metrics

        if experiment.history is not None:

            experiment.metrics = self.metrics_calculator.calculate(
                experiment.history
            )

        return experiment

    # -------------------------------------------------

    def process_all(self, experiments):

        results = []

        for exp in experiments:

            results.append(

                self.process(exp)

            )

        return results