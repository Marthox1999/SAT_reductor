#!/venv/pyvenv.cfg
# -*- coding: utf-8 -*-
from read_file import *
from solver import *

# Folder Structure

#SAT/ <-Parent Folder
#├── InstanciasSAT <- store one of the 100 problems to test
#│   └── SAT-Problems
#├── InstanciasSAT_FINAL <- store all the problems
#│   ├── SAT-Problems
#├── Reductor <- Store de source code of the project
#│   ├── main.py <- Main, here the magic of merge all the other things occurs
#│   ├── read_file.py <- Read and understand the all the files in InstanciasSAT in the following format Problems->[Problem->[Clause->[variables]]]
#│   └── solver.py <- Converts SAT to X-SAT (actually is only implemented but not proved for k < x, missing k > x. {k=clause size, x=SAT target})
#├── X-SAT <- Here will be stored the solutions of converts SAT to X-SAT
#└── reducir.sh <- Script that prepares the environment and executes the solver for an input given by the proffesor

if __name__ == '__main__':
    readed_problems = Reader()
    readed_problems.read_file()
    problem = readed_problems.problems
    SAT_instances = readed_problems.SAT_instances
    
    for index,p in enumerate(problem):
        solution = Solver(p, 5)
        solution.reduct_sat()
        #print("Solucion:")
        '''
        for clause in solution.solution:
            print(clause)
            if clause is None:
                break
        '''
        readed_problems.export_solution(solution.solution, SAT_instances[index], solution.var_count)