""" ...
"""

from typing import Union, Tuple, Iterable

import itertools
import numpy as np


class ChaoticMap:
    """Define, iterate and analyze the dynamics of discrete chaotic maps"""

    def __init__(self, iteration):
        """Define a chaotic map using the iteration function"""
        self.iteration = iteration

    def next_point(self, point: Tuple[float], pams: Tuple[float]):
        """Get the next trajectory point

        Args:
        point (tuple[float]): The initial trajectory point
        pams (tuple[float]): Parameters for the map

        Returns:
        The next trajectory point

        Raises:
        ValueError: If any point generated is NaN
        """
        next_point = self.iteration(point, pams)
        if np.any(np.isnan(next_point)):
            raise ValueError("Encountered NaN value in iteration")
        return next_point

    def trajectory(
        self, point: Tuple[float], pams: Tuple[float], num_point: int = 2000
    ):
        """Generate a finite sequence of trajectory points

        Args:
        point (tuple[float]): The initial trajectory point
        pams (tuple[float]): Parameters for the map
        num_point (int, optional): number of points to generate, Default=2000

        Returns:
        A generator of trajectory points

        Raises:
        ValueError: If any element of the sequence is NaN
        """

        for _ in range(num_point):
            if np.any(np.isnan(point)):
                raise ValueError("Encountered NaN in infinite sequence")
            yield point
            point = self.iteration(point, pams)

    def sequence_gen_infinite(self, point: Tuple[float], pams: Tuple[float]):
        """Generate an infinite sequence of trajectory points

        Args:
        point (tuple[float]): The initial trajectory point
        pams (tuple[float]): Parameters for the map

        Returns:
        A generator of trajectory points

        Raises:
        ValueError: If any point generated is NaN
        """
        while True:
            if np.any(np.isnan(point)):
                raise ValueError("Encountered NaN")
            yield point
            point = self.iteration(point, pams)

    
    @staticmethod
    def move_by_d(point: Tuple[float], displace: float) -> Tuple[float]:
        """Alter the coordinates of a tuple point to move it by eucledean distance d

        Args:
        point (tuple[float]): The point to move
        displace (float): The distance to move the point

        Returns:
        The moved point
        """
        new_point = [
            point[k] + (-1) ** k * displace / np.sqrt(len(point))
            for k in range(len(point))
        ]
        new_point = tuple(new_point)
        return new_point

    @staticmethod
    def tuple_dist(tuple_1: Tuple[float], tuple_2: Tuple[float]) -> float:
        """Calculate the eucledean distance between two tuples

        Args:
        tuple_1 (tuple[float]): The first tuple
        tuple_2 (tuple[float]): The second tuple

        Returns:
        (float) The eucledean distance between the two tuples
        """

        if not len(tuple_1) == len(tuple_2):
            raise ValueError("Tuples must be of the same length to define distance")
        array_1, array_2 = np.array(tuple_1), np.array(tuple_2)
        return np.linalg.norm(array_1 - array_2)

    @staticmethod
    def alter_tuple_value(point: Tuple[float], idx: int, displacement: float):
        """Change a value of a tuple element at a specific index"""
        if not point:
            raise ValueError("Empty tuple entered")
        
        new_point = [
            point[k] + displacement if k == idx else point[k] for k in range(len(point))
        ]
        new_point = tuple(new_point)
        return new_point

    def approximate_partial_derivative(
        self, point: Tuple[float], pams: Tuple[float], **kwargs
    ) -> float:
        """Approximate the partial derivative of the chaotic map at a point

        The method used here is the finite difference method.
        I actually have no idea what algorithm is implemented tho, need to check.

        Args:
        point (tuple[float]): The point to calculate the partial derivative at
        pams (tuple[float]): The parameters of the function
        which_num (int, optional): The index of the numerator, Default=0
        which_den (int, optional): The index of the denominator, Default=0
        step (float, optional): The step size, Default=1e-4

        Returns:
        The partial derivative of the function at the point
        """
        which_num = kwargs.get("which_num", 0)
        which_den = kwargs.get("which_den", 0)
        step = kwargs.get("step", 1e-4)

        moved_point_1 = ChaoticMap.alter_tuple_value(point, which_den, step)
        moved_point_2 = ChaoticMap.alter_tuple_value(point, which_den, -step)

        next_moved_point_1 = self.iteration(moved_point_1, pams)
        next_moved_point_2 = self.iteration(moved_point_2, pams)

        return (next_moved_point_1[which_num] - next_moved_point_2[which_num]) / (
            2 * step
        )

    def approximate_jacobian(
        self, point: Tuple[float], pam: Tuple[float], step: float = 1e-4
    ) -> np.array:
        """Approximate the Jacobian of the chaotic map at a point

        The method used here is the finite difference method.

        Args:
        point (tuple[float]): The point to calculate the Jacobian at
        pam (tuple[float]): The parameters of the function
        step (float, optional): The step size, Default=1e-4

        Returns:
        The Jacobian of the function at the point
        """
        ind = range(len(point))
        j = np.array(
            [
                self.approximate_partial_derivative(
                    point, pam, which_num=i, which_den=j, step=step
                )
                for i in ind
                for j in ind
            ]
        )
        j = j.reshape((len(point), len(point)))
        return j

    def approximate_lyapunov_exponents(
        self, point: Tuple[float], pams: Tuple[float], **kwargs
    ) -> np.array:
        """Approximate the Lyapunov exponents of the chaotic map at a point

        Args:
        point (tuple[float]): The point to calculate the Lyapunov exponents at
        pams (tuple[float]): The parameters of the function
        discard (int, optional): The number of iterations to discard, Default=100
        num_points (int, optional): The number of points to use in the approximation, Default=1000

        step (float, optional): The step size, Default=1e-4
        """

        num_points = kwargs.get("num_points", 1000)
        discard = kwargs.get("discard", 100)
        step = kwargs.get("step", 1e-04)

        gen = self.trajectory(point, pams, num_points)
        gen = itertools.islice(gen, discard, None)

        diagonal_elements = []

        q_diagonal = np.identity(len(point))

        for traj_poin in gen:
            jacobian = self.approximate_jacobian(traj_poin, pams, step)
            updated_q = jacobian @ q_diagonal
            q_diagonal, r_factor = np.linalg.qr(updated_q)
            diagonal_elements.append(np.diagonal(r_factor))

        les = np.zeros(diagonal_elements[0].shape)

        for diag in diagonal_elements:
            les += np.log(np.abs(diag))

        return les / num_points

    def is_divergent(
        self, point: Tuple[float], pams: Tuple[float], num_points: int = 2000
    ) -> bool:
        """Check if intial condition and parameter selections lead to divergent trajectory.

        Args:
        point (tuple[float]): The initial condition
        pams (tuple[float]): The parameters of the chaotic map
        num_points (int, optional): The number of points to check, Default=2000

        Returns:
        (bool) True if the trajectory is divergent, False otherwise
        """
        try:
            sequence = list(self.trajectory(point, pams, num_point=num_points))
        except ValueError:
            return True

        if -np.inf in min(sequence) or np.inf in max(sequence):
            return True
        return False
