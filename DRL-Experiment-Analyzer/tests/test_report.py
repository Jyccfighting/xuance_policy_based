from drl_analyzer.report import ReportGenerator


generator = ReportGenerator()


file = generator.generate(

    csv_file=
    "D:/document/coding/policy/DRL-Experiment-Analyzer/results/benchmark.csv",

    figure_dir=
    "D:/document/coding/policy/DRL-Experiment-Analyzer/results",

    output=
    "D:/document/coding/policy/DRL-Experiment-Analyzer/results/report.html"

)


print(file)