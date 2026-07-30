from pathlib import Path

from drl_analyzer.logger import get_logger
from drl_analyzer.scanner import Scanner
from drl_analyzer.history_loader import HistoryLoader
from drl_analyzer.metrics import MetricsCalculator
from drl_analyzer.exporter import BenchmarkExporter


logger = get_logger(__name__)


class Analyzer:
    """
    Main analyzer.

    Pipeline

        Scan
          ↓
        Load History
          ↓
        Calculate Metrics
          ↓
        Return Experiments
    """

    def __init__(self, log_root):

        self.log_root = Path(log_root)

        self.scanner = Scanner(self.log_root)

        self.history_loader = HistoryLoader()

        self.metrics_calculator = MetricsCalculator()

    # =====================================================

    def analyze(self):

        logger.info("Scanning experiments...")

        experiments = self.scanner.scan()

        logger.info(
            f"Found {len(experiments)} experiments."
        )

        for i, experiment in enumerate(experiments):

            logger.info(
                f"[{i+1}/{len(experiments)}] "
                f"{experiment.algorithm} "
                f"{experiment.environment}"
            )

            # ---------------------------------

            history = self.history_loader.load(
                experiment
            )

            experiment.history = history

            # ---------------------------------

            experiment.metrics = (
                self.metrics_calculator.calculate(
                    history
                )
            )

        logger.info("Analysis finished.")

        return experiments
    
    def export(
        self,
        experiments
    ):

        exporter = BenchmarkExporter()

        path = exporter.export_csv(
            experiments
        )

        logger.info(
            f"Benchmark saved: {path}"
        )