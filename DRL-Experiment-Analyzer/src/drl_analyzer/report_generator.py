from pathlib import Path
import pandas as pd


class ReportGenerator:


    def generate(
        self,
        csv_file,
        output="results/report.xlsx"
    ):


        df=pd.read_csv(
            csv_file
        )


        Path(
            output
        ).parent.mkdir(
            exist_ok=True
        )


        with pd.ExcelWriter(
            output
        ) as writer:


            df.to_excel(
                writer,
                sheet_name="benchmark",
                index=False
            )


            for env in df.environment.unique():


                env_df=df[
                    df.environment==env
                ]


                env_df.to_excel(
                    writer,
                    sheet_name=env[:30],
                    index=False
                )


        return output