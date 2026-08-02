import matplotlib.pyplot as plt


class RewardPlotter:


    def plot(
        self,
        experiments,
        save_path="reward_curve.png"
    ):


        plt.figure(
            figsize=(10,6)
        )


        for exp in experiments:


            if exp.metrics is None:
                continue


            reward = exp.metrics.reward_history


            if reward is None:
                continue


            plt.plot(
                reward,
                label=(
                    f"{exp.algorithm}-"
                    f"{exp.environment}"
                )
            )


        plt.xlabel(
            "Training Step"
        )


        plt.ylabel(
            "Reward"
        )


        plt.title(
            "DRL Reward Curve"
        )


        plt.legend()


        plt.grid(
            True
        )


        plt.savefig(
            save_path,
            dpi=300,
            bbox_inches="tight"
        )


        plt.close()


        return save_path