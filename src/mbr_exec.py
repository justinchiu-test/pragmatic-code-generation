from .utils import execute_testcase

class MBRExec:
    def __init__(self, programs, tests, value_matrix = None):
        self.reranked_programs = self.select_programs(programs, tests, value_matrix)
       
    def select_programs(self, programs, tests, value_matrix):
        mbr_scores = [0 for _ in range(len(programs))]
        for i in range(len(programs)):
            for j in range(len(programs)):
                if i != j:
                    p_i, p_j = programs[i], programs[j]
                    l_ij = 0
                    for t, test in enumerate(tests):
                        if value_matrix is None:
                            exec_i = execute_testcase(p_i, test)
                            exec_j = execute_testcase(p_j, test)
                        else:
                            exec_i = value_matrix[t][i]
                            exec_j = value_matrix[t][j]
                       
                        if exec_i != exec_j:
                            l_ij = 1
                            break
                    mbr_scores[i] += l_ij
        
        program_scores = list(zip(programs, mbr_scores))
        program_scores.sort(key = lambda x : x[1])
        return [program_score[0] for program_score in program_scores]


if __name__ == '__main__':
    import numpy as np
    p1 = "def count(s): return len([c for c in s if c.islower()])"
    p2 = """
def count(string):
    cnt = 0
    for ch in string:
        if ch.islower():
            cnt += 1
    return cnt
"""
    p3 = "def count(s): return len(s)"

    t = "assert count(\"abc1\") == 3"

    programs = [p1, p2, p3]
    tests = [t]

    value_matrix = np.array([
        [3, 3, 4]
    ])

    mbr = MBRExec(programs, tests, value_matrix)