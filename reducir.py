from os import walk, getcwd, system
from os.path import join, sep
from glob import glob
from datetime import datetime, timedelta

import subprocess
import pandas as pd

begin_time = datetime.now()

SOLVER_PATH = join(getcwd(), "syrup")

SOLVER_CMD = "cd " + SOLVER_PATH + " &&" + " ./glucose-syrup-24.sh"
SOLVER_CMD = " ".join([SOLVER_CMD, "{}"])

SAT_PROBLEMS = glob('./InstanciasSAT/*.cnf', recursive=True)
X_SAT_PROBLEMS = glob('./X-SAT/*.cnf', recursive=True)

satexecTimes = []
xsatexecTimes = []

for i in SAT_PROBLEMS:
    print("Solving SAT problems")
    cpu_time = None
    real_time = None
    satisfying = None
    problem = join(getcwd(), i)
    sat_output = subprocess.Popen(SOLVER_CMD.format(
        problem), shell=True, stdout=subprocess.PIPE)
    subprocess_return = sat_output.stdout.read().decode("utf-8").split("\n")

    for j in subprocess_return:
        if ("SATISFIABLE" in j):
            satisfying = j.split(" ")[1]
        if ("cpu time" in j):
            cpu_time = j.split(" ")[5]
        if ("real time" in j):
            real_time = j.split(" ")[4]

    xsatexecTimes.append(
        [i.rsplit("/", 1)[1], cpu_time, real_time, satisfying])

df = pd.DataFrame(data=xsatexecTimes, columns=[
    'File', 'cpu time', 'real time', 'Satisfying'])
df.to_csv('sat_output.csv', index=False)

for i in X_SAT_PROBLEMS:
    print("Solving X-SAT problems")
    cpu_time = None
    real_time = None
    satisfying = None
    problem = join(getcwd(), i)
    xsat_output = subprocess.Popen(SOLVER_CMD.format(
        problem), shell=True, stdout=subprocess.PIPE)
    subprocess_return = xsat_output.stdout.read().decode("utf-8").split("\n")

    for j in subprocess_return:
        if ("SATISFIABLE" in j):
            satisfying = j.split(" ")[1]
        if ("cpu time" in j):
            print(j.split(" ")[5])
            cpu_time = j.split(" ")[5]
        if ("real time" in j):
            real_time = j.split(" ")[4]

    xsatexecTimes.append(
        [i.rsplit("/", 1)[1], cpu_time, real_time, satisfying])

df = pd.DataFrame(data=xsatexecTimes, columns=[
                  'File', 'cpu time', 'real time', 'Satisfying'])
df.to_csv('xsat_output.csv', index=False)

end_time = datetime.now()
print((end_time-begin_time).total_seconds())
