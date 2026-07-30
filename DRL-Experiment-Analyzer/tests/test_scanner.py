from pathlib import Path

from drl_analyzer.scanner import ExperimentScanner


def main():

    log_dir = Path(
        r"D:\document\coding\policy\logs"
    )


    scanner = ExperimentScanner(
        log_dir
    )


    experiments = scanner.scan()


    print(
        f"Found {len(experiments)} experiments"
    )


    for exp in experiments:

        print("----------------")

        print(
            exp
        )


if __name__ == "__main__":
    main()