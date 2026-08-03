from drl_analyzer.report import ReportGenerator



generator = ReportGenerator()


file = generator.generate(

    "results/benchmark.csv",

    "results/figures",

    "results/report.html"

)


print(
    file
)