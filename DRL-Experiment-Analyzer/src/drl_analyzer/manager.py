"""
manager.py

Experiment Manager
"""

from collections import defaultdict
from typing import List, Dict

from models import Experiment


class ExperimentManager:
    """
    管理所有 Experiment
    """

    def __init__(self):

        self.experiments: List[Experiment] = []

    # -------------------------------------

    def add(self, experiment: Experiment):

        self.experiments.append(experiment)

    # -------------------------------------

    def add_many(self, experiments: List[Experiment]):

        self.experiments.extend(experiments)

    # -------------------------------------

    def get_all(self) -> List[Experiment]:

        return self.experiments

    # -------------------------------------

    def count(self):

        return len(self.experiments)

    # -------------------------------------

    def algorithms(self):

        return sorted(
            {
                e.algorithm
                for e in self.experiments
            }
        )

    # -------------------------------------

    def environments(self):

        return sorted(
            {
                e.environment
                for e in self.experiments
            }
        )

    # -------------------------------------

    def by_algorithm(self, algorithm):

        return [

            e

            for e in self.experiments

            if e.algorithm == algorithm

        ]

    # -------------------------------------

    def by_environment(self, environment):

        return [

            e

            for e in self.experiments

            if e.environment == environment

        ]

    # -------------------------------------

    def summary(self):

        table: Dict = defaultdict(dict)

        for exp in self.experiments:

            algo = exp.algorithm

            env = exp.environment

            if env not in table[algo]:

                table[algo][env] = 0

            table[algo][env] += 1

        return table