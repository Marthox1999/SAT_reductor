from os import walk, getcwd, system
from os.path import join,sep
from glob import glob

SOLVER_PATH =  join(getcwd(), "syrup")

SOLVER_CMD = "cd " + SOLVER_PATH + " &&" + " ./glucose-syrup-24.sh"
SOLVER_CMD = " ".join([SOLVER_CMD,"{}"])

print(SOLVER_CMD)

SAT_PROBLEMS = glob('./InstanciasSAT/*', recursive=True)
X_SAT_PROBLEMS = glob('./X-SAT/*', recursive=True)

for i in X_SAT_PROBLEMS:
    problem = join(getcwd(), i)
    system(SOLVER_CMD.format(problem))
