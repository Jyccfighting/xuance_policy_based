import pandas as pd
import matplotlib.pyplot as plt


class EfficiencyPlotter:


    def plot_efficiency(
        self,
        csv_file,
        save_path="efficiency.png"
    ):


        df = pd.read_csv(
            csv_file
        )


        plt.figure(
            figsize=(10,6)
        )


        plt.bar(
            df["algorithm"],
            df["sample_efficiency"]
        )


        plt.xticks(
            rotation=45
        )


        plt.ylabel(
            "Sample Efficiency"
        )


        plt.title(
            "Sample Efficiency Comparison"
        )


        plt.tight_layout()


        plt.savefig(
            save_path,
            dpi=300
        )


        plt.close()