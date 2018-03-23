import searchMethods, waterPump
searcher = searchMethods.astar_search
problem = waterPump.WaterPumpRelaxed(3,5,5,3,2)
solution = searcher(problem, problem.h)