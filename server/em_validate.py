from em_search import EM_Searcher
searcher = EM_Searcher()
solutions = searcher.validate()
print('------------------Solutions----------------\n')
print('Found', len(solutions), 'solutions')
searcher.visulaize_solutions()