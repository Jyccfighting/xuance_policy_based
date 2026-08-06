# DRL Experiment Analyzer

Deep Reinforcement Learning Experiment Analyzer：扫描 WandB 训练日志，加载过程历史，计算指标，导出 CSV/Excel/图表/HTML/Markdown 报告，并支持过程突变/失败事件分析。

## 一键运行（推荐）

打开项目根目录的 `run.py`，在 VS Code 中点击右上角 ▶ 即可运行全部功能；也可以在终端执行：

```bash
python run.py
```

跳过某一步：打开 `run.py` 中的 `run_all()`，把不需要的那一行注释掉即可，例如：

```python
# step_plots(config, benchmark_csv)   # 不生成图表
# step_process(config, experiments, process_report)  # 不生成过程分析
```

常用命令：

```bash
# 默认路径 logs -> results
python run.py

# 指定路径并禁用 WandB 在线获取（只用本地数据）
python run.py --log-root logs --output results --no-wandb

# 额外生成过程分析报告
python run.py --log-root logs --output results --process-report results/process.md

# 加载 YAML 配置
python run.py --config config.yaml
```

## 系统架构

```text
run.py / cli.py（总入口）
        │
        ▼
logs/ ──► Scanner ──► Experiment[]
                          │
                          ▼
             ┌──── HistoryLoader ────────────┐
             │ 1) files/history.csv (缓存)    │
             │ 2) run-*.wandb 本地解析        │
             │ 3) WandB API（超时+重试+缓存） │
             └──────────────┬────────────────┘
                            ▼
                  MetricsCalculator ──► Metrics
                            │
                            ▼
                   BenchmarkExporter ──► benchmark.csv / report.xlsx
                            │
          ┌─────────────────┼──────────────────┐
          ▼                 ▼                  ▼
   SummaryGenerator  ReportGenerator    SummaryPlotter
     summary.md        report.html        figures/*.png
          │                 │                  │
          └───── process_analyzer（过程分析）───┘
                     突变/异常/失败事件/时间线
```

模块职责：

| 模块 | 职责 |
|---|---|
| `scanner.py` | 扫描日志目录，识别 WandB run，构造 Experiment |
| `history_loader.py` | 按 本地 CSV → 本地 .wandb → WandB API 加载过程历史 |
| `metrics.py` | 从历史计算 reward/loss/收敛/稳定性等指标 |
| `scoring.py` | 归一化与综合分，排行榜统一口径 |
| `exporter.py` | 导出 benchmark.csv / report.xlsx |
| `summary.py` / `report.py` | 生成 Markdown / HTML 报告 |
| `visualization/summary_plot.py` | 生成全部汇总图表 |
| `process_analyzer.py` | 过程突变、NaN、事件提取与失败定位 |
| `run.py` | 一键运行总入口，步骤可注释跳过 |

## 安装

```bash
pip install -e ".[dev]"
```

也可以不安装，直接使用 `run.py`（它会自动把 `src` 加入 `sys.path`）。

## 输入目录结构

```text
logs/
    algorithm/
        environment/
            wandb/
                run-xxx/
                    files/config.yaml
                    files/wandb-summary.json
                    run-xxx.wandb
```

## 过程数据获取优先级

1. `files/history.csv`：本地缓存或训练端导出，最快。
2. `run-*.wandb`：本地 WandB 二进制过程文件（best-effort 解析，无需网络）。
3. WandB API：完整逐 step 历史，成功后自动写入 `history.csv` 缓存，之后可离线复用。

## 配置

通过 `--config config.yaml` 加载配置，命令行参数优先：

```yaml
log_root: logs
output_dir: results
wandb:
  enabled: true
  entity: your_name
  project: your_project
  timeout: 30
  retries: 2
  cache_history: true
```

## 输出

- `results/benchmark.csv`：每个实验一行，含 `status` 列（ok / no_history / no_metrics）。
- `results/report.xlsx`：汇总 sheet + 每个环境一个 sheet。
- `results/summary.md`：最佳/最快/最稳、排名、分环境分析。
- `results/report.html`：HTML 报告。
- `results/figures/*.png`：汇总图、学习曲线、热力图、过程时间线。
- `results/process.md`（可选）：过程分析，突变点 / NaN / reward 回退 / 日志事件。

## 测试

```bash
pytest
```

测试全部使用合成数据和临时目录，不访问真实网络。