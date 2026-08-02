import pandas as pd
import matplotlib.pyplot as plt


class StabilityPlotter:


    def plot_stability(
        self,
        csv_file,
        save_path="stability.png"
    ):


        df = pd.read_csv(
            csv_file
        )


        plt.figure(
            figsize=(10,6)
        )


        plt.bar(
            df["algorithm"],
            df["stability"]
        )


        plt.xticks(
            rotation=45
        )


        plt.ylabel(
            "Stability"
        )


        plt.title(
            "Algorithm Stability Comparison"
        )


        plt.tight_layout()


        plt.savefig(
            save_path,
            dpi=300
        )


        plt.close()