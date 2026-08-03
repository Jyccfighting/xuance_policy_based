# DRL Experiment Analyzer

Deep Reinforcement Learning Experiment Analyzer：扫描 WandB 训练日志，加载过程历史，计算指标，导出 CSV/Excel/图表/HTML/Markdown 报告，并支持过程突变/失败事件分析。

## 安装

```bash
pip install -e ".[dev]"
```

## 快速开始

```bash
# 分析 logs 目录，输出到 results，禁用网络（只用本地数据）
drl-analyzer --log-root logs --output results --no-wandb

# 允许通过 WandB API 在线获取过程数据（本地无 history.csv 时自动拉取并缓存）
drl-analyzer --log-root logs --output results

# 额外生成过程分析报告
drl-analyzer --log-root logs --output results --process-report results/process.md
```

也可以使用 Python API：

```python
from drl_analyzer.config import AnalyzerConfig
from drl_analyzer.analyzer import Analyzer

config = AnalyzerConfig(log_root="logs", output_dir="results")
analyzer = Analyzer(config)
experiments = analyzer.analyze()
analyzer.export(experiments)
```

## 输入目录结构

工具按以下结构查找实验（`wandb` 目录名匹配，深度不限）：

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