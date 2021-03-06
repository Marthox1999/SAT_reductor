from os import system, getcwd, walk, remove
from os.path import join, sep, exists
from glob import glob
import copy
import sys


class Reader():
    def __init__(self):
        actual_directory = getcwd()  # <- Get the current directory path (../SAT/Reductor)
        # <- Get the parent directory (../SAT)
        parent_directory = sep.join(actual_directory.split(sep)[1:-1])
        # <- Apeend SO separator to access the folder
        parent_directory = join(sep, parent_directory)

        # <- Joins the parent directory with InstanciasSAT to get into (../SAT/instanciasSAT)
        self.SAT_instances_directory = join(parent_directory, "InstanciasSAT")
        # <- Store all the SAT problems in format Problems->[Problem->[Clause->[variables]]]
        self.problems = []

        # <- Create an array of all the files into (../SAT/instanciasSAT)
        self.SAT_instances = glob(
            self.SAT_instances_directory + '/*.cnf', recursive=True)

    def read_file(self):

        for SAT_instance in self.SAT_instances:
            SAT_file = open(
                join(self.SAT_instances_directory, SAT_instance), 'r')
            problem = []  # <- Stores the problem using the following format Problem->[Clause->[variables]]

            for line in SAT_file:
                if line[0] == "c":  # <- Ignore comments
                    continue
                # <- Identify the first problems and store it (verify no other problem is in the file)
                if line[0] == "p" and not problem:
                    problem.append(line[:-1].split(" "))
                    continue
                # <- Identify the rest of problems and store them (We assumed can be more than 1 problem per file)
                if line[0] == "p":
                    problem.append(line[:-1].split(" "))
                    problem = []
                    continue
                if problem:  # <- Store the clauses for the current problem
                    problem.append(line[:-3].split(" "))

            self.problems.append(problem)

    def export_solution(self, solution, solution_name, p):
        if exists("../X-SAT/"+solution_name):
            remove("../X-SAT/"+solution_name)

        solution_file = open("../X-SAT/"+solution_name, "x")

        clauses = len(solution)

        prob_conf = " ".join(["p", "cnf", str(p), str(clauses), "\n"])
        solution_file.write(prob_conf)

        aux_clause = ""
        for clause in solution:
            aux_clause = copy.copy(clause)
            aux_clause.append("0\n")
            aux_clause_str = " ".join(aux_clause)
            solution_file.write(aux_clause_str)
        solution_file.close()
        # lo hacemos luego :D
