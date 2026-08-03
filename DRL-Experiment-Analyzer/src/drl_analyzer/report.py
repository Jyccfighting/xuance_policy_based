from pathlib import Path

import pandas as pd


class ReportGenerator:

    def generate(
        self,
        csv_file,
        figure_dir="results/figures",
        output="results/report.html"
    ):

        csv_file = Path(csv_file)
        figure_dir = Path(figure_dir)
        output = Path(output)

        df = pd.read_csv(csv_file)

        # ======================================================
        # Summary
        # ======================================================

        best_reward = df.loc[
            df.final_reward.idxmax()
        ]

        fastest = df.loc[
            df.runtime.idxmin()
        ]

        stable_df = df.dropna(
            subset=["stability"]
        )

        if len(stable_df) > 0:

            stable = stable_df.loc[
                stable_df.stability.idxmax()
            ]

        else:

            stable = None

        # ======================================================
        # LeaderBoard
        # ======================================================

        score = df.groupby(
            "algorithm"
        ).agg({

            "final_reward":"mean",

            "runtime":"mean",

            "stability":"mean",

            "sample_efficiency":"mean"

        })

        reward = (

            score.final_reward -

            score.final_reward.min()

        ) / (

            score.final_reward.max()

            -

            score.final_reward.min()

            +

            1e-6

        )

        runtime = (

            score.runtime.max()

            -

            score.runtime

        ) / (

            score.runtime.max()

            -

            score.runtime.min()

            +

            1e-6

        )

        stability = (

            score.stability -

            score.stability.min()

        ) / (

            score.stability.max()

            -

            score.stability.min()

            +

            1e-6

        )

        efficiency = (

            score.sample_efficiency -

            score.sample_efficiency.min()

        ) / (

            score.sample_efficiency.max()

            -

            score.sample_efficiency.min()

            +

            1e-6

        )

        score["Overall Score"] = (

            0.4 * reward +

            0.2 * runtime +

            0.2 * stability +

            0.2 * efficiency

        )

        score = score.sort_values(

            "Overall Score",

            ascending=False

        )

        score.insert(

            0,

            "Rank",

            range(

                1,

                len(score)+1

            )

        )

        leaderboard = score.to_html()

        ranking = (

            df.sort_values(

                "final_reward",

                ascending=False

            )

            [

                [

                    "algorithm",

                    "environment",

                    "final_reward"

                ]

            ]

            .to_html(index=False)

        )

        benchmark = df.to_html(index=False)

        # ======================================================
        # HTML
        # ======================================================

        html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>

DRL Benchmark Report

</title>

<style>

body{{

font-family:Arial;

margin:40px;

}}

table{{

border-collapse:collapse;

width:100%;

}}

th,td{{

border:1px solid #ddd;

padding:8px;

text-align:center;

}}

th{{

background:#eeeeee;

}}

.summary{{

background:#f5f5f5;

padding:20px;

border-radius:8px;

}}

img{{

width:900px;

margin-top:20px;

margin-bottom:30px;

border:1px solid #ccc;

}}

</style>

</head>

<body>

<h1>

Deep Reinforcement Learning Benchmark Report

</h1>

<h2>

Experiment Summary

</h2>

<div class="summary">

<p>

Total Experiments :

<b>{len(df)}</b>

</p>

<p>

Best Reward :

<b>{best_reward.algorithm}</b>

({best_reward.final_reward:.3f})

</p>

<p>

Fastest :

<b>{fastest.algorithm}</b>

({fastest.runtime:.2f} s)

</p>

"""

        if stable is not None:

            html += f"""

<p>

Most Stable :

<b>{stable.algorithm}</b>

({stable.stability:.2f})

</p>

"""

        html += f"""

</div>

<h2>

Algorithm LeaderBoard

</h2>

{leaderboard}

<h2>

Reward Ranking

</h2>

{ranking}

<h2>

Benchmark Table

</h2>

{benchmark}

<h2>

Figures

</h2>

"""

        # ======================================================
        # Figures
        # ======================================================

        if figure_dir.exists():

            for img in sorted(

                figure_dir.glob("*.png")

            ):

                html += f"""

<h3>

{img.stem}

</h3>

<img src="../{img.as_posix()}">

"""

        else:

            html += """

<p>

No Figures.

</p>

"""

        # ======================================================
        # Conclusion
        # ======================================================

        html += f"""

<h2>

Conclusion

</h2>

<ul>

<li>

Best Overall Algorithm :

<b>{score.index[0]}</b>

</li>

<li>

Highest Reward :

<b>{best_reward.algorithm}</b>

</li>

<li>

Fastest Training :

<b>{fastest.algorithm}</b>

</li>

"""

        if stable is not None:

            html += f"""

<li>

Most Stable :

<b>{stable.algorithm}</b>

</li>

"""

        html += """

</ul>

</body>

</html>

"""

        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        output.write_text(

            html,

            encoding="utf-8"

        )

        return output