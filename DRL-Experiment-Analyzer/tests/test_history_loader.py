from pathlib import Path

from drl_analyzer.history_loader import (
    HistoryLoader
)



def main():

    run_path = Path(
        r"D:\document\coding\policy\logs\a2c\Acrobot-v1\wandb\run-20260729_152317-bmpn9afc"
    )


    loader = HistoryLoader()


    history = loader.load(
        run_path
    )


    if history is None:

        print(
            "No history found"
        )

    else:

        print(
            history.head()
        )

        print(
            history.columns
        )



if __name__ == "__main__":
    main()