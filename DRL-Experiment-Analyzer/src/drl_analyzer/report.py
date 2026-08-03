from pathlib import Path

import pandas as pd

from drl_analyzer.analyzer import Analyzer



class ReportGenerator:


    def generate(
        self,
        csv_file,
        figure_dir="results/figures",
        output="results/report.html"
    ):


        csv_file = Path(csv_file)

        figure_dir = Path(
            figure_dir
        )

        output = Path(
            output
        )


        # =====================
        # Load benchmark
        # =====================

        df = pd.read_csv(
            csv_file
        )


        # =====================
        # Basic analysis
        # =====================


        # best reward

        best_reward_row = (
            df
            .sort_values(
                "final_reward",
                ascending=False
            )
            .iloc[0]
        )


        best_reward_algorithm = (
            best_reward_row["algorithm"]
        )


        best_reward_value = (
            round(
                best_reward_row["final_reward"],
                3
            )
        )



        # stability

        if "stability" in df.columns:


            stable_row = (
                df
                .sort_values(
                    "stability",
                    ascending=False
                )
                .iloc[0]
            )


            best_stability_algorithm = (
                stable_row["algorithm"]
            )


            best_stability_value = (
                round(
                    stable_row["stability"],
                    3
                )
            )


        else:

            best_stability_algorithm = "N/A"

            best_stability_value = "N/A"



        # runtime

        if "runtime" in df.columns:


            fast_row = (
                df
                .sort_values(
                    "runtime",
                    ascending=True
                )
                .iloc[0]
            )


            fastest_algorithm = (
                fast_row["algorithm"]
            )


            fastest_time = (
                round(
                    fast_row["runtime"],
                    3
                )
            )


        else:

            fastest_algorithm = "N/A"

            fastest_time = "N/A"



        # =====================
        # Ranking
        # =====================


        ranking = (

            df

            .sort_values(
                "final_reward",
                ascending=False
            )

        )



        ranking_html = (

            ranking
            [
                [
                    "algorithm",
                    "environment",
                    "final_reward"
                ]
            ]

            .to_html(
                index=False
            )

        )



        table_html = (

            df

            .to_html(
                index=False
            )

        )



        # =====================
        # HTML
        # =====================


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

font-family:
Arial, sans-serif;

margin:
40px;

background:
#ffffff;

}}



h1{{

color:
#333333;

}}



h2{{

margin-top:
40px;

}}



table{{

border-collapse:
collapse;

width:
100%;

}}



th,td{{

border:
1px solid #cccccc;

padding:
8px;

text-align:center;

}}



th{{

background:
#eeeeee;

}}



img{{

width:
800px;

margin:
20px;

border:
1px solid #ddd;

}}



.summary{{

background:
#f7f7f7;

padding:
20px;

border-radius:
10px;

}}


</style>



</head>



<body>



<h1>
Deep Reinforcement Learning Benchmark Report
</h1>



<h2>
1. Experiment Summary
</h2>



<div class="summary">


<p>

Total Experiments:

<b>
{len(df)}
</b>


</p>



<p>

Best Reward Algorithm:

<b>
{best_reward_algorithm}
</b>


<br>

Reward:

{best_reward_value}


</p>




<p>

Most Stable Algorithm:

<b>
{best_stability_algorithm}
</b>


<br>

Stability:

{best_stability_value}


</p>




<p>

Fastest Algorithm:

<b>
{fastest_algorithm}
</b>


<br>

Runtime:

{fastest_time}s


</p>


</div>




<h2>
2. Algorithm Ranking
</h2>


{ranking_html}





<h2>
3. Complete Benchmark Results
</h2>


{table_html}




<h2>
4. Visualization Results
</h2>


"""



        # =====================
        # Add figures
        # =====================


        if figure_dir.exists():


            images = list(
                figure_dir.glob(
                    "*.png"
                )
            )


            for img in images:


                html += f"""

<h3>
{img.stem}
</h3>


<img src="../{img.as_posix()}">


"""



        else:


            html += """

<p>
No visualization figures found.
</p>

"""



        html += """

</body>

</html>

"""



        # =====================
        # Save
        # =====================


        output.parent.mkdir(
            exist_ok=True
        )


        output.write_text(
            html,
            encoding="utf-8"
        )


        return output