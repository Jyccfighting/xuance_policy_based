"""
report.py

生成 HTML 报告：实验汇总、算法排行榜、Reward 排名、明细表、图表。
"""

from __future__ import annotations

import html
import logging
import os
from pathlib import Path

import pandas as pd

from drl_analyzer.scoring import compute_leaderboard

logger = logging.getLogger(__name__)


class ReportGenerator:
    """从 benchmark.csv 生成 report.html。"""

    def generate(
        self,
        csv_file,
        figure_dir="results/figures",
        output="results/report.html",
    ) -> Path:
        """
        参数
        ----
        csv_file : str | Path
            benchmark.csv 路径。
        figure_dir : str | Path
            图表目录，用于嵌入图片。
        output : str | Path
            输出 HTML 路径。
        """
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        figure_dir = Path(figure_dir)

        df = pd.read_csv(csv_file)
        valid = self._valid_rows(df)

        if valid.empty:
            output.write_text("<html><body><h1>DRL Benchmark Report</h1><p>暂无有效实验数据。</p></body></html>", encoding="utf-8")
            return output

        # 汇总
        best = valid.sort_values("final_reward", ascending=False).iloc[0]
        fastest = valid.sort_values("runtime").iloc[0]
        stable_df = valid.dropna(subset=["stability"])
        stable = stable_df.sort_values("stability", ascending=False).iloc[0] if not stable_df.empty else None

        # 排行榜与表格
        leaderboard = compute_leaderboard(valid)
        leaderboard.index.name = "algorithm"
        leaderboard_html = leaderboard.to_html()
        ranking_html = (
            valid.sort_values("final_reward", ascending=False)
            [["algorithm", "environment", "final_reward"]]
            .to_html(index=False)
        )
        benchmark_html = valid.to_html(index=False)

        # 图片（相对 report.html 的路径）
        images = ""
        if figure_dir.exists():
            for img in sorted(figure_dir.glob("*.png")):
                rel = os.path.relpath(img, output.parent).replace("\\", "/")
                images += f'<h3>{html.escape(img.stem)}</h3><img src="{html.escape(rel)}">'

        stable_html = (
            f"<p>Most Stable: <b>{html.escape(str(stable.algorithm))}</b> ({stable.stability:.2f})</p>"
            if stable is not None else "<p>Most Stable: 暂无有效数据</p>"
        )

        html_text = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>DRL Benchmark Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
th {{ background: #eee; }}
img {{ width: 900px; max-width: 100%; margin: 10px 0; border: 1px solid #ccc; }}
</style>
</head>
<body>
<h1>Deep Reinforcement Learning Benchmark Report</h1>
<h2>Experiment Summary</h2>
<div class="summary">
<p>Total Experiments: <b>{len(valid)}</b></p>
<p>Best Reward: <b>{html.escape(str(best.algorithm))}</b> ({html.escape(str(best.environment))}) - {best.final_reward:.3f}</p>
<p>Fastest: <b>{html.escape(str(fastest.algorithm))}</b> - {fastest.runtime:.2f}s</p>
{stable_html}
</div>
<h2>Algorithm LeaderBoard</h2>
{leaderboard_html}
<h2>Reward Ranking</h2>
{ranking_html}
<h2>Benchmark Table</h2>
{benchmark_html}
<h2>Figures</h2>
{images if images else '<p>No Figures.</p>'}
<h2>Conclusion</h2>
<ul>
<li>Best Overall Algorithm: <b>{html.escape(str(leaderboard.index[0]))}</b></li>
<li>Highest Reward: <b>{html.escape(str(best.algorithm))}</b></li>
<li>Fastest Training: <b>{html.escape(str(fastest.algorithm))}</b></li>
</ul>
</body>
</html>
"""
        output.write_text(html_text, encoding="utf-8")
        logger.info("已生成 %s", output)
        return output

    @staticmethod
    def _valid_rows(df: pd.DataFrame) -> pd.DataFrame:
        """过滤出 status=ok 且 final_reward 非空的实验。"""
        if df.empty:
            return df
        if "status" not in df.columns:
            df = df.copy()
            df["status"] = "ok"
        valid = df[df["status"] == "ok"].copy()
        valid = valid[pd.to_numeric(valid["final_reward"], errors="coerce").notna()]
        return valid