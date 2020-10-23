from os import walk, getcwd, system
from os.path import join, sep
from glob import glob
from datetime import datetime, timedelta

import pandas as pd

SOLVER_PATH = join(getcwd(), "syrup")

SOLVER_CMD = "cd " + SOLVER_PATH + " &&" + " ./glucose-syrup-24.sh"
SOLVER_CMD = " ".join([SOLVER_CMD, "{}"])

print(SOLVER_CMD)

SAT_PROBLEMS = glob('./InstanciasSAT/*', recursive=True)
X_SAT_PROBLEMS = glob('./X-SAT/*', recursive=True)
print(SAT_PROBLEMS)
satexecTimes = []
xsatexecTimes = []

for i in SAT_PROBLEMS:
    begin_solving = datetime.now()
    problem = join(getcwd(), i)
    system(SOLVER_CMD.format(problem))
    end_solving = datetime.now()
    satexecTimes.append(
        [i.rsplit("/", 1)[1], (end_solving-begin_solving).total_seconds()])

df = pd.DataFrame(data=satexecTimes, columns=['File', 'Time'])
df.to_csv('sat_output.csv', index=False)

for i in X_SAT_PROBLEMS:
    begin_solving = datetime.now()
    problem = join(getcwd(), i)
    system(SOLVER_CMD.format(problem))
    end_solving = datetime.now()
    xsatexecTimes.append(
        [i.rsplit("/", 1)[1], (end_solving-begin_solving).total_seconds()])

df = pd.DataFrame(data=xsatexecTimes, columns=['File', 'Time'])
df.to_csv('xsat_output.csv', index=False)
