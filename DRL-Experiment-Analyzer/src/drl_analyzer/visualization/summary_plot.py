"""
summary_plot.py

统一绘图模块：汇总柱状图、学习曲线、热力图、综合分图、过程时间线。
原来的 benchmark/efficiency/runtime/stability/reward/comparison 单文件绘图全部合并到这里。
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # 无显示环境也能保存图片

import matplotlib.pyplot as plt
import pandas as pd

from drl_analyzer.metrics import MetricsCalculator
from drl_analyzer.scoring import compute_leaderboard, weighted_score

logger = logging.getLogger(__name__)


class SummaryPlotter:
    """集中管理实验汇总图表。"""

    def __init__(self, save_dir="results/figures"):
        """save_dir 为图片输出目录，不存在时自动创建。"""
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self._metrics = MetricsCalculator()

    # ---------------- 公共接口 ----------------

    def plot_all(self, csv_file):
        """生成全部汇总图。"""
        self.plot_average_reward(csv_file)
        self.plot_average_runtime(csv_file)
        self.plot_average_stability(csv_file)
        self.plot_average_efficiency(csv_file)
        self.plot_win_count(csv_file)
        self.plot_overall_score(csv_file)
        self.plot_final_reward(csv_file)

    # ---------------- 数据清洗 ----------------

    @staticmethod
    def _clean_df(csv_file) -> pd.DataFrame:
        """读取 CSV 并只保留 status=ok、final_reward 非空的实验。"""
        df = pd.read_csv(csv_file)
        if "status" in df.columns:
            df = df[df["status"] == "ok"]
        return df.dropna(subset=["final_reward"])

    # ---------------- 通用绘图 ----------------

    def _save(self, fig, name):
        """保存图片并关闭 figure。"""
        fig.tight_layout()
        fig.savefig(self.save_dir / name)
        plt.close(fig)

    def _bar(self, data, ylabel, title, name, ascending=None):
        """通用柱状图。"""
        if ascending is not None:
            data = data.sort_values(ascending=ascending)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(data.index.astype(str), data.values)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.tick_params(axis="x", rotation=30)
        self._save(fig, name)

    # ---------------- 汇总图 ----------------

    def plot_average_reward(self, csv_file):
        """各算法平均最终奖励。"""
        df = self._clean_df(csv_file)
        data = df.groupby("algorithm")["final_reward"].mean()
        self._bar(data, "Average Final Reward", "Average Final Reward", "average_reward.png", ascending=False)

    def plot_average_runtime(self, csv_file):
        """各算法平均运行时长。"""
        df = self._clean_df(csv_file)
        data = df.groupby("algorithm")["runtime"].mean()
        self._bar(data, "Average Runtime (s)", "Average Runtime", "average_runtime.png")

    def plot_average_stability(self, csv_file):
        """各算法平均稳定性。"""
        df = self._clean_df(csv_file)
        data = df.groupby("algorithm")["stability"].mean().dropna()
        self._bar(data, "Average Stability (%)", "Average Stability", "average_stability.png", ascending=False)

    def plot_average_efficiency(self, csv_file):
        """各算法平均样本效率（达到收敛的步数，越小越好）。"""
        df = self._clean_df(csv_file)
        data = df.groupby("algorithm")["sample_efficiency"].mean().dropna()
        self._bar(data, "Average Sample Efficiency (steps)", "Average Sample Efficiency", "average_sample_efficiency.png")

    def plot_final_reward(self, csv_file):
        """每个实验的最终奖励柱状图。"""
        df = self._clean_df(csv_file)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df["algorithm"].astype(str), df["final_reward"])
        ax.set_title("Final Reward")
        ax.set_ylabel("Reward")
        ax.tick_params(axis="x", rotation=45)
        self._save(fig, "final_reward.png")

    def plot_win_count(self, csv_file):
        """各算法在环境中的胜场次数。"""
        df = self._clean_df(csv_file)
        winners = df.loc[df.groupby("environment")["final_reward"].idxmax()]
        data = winners["algorithm"].value_counts()
        self._bar(data, "Number of Wins", "Algorithm Win Count", "win_count.png", ascending=False)

    def plot_overall_score(self, csv_file):
        """各算法综合分（使用 scoring.compute_leaderboard）。"""
        df = self._clean_df(csv_file)
        score = compute_leaderboard(df)
        if score.empty:
            return
        self._bar(score["overall_score"], "Overall Score", "Overall Algorithm Ranking", "overall_score.png", ascending=False)

    # ---------------- 学习曲线 ----------------

    def plot_learning_curve(self, histories, env_name, smooth_window=50):
        """
        画某环境的平滑学习曲线。

        参数
        ----
        histories : list[dict]
            每项 {"algorithm": str, "history": DataFrame}。
        env_name : str
        smooth_window : int
            滑动平均窗口。
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        for item in histories:
            history = item["history"]
            if history is None or history.empty:
                continue
            reward = self._metrics.extract_reward(history)
            if reward is None:
                continue
            smooth = reward.rolling(smooth_window, min_periods=1).mean()
            ax.plot(smooth, label=item["algorithm"])
        ax.set_xlabel("Training Steps")
        ax.set_ylabel("Average Episode Reward")
        ax.set_title(f"{env_name} Learning Curve")
        ax.legend()
        ax.grid()
        self._save(fig, f"{env_name}_smooth_learning_curve.png")

    # ---------------- 环境对比图 ----------------

    def plot_heatmap(self, csv_file, env_name):
        """某环境下算法 x 指标 的热力图（runtime 越小越好已反转）。"""
        df = self._clean_df(csv_file)
        df = df[df.environment == env_name]
        if df.empty:
            return
        metrics = ["final_reward", "runtime", "stability"]
        table = df.set_index("algorithm")[metrics].apply(pd.to_numeric, errors="coerce")
        table = (table - table.min()) / (table.max() - table.min() + 1e-8)
        table["runtime"] = 1 - table["runtime"]

        fig, ax = plt.subplots(figsize=(8, 5))
        im = ax.imshow(table, aspect="auto")
        ax.set_xticks(range(len(metrics)), metrics)
        ax.set_yticks(range(len(table.index)), table.index)
        fig.colorbar(im)
        self._save(fig, f"{env_name}_heatmap.png")

    def plot_score(self, csv_file, env_name):
        """某环境下各实验综合分（排序后绘制，修复旧版顺序错位）。"""
        df = self._clean_df(csv_file)
        df = df[df.environment == env_name].copy()
        if df.empty:
            return
        score = weighted_score(df)
        result = pd.DataFrame({"algorithm": df["algorithm"].values, "score": score.values})
        result = result.sort_values("score", ascending=False)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(result["algorithm"].astype(str), result["score"])
        ax.set_ylabel("Overall Score")
        ax.set_title(f"{env_name} Score")
        ax.tick_params(axis="x", rotation=30)
        self._save(fig, f"{env_name}_score.png")

    # ---------------- 过程时间线 ----------------

    def plot_process_timeline(self, history, events, name="process"):
        """
        画 reward 曲线，并在异常事件位置画红色竖线。

        参数
        ----
        history : pd.DataFrame
        events : list[dict]
            analyze_process() 返回的 events。
        name : str
            输出文件名前缀。
        """
        if history is None or history.empty:
            return
        reward = self._metrics.extract_reward(history)
        if reward is None:
            return
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(reward, label="reward")
        for e in events:
            step = e.get("step")
            if step is not None:
                ax.axvline(step, color="red", alpha=0.6, linestyle="--")
        ax.set_xlabel("Step")
        ax.set_ylabel("Reward")
        ax.set_title(f"{name} Process Timeline")
        ax.legend()
        ax.grid()
        self._save(fig, f"{name}_process_timeline.png")