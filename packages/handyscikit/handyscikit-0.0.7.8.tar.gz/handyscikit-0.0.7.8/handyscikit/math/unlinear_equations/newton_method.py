import math
import numpy as np

class UnlinearEquations:
    def __init__(self):
        self.__converge = 1e-6
        self.__forward_delta = 1e-10
        self.__iterate_matrix = None
        self.__iterate_steps = 0
        self.__method = "n_point_secant"
        self.__method_list = ["newton", "discrete_newton", "n_point_secant"]
        self.__result = None

    def set_converge_error(self, converge):
        self.__converge = converge

    def set_method(self, method_name):
        if method_name in self.__method_list:
            self.__method = method_name
        else:
            print("There is no this kind of method!")
            exit(7)

    def solve(self, funcs, init_value, funcs_jacobi=None):
        # [Check] Init_value type.
        if (not isinstance(init_value, np.ndarray)):
            print ("Please input a ndarry as init_value!")
            exit(7)
        # [Load] Init_value.
        self.__result = init_value

        # Choose solve method.
        if self.__method==self.__method_list[0]:
            if funcs_jacobi is None:
                print("Must give funcs_jacobi for newton method!")
                exit(7)
            self.__newton_solver(funcs, init_value, funcs_jacobi)
        elif self.__method==self.__method_list[1]:
            self.__discrete_newton_solver(funcs, init_value)
        elif self.__method==self.__method_list[2]:
            self.__n_point_secant_solver(funcs, init_value)

        print("[Unlinear Equations] Solving method:", self.__method)
        print("[Unlinear Equations] Iteration steps:", self.__iterate_steps)
        print("[Unlinear Equations] Converge erroe:", self.__converge)

        return self.__result

    def __newton_solver(self, funcs, init_value, funcs_jacobi):
        # Main loop.
        while True:
            # Store last value.
            result_ago = self.__result.copy()
            # Iterate one step.
            self.__result = result_ago - np.matmul(np.linalg.inv(funcs_jacobi(result_ago)), funcs(result_ago))
            # Stop condition.
            if np.linalg.norm(funcs(self.__result))<self.__converge:
                break
            # Plus iteration steps.
            self.__iterate_steps += 1

    def __discrete_newton_solver(self, func, init_value):
        # Initialize iterate matrix.
        self.__iterate_matrix = np.zeros([init_value.size, init_value.size])
        # Main loop.
        while True:
            # Store last value.
            result_ago = self.__result.copy()
            # Calculate f(result_age).
            f = func(result_ago)
            f_norm = np.linalg.norm(f)
            # Stop condition.
            if f_norm < self.__converge:
                break
            # Assemble iterate matrix.
            for i in range(init_value.size):
                result_tmp = result_ago.copy()
                result_tmp[i] += f_norm*self.__forward_delta
                self.__iterate_matrix[:, i] = (func(result_tmp) - f)/(f_norm*self.__forward_delta)
            # Forward.
            self.__result = result_ago - np.matmul(np.linalg.inv(self.__iterate_matrix), f)
            # Plus iteration.
            self.__iterate_steps += 1


    def __n_point_secant_solver(self, func, init_value):
        # Initialize iterate matrix.
        self.__iterate_matrix = np.zeros([init_value.size, init_value.size])
        # Initialize first step.
        f_init = func(self.__result)
        f_init_norm = np.linalg.norm(f_init)*self.__forward_delta
        for i in range(init_value.size):
            result_tmp = self.__result.copy()
            result_tmp[i] += f_init_norm
            self.__iterate_matrix[:, i] = (func(result_tmp) - f_init)/f_init_norm
        # Forward.
        self.__result = self.__result - np.matmul(np.linalg.inv(self.__iterate_matrix), f_init)

        # Main loop.
        while True:
            # Store last value.
            result_ago = self.__result.copy()
            # Calculate f(result_ago).
            f = func(result_ago)
            f_norm = np.linalg.norm(f)
            # Stop condition.
            if f_norm<self.__converge:
                break
            # Interpolated point value.
            result_tmp = result_ago.copy()
            result_tmp[self.__iterate_steps%init_value.size] += f_norm*self.__forward_delta
            # Construct iterate matrix.
            self.__iterate_matrix[:, self.__iterate_steps%init_value.size] = (func(result_tmp) - f)/(f_norm*self.__forward_delta)
            # Forward.
            self.__result = result_ago - np.matmul(np.linalg.inv(self.__iterate_matrix), f)
            # Plus iteration.
            self.__iterate_steps += 1