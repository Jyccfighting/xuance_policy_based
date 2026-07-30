"""
Export benchmark results.
"""

from pathlib import Path
import pandas as pd


class BenchmarkExporter:


    def __init__(
        self,
        output_dir="results"
    ):

        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            exist_ok=True
        )


    def export_csv(
        self,
        experiments
    ):

        rows=[]


        for exp in experiments:


            row={

                "algorithm":
                    exp.algorithm,


                "environment":
                    exp.environment,


                "seed":
                    exp.seed,

            }


            # Metrics

            if exp.metrics:

                row.update({

                    "final_reward":
                        exp.metrics.final_reward,


                    "best_reward":
                        exp.metrics.best_reward,


                    "mean_reward":
                        exp.metrics.mean_reward,


                    "std_reward":
                        exp.metrics.std_reward,


                    "runtime":
                        exp.metrics.runtime,


                    "episodes":
                        exp.metrics.episodes,


                    "stability":
                        exp.metrics.stability_score,


                    "sample_efficiency":
                        exp.metrics.sample_efficiency,

                })


            rows.append(row)



        df=pd.DataFrame(rows)


        path = (
            self.output_dir /
            "benchmark.csv"
        )


        df.to_csv(
            path,
            index=False
        )


        return path