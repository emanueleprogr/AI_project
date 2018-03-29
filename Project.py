import searchMethods, waterPump


searcher = searchMethods.astar_search
problem = waterPump.WaterPumpDistance(8, 8, 4, 4)
solution = searcher(problem)
path = solution.path()
path.reverse()
print(path)
