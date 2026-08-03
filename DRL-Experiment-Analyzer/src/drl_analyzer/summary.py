"""
summary.py

生成 Markdown 摘要报告：最佳/最快/最稳、算法排名、分环境分析。
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from drl_analyzer.scoring import compute_leaderboard

logger = logging.getLogger(__name__)


class SummaryGenerator:
    """从 benchmark.csv 生成 summary.md。"""

    def generate(self, csv_file, output="results/summary.md") -> Path:
        """
        参数
        ----
        csv_file : str | Path
            benchmark.csv 路径。
        output : str | Path
            输出 Markdown 路径。
        """
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)

        df = pd.read_csv(csv_file)
        valid = self._valid_rows(df)

        if valid.empty:
            output.write_text("# DRL Benchmark Summary\n\n暂无有效实验数据。\n", encoding="utf-8")
            return output

        # 最佳 / 最快 / 最稳
        best = valid.sort_values("final_reward", ascending=False).iloc[0]
        fastest = valid.sort_values("runtime").iloc[0]
        stable_df = valid.dropna(subset=["stability"])
        stable = stable_df.sort_values("stability", ascending=False).iloc[0] if not stable_df.empty else None

        # 按 reward 排名
        ranking = valid.sort_values("final_reward", ascending=False)
        ranking_text = "\n".join(
            f"{i}. {row.algorithm} ({row.environment}) - reward={row.final_reward:.3f}"
            for i, row in enumerate(ranking.itertuples(), 1)
        )

        # 分环境分析
        env_text = ""
        for env in valid.environment.dropna().unique():
            sub = valid[valid.environment == env].sort_values("final_reward", ascending=False)
            top = sub.iloc[0]
            env_text += f"\n## {env}\n\n最佳算法: **{top.algorithm}**\n\n最终奖励: {top.final_reward:.3f}\n"

        stable_text = f"**{stable.algorithm}** ({stable.stability:.3f})" if stable is not None else "暂无有效数据"

        # 算法排行榜
        leaderboard = compute_leaderboard(valid)
        lb_text = "| Rank | Algorithm | Overall Score |\n|---|---|---|\n" + "\n".join(
            f"| {row.Rank} | {row.Index} | {row.overall_score:.3f} |"
            for row in leaderboard.itertuples()
        )

        md = f"""
# DRL Benchmark Summary

## Overall Performance

实验数量: {len(valid)}

最佳 Reward 算法: **{best.algorithm}** ({best.environment}) - {best.final_reward:.3f}

最高稳定性: {stable_text}

最快训练: **{fastest.algorithm}** - {fastest.runtime:.3f}s

---

## Algorithm Leaderboard

{lb_text}

---

## Reward Ranking

{ranking_text}

---

## Environment Analysis

{env_text}
"""
        output.write_text(md, encoding="utf-8")
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