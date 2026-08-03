from drl_analyzer.leaderboard import LeaderBoard

board = LeaderBoard()

file = board.generate(

    "results/benchmark.csv"

)

print(file)