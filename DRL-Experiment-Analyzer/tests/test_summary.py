from drl_analyzer.summary import SummaryGenerator



generator = SummaryGenerator()



file = generator.generate(

    "results/benchmark.csv"

)



print(file)