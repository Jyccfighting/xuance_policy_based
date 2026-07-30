"""
excel_writer.py

将所有 Experiment 导出为 Excel
"""

from pathlib import Path
from typing import List

import pandas as pd

from models import Experiment


class ExcelWriter:

    def __init__(self, output_dir: Path):

        self.output_dir = output_dir

        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------

    def export(self, experiments: List[Experiment]):

        rows = []

        for exp in experiments:

            row = {

                # 基本信息
                "Algorithm": exp.algorithm,
                "Environment": exp.environment,
                "Run": exp.run_name,

                # 参数
                "Seed": exp.get("seed"),
                "Learning Rate": exp.get("learning_rate"),
                "Gamma": exp.get("gamma"),
                "Batch Size": exp.get("batch_size"),
                "Buffer Size": exp.get("buffer_size"),
                "Running Steps": exp.get("running_steps"),

                # WandB Summary（如果存在）
                "Best Score": exp.get("Best Score"),
                "Train Step": exp.get("Train Step"),
                "Episode": exp.get("Episode"),
                "Runtime": exp.get("_runtime"),

            }

            rows.append(row)

        df = pd.DataFrame(rows)

        save_path = self.output_dir / "experiment_index.xlsx"

        df.to_excel(save_path, index=False)

        print(f"\nExcel 已保存：{save_path}")

        return df