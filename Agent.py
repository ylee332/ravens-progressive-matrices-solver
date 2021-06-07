from TwoDimensionalMatrixSolver import TwoDimensionalMatrixSolver


class Agent:
    def __init__(self):
        pass

    def Solve(self, problem):

        if problem.problemType == '2x2':
            two_dimensional_matrix_solver = TwoDimensionalMatrixSolver(problem)
            return two_dimensional_matrix_solver.solve()

        return -1
