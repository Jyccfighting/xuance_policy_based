from pathlib import Path

from drl_analyzer.utils import (
    ensure_dir,
    format_seconds,
    moving_average,
)


def main():

    ensure_dir(Path("output"))

    print("Directory OK")

    print(format_seconds(3661))

    reward = [1,2,3,4,5,6]

    ma = moving_average(
        reward,
        window=3
    )

    print(ma)


if __name__ == "__main__":
    main()