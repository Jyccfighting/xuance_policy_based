import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


class RuntimePlotter:


    def plot_runtime(
        self,
        csv_file,
        save_path="results/runtime.png"
    ):


        df = pd.read_csv(csv_file)


        plt.figure(
            figsize=(10,6)
        )


        plt.bar(
            df["algorithm"],
            df["runtime"]
        )


        plt.xticks(
            rotation=45
        )


        plt.ylabel(
            "Runtime(s)"
        )


        plt.title(
            "Training Runtime Comparison"
        )


        plt.tight_layout()


        Path(save_path).parent.mkdir(
            exist_ok=True
        )


        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )


        plt.close()


        print(
            f"Runtime plot saved: {save_path}"
        )