import itertools
import copy


class Solver():
    def __init__(self, problem, x_target):
        self.solution = []
        self.var_count = 0
        self.problem = problem
        self.x_target = x_target

    def reduct_sat(self):
        for clause in self.problem:
            if clause[0] == 'p':  # <- Problem configuration (ignore)
                self.var_count = int(clause[2])
                continue
            clause_size = len(clause)  # <- Calculate clause size
            if clause_size == self.x_target:  # <- If clause size is already on X-SAT add to the solution
                self.solution.append(clause)
                continue
            if clause_size < self.x_target:  # <- If clause size is less than X-SAT
                # <- Calculate the missing variables to convert from clause-size to X-SAT
                missing_variables = self.x_target - clause_size
                partial_solution = self.generate_clause_lesser(
                    clause, missing_variables)
                for clause in partial_solution:
                    # <- Stores on the solution the new clauses (see generate_clause)
                    self.solution.append(clause)
                continue
            else:
                missing_variables = clause_size - 3
                missing_clauses = clause_size - 2
                self.generate_clause_greater(
                    clause, missing_variables, missing_clauses)
                # do something else

    def generate_clause_lesser(self, clause, missing_variables):
        new_variables = []  # <- Variable to store the new variables
        new_clauses = []  # <- Variable to store the new clauses
        boolean_combinations = list(itertools.product([False, True],
                                                      repeat=missing_variables))  # <- Generates all the posible 2^missing_variables boolean combinations

        # Example of boolean combinations:
        # for missing_variables = 3
        # Boolean combinations = [[False, False, False],
        #                         [False, False, True],
        #                         [False, True, False],
        #                         [False, True, True],
        #                         [True, False, False],
        #                         [True, False, True],
        #                         [True, True, False],
        #                         [True, True, True]]

        # <- Iterate for all the variables we need to add
        for _ in range(missing_variables):
            self.var_count += 1
            # <- Add an unique number to each of the needed variables following the format v#
            new_variables.append(str(self.var_count))

        # <- Iterate over all the boolean combinatios generated previously [..., [..., boolean_value, ...],...]
        for boolean_values in boolean_combinations:
            new_clause = []
            # <- Creates a copy of the clause
            new_clause = copy.deepcopy(clause)
            # <- Iterates over each of the boolean values [..., boolean_value, ...]
            for index, boolean_value in enumerate(boolean_values):
                if boolean_value:  # <- if boolean is True means that we need to add the new variable but positive
                    # <- here we add the positive variable to the new_clause
                    new_clause.append(new_variables[index])
                else:  # <- if boolean is not True means that we need to add the new variable but negative
                    # <- here we add the negative variable to the new_clause
                    new_clause.append("-"+new_variables[index])
            # <- After iterate over the first boolean_values we add the new_clause to new_clauses variable
            new_clauses.append(new_clause)

        return new_clauses

    def generate_clause_greater(self, clause, missing_variables, missing_clauses):
        new_variables = []
        aux_solution = []

        self.var_count = self.var_count + 1

        for i in range(self.var_count, self.var_count + missing_variables):
            new_variables.append(str(i))
            new_variables.append("-"+str(i))

        self.var_count = self.var_count + missing_variables - 1

        clause_position = 0
        new_variables_position = 0

        for new_clause_index in range(missing_clauses):
            new_clause = []
            if new_clause_index == 0:
                new_clause.append(clause[clause_position])
                new_clause.append(clause[clause_position+1])
                new_clause.append(new_variables[new_variables_position])
                new_variables_position += 1
                clause_position += 2
                aux_solution.append(new_clause)
                continue
            if new_clause_index == missing_clauses-1:
                new_clause.append(new_variables[new_variables_position])
                new_clause.append(clause[clause_position])
                new_clause.append(clause[clause_position+1])
                new_variables_position += 1
                clause_position += 2
                aux_solution.append(new_clause)
                break
            else:
                new_clause.append(new_variables[new_variables_position])
                new_clause.append(clause[clause_position])
                new_clause.append(new_variables[new_variables_position+1])
                clause_position += 1
                new_variables_position += 2
                aux_solution.append(new_clause)

        for new_clause in aux_solution:
            clause_size = len(new_clause)
            # <- Calculate the missing variables to convert from clause-size to X-SAT
            missing_variables = self.x_target - clause_size
            partial_solution = self.generate_clause_lesser(
                new_clause, missing_variables)
            for clause in partial_solution:
                # <- Stores on the solution the new clauses (see generate_clause)
                self.solution.append(clause)
            continue
