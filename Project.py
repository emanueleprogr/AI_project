import searchMethods, waterPump


searcher = searchMethods.astar_search
problem = waterPump.WaterPumpAdmissible(3, 5, 5, 3, 2)
solution = searcher(problem)
path = solution.path()
path.reverse()
print(path)
