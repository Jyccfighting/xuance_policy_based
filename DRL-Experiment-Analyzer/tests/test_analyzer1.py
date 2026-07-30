from drl_analyzer.analyzer import Analyzer
from drl_analyzer.exporter import BenchmarkExporter


analyzer = Analyzer(
    "D:/document/coding/policy/logs"
)


experiments = analyzer.analyze()


exporter = BenchmarkExporter()


file = exporter.export_csv(
    experiments
)


print(file)