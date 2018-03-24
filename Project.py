import searchMethods, waterPump
searcher = searchMethods.astar_search
problem = waterPump.WaterPumpRelaxed(2, 5, 5, 3, 2)
solution = searcher(problem, problem.h)
path = solution.path()
path.reverse()
print(path)