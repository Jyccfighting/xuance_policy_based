from pathlib import Path

import pandas as pd



class SummaryGenerator:



    def generate(
        self,
        csv_file,
        output="results/summary.md"
    ):


        df = pd.read_csv(
            csv_file
        )


        output = Path(
            output
        )


        # =====================
        # Best algorithm
        # =====================


        best = (
            df
            .sort_values(
                "final_reward",
                ascending=False
            )
            .iloc[0]
        )


        fastest = (
            df
            .sort_values(
                "runtime"
            )
            .iloc[0]
        )


        stable = (
            df
            .sort_values(
                "stability",
                ascending=False
            )
            .iloc[0]
        )



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



        ranking_text = ""


        for i,row in enumerate(
            ranking.itertuples(),
            1
        ):

            ranking_text += (

                f"{i}. "
                f"{row.algorithm} "
                f"({row.environment}) "
                f"- reward={row.final_reward:.3f}\n"

            )



        # =====================
        # Environment analysis
        # =====================


        env_text=""


        for env in df.environment.unique():


            sub=df[
                df.environment==env
            ]


            best_env=(
                sub
                .sort_values(
                    "final_reward",
                    ascending=False
                )
                .iloc[0]
            )


            env_text += f"""

## {env}


最佳算法:

**{best_env.algorithm}**


最终奖励:

{best_env.final_reward:.3f}


"""


        # =====================
        # markdown
        # =====================


        md=f"""

# DRL Benchmark Summary


## Overall Performance


实验数量:

{len(df)}



最佳Reward算法:

**{best.algorithm}**


Reward:

{best.final_reward:.3f}



最高稳定性:

**{stable.algorithm}**


Stability:

{stable.stability:.3f}



最快训练:

**{fastest.algorithm}**


Runtime:

{fastest.runtime:.3f}s



---

# Algorithm Ranking


{ranking_text}



---

# Environment Analysis


{env_text}


"""


        output.parent.mkdir(
            exist_ok=True
        )


        output.write_text(
            md,
            encoding="utf-8"
        )


        return output