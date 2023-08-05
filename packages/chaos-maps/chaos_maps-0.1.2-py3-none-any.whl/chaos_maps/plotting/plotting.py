""" This module provides utilities for plotting and visualizing chaotic maps."""
from typing import Union, Tuple, Iterable

import warnings
import matplotlib.pyplot as plt

from typing import List, Tuple, TypeVar, Union
Figure = TypeVar("Figure")

from chaos_maps.chaotic_maps import ChaoticMap


class ChaoticMapPlot:
    """This class takes a chaotic map object and provides the
    methods for creating plots of its dynamical behavior.
    """

    def __init__(self, chaotic_map: ChaoticMap):
        """Initialize the object for generating the plots

        Args:
            chaotic_map (ChaoticMap): The chaotic map object

        Raises:
            TypeError -- If the chaotic map is not of type ChaoticMap
        """
        if not isinstance(chaotic_map, ChaoticMap):
            raise TypeError("ChaoticMap object required as input")
        self.map = chaotic_map


    @staticmethod
    def _find_iterable_(
        pams: Tuple[Union[Iterable, float]]
    ) -> Union[Tuple[Iterable, int], None]:
        """Locate the first iteratble element of a tuple

        Args:
        pams (tuple[Union[Iterable, float]]): The tuple to search

        Returns:
        The first iterable and its index on the input tuple

        Raises:
        ValueError: If no iterable is found
        """
        loc, par_values = None, None
        for num, item in enumerate(pams):
            if hasattr(item, "__iter__"):
                loc, par_values = num, item
                return loc, par_values
        if par_values is None:
            raise TypeError("No iterator is given")


    @staticmethod
    def _iterator_parameter_gen_(pams: Tuple[Union[Iterable, float]]) -> Tuple[float]:
        """Generate every possible combination of tuples from a tuple containing an iterable

        Args:
        pams (tuple[Union[Iterable, float]]): The tuple to search

        Yields:
        The next parameter tuple
        """

        loc, par_values = ChaoticMapPlot._find_iterable_(pams)
        for par_value in par_values:
            yield tuple(par_value if i == loc else pams[i] for i in range(len(pams)))


    def plot_trajectory(
        self,
        init_point: Tuple[float],
        parameter: Tuple[float],
        num_points: int = 100,
        which_var: int = 0,
        fig: Union[Figure, None] = None,
        **kwargs
    ) -> Figure:
        """ Plot the trajectory of the selected system variable

        Args:
        init_point:
        The initial point of the trajectory

        parameter:
        The tuple representing the parameters for the cahotic map

        num_points (Optional):
        The number of trajectrory points to be plotted (Default 2000)

        which_var (Optional):
        The variable to be plotted (Default 0)

        fig (Optional):
        The figure in which the scatter plot is to be created.

        kwags:
        Named arguments to alter the plot appearance, refer to matplotlib
        scatter plot for options.


        Returns:

        fig (Figure):
        The figure object that contains the return map
        """
        seq_gen = self.map.trajectory(init_point, parameter, num_points)

        points = [point[which_var] for point in seq_gen]

        if fig is None:
            fig = plt.figure()
        else:
            plt.figure(fig.number)

        plt.plot(points, **kwargs)

        return fig

    def bifurcation_dict(
        self,
        start_point: Tuple[float],
        parameters: Tuple[Union[float, Iterable]],
        num_points: int = 500,
        points_to_skip: int = 50,
    ):
        """Get a dictionary with parameter values as key and trajectories.

        Args:
            start_point (Tuple[float]): The starting point of the trajectory
            parameters (Tuple[Union[float, Iterable]]): The parameters to vary
            num_points (int, optional): The number of points for each trajectory. Defaults to 500.
            points_to_skip (int, optional): Number of points to discard. Defaults to 50.

        Returns:
            dict: A dictionary with parameter values as keys and generators of
            trajectory objects as values

        Raises:
            ValueError: If the number of points to be discarded are more that
            the number of points to generate
        """
        if points_to_skip >= num_points:
            raise ValueError(
                "The number of total points generated has to be greater than"
                + "the number of points skipped"
            )

        bif_dict = {}
        pam_loc, _ = self._find_iterable_(parameters)
        for pam in self._iterator_parameter_gen_(parameters):
            try:
                point_gen = self.map.trajectory(start_point, pam, num_points)
                for _ in range(points_to_skip):
                    next(point_gen)
                bif_dict[pam[pam_loc]] = point_gen
            except Exception as exc:  # If an exception is raised skip this parameter
                warnings.warn(f"Skipping parameter {pam} due to {exc}")
                continue
        return bif_dict

    def bifurcation_diagram(
        self, start_point: Tuple[float], pams: Tuple[Union[float, Iterable]], **kwargs
    ):
        """Create the bifurcation diagram for the chaotic map on a
        given set of parameters.

        Args:
            start_point (Tuple[float]): The starting point of the trajectory
            pams (Tuple[Union[float, Iterable]]): The parameters to vary
            **kwargs: Additional keyword arguments for the plot

        Returns:
            matplotlib.pyplot.Figure: The figure object
        """

        which_var = kwargs.pop("which_var", 0)

        num_points = kwargs.pop("num_points", 500)

        points_to_skip = kwargs.pop("points_to_skip", 50)

        fig = kwargs.pop("fig", None)

        # Find the position of the iterable in the pams tuple
        loc, _ = self._find_iterable_(pams)

        # Create the bifurcation dictionary, where the keys are the parameter tuples
        bif_dict = self.bifurcation_dict(start_point, pams, num_points, points_to_skip)

        if fig is None:
            fig = plt.figure()
        for key, value in bif_dict.items():
            pam = key
            points = [val[which_var] for val in value]
            ell = len(points)
            plt.scatter(ell * [pam], points, **kwargs)
        return fig

    def return_map(
        self,
        init_point: Tuple[float],
        parameter: Tuple[float],
        num_points: int =2000,
        which_var: int = 0,
        fig: Figure = None,
        **kwargs
    ) -> Figure:
        """Plot the return map diagram of the given chaotic map on a given or new figure

        The return map is a diagram in which the x axis represent a the value at k-th step
        and the y axis is the value of the trajectory at the (k+1)-th step.
        The figure is thus a scatter plots where (x, y) are subsequent trajectory points.


        Args:

        init_point:
        The initial point of the trajectory

        parameter:
        The tuple representing the parameters for the cahotic map

        num_points (Optional):
        The number of trajectrory points to be plotted (Default 2000)

        which_var (Optional):
        The variable to be plotted (Default 0)

        fig (Optional):
        The figure in which the scatter plot is to be created.

        kwags:
        Named arguments to alter the plot appearance, refer to matplotlib
        scatter plot for options.


        Returns:

        fig (Figure):
        The figure object that contains the return map
        """
        seq_gen = self.map.trajectory(init_point, parameter, num_points)
        points1 = [point[which_var] for point in seq_gen]
        points2 = points1[1:]
        points1 = points1[:-1]
        if fig is None:
            fig = plt.figure()
        else:
            plt.figure(fig.number)
        plt.scatter(points1, points2, **kwargs)
        return fig

    @staticmethod
    def _cobweb_line_(xs: float, ys: float, zs: float
    ) -> Tuple[List[float], List[float]]:
        """Create a line for the cobweb plot

        Given three consecutive trajectory points for one variable, create the
        lists that define the trajectory line for the cobweb diagram.
        """

        x_locs = [xs, ys, ys]
        y_locs = [ys, ys, zs]

        return x_locs, y_locs

    def cobweb_diagram(
        self,
        init_point: Tuple[float],
        parameter: Tuple[float],
        num_points: int = 50,
        which_var: int = 0,
        fig: Union[Figure, None] = None,
        **kwargs
    ) -> Figure:
        """ Create the cobweb diagram for the selected initial condition and parameter
        values of the map.

        For details about the Cobweb diagram, refer to

        Args:
        init_point:
        The initial point of the trajectory

        parameter:
        The tuple representing the parameters for the cahotic map

        num_points (Optional):
        The number of trajectrory points to be plotted (Default 2000)

        which_var (Optional):
        The variable to be plotted (Default 0)

        fig (Optional):
        The figure in which the scatter plot is to be created.

        kwags:
        Named arguments to alter the plot appearance, refer to matplotlib
        scatter plot for options.


        Returns:

        fig (Figure):
        The figure object that contains the return map
        """
        seq_gen = self.map.trajectory(init_point, parameter, num_points)

        points = []
        for k in range(num_points):
            point = next(seq_gen)
            points.append(point[which_var])
        # points = [point[which_var] for point in seq_gen]
        x_plot = []
        y_plot = []
        for k in range(len(points) - 2):

            xs, ys, zs = points[k : k + 3]
            x_n, y_n = self._cobweb_line_(xs, ys, zs)
            x_plot.extend(x_n)
            y_plot.extend(y_n)

        if fig is None:
            fig = plt.figure()
        else:
            plt.figure(fig.number)

        plt.plot(x_plot, y_plot, **kwargs)
        plt.xlim(min(x_plot), max(x_plot))
        plt.ylim(min(y_plot), max(y_plot))
        plt.plot([min(x_plot), max(x_plot)], [min(x_plot), max(x_plot)], "k")

        return fig

    def lyapunov_exponent_dict(
        self,
        start_point: Tuple[float],
        parameters: Tuple[Union[Tuple, float]],
        num_points: int = 500,
        points_to_skip: int = 50,
    ) -> dict:
        """Get a dictionary with parameter values as key and the lyapunov exponent as value.

        Args:
            start_point (Tuple[float]): The starting point of the trajectory
            parameters (Tuple[Union[Tuple, float]]): The parameters to vary
            num_points (int, optional): The number of points for each trajectory. Defaults to 500.
            points_to_skip (int, optional): Number of points to discard. Defaults to 50.

        Returns:
            dict: A dictionary with parameter values as keys and generators of

        Raises:
            ValueError: If the number of points to be discarded are more that the number of points kept
        """
        if points_to_skip >= num_points:
            raise ValueError(
                "The number of total points generated has to be greater than the"
                + "number of points skipped"
            )
        le_dict = {}
        for pam in self._iterator_parameter_gen_(parameters):
            try:
                le_now = self.map.approximate_lyapunov_exponents(
                    start_point, pam, num_points=1000, discard=100, h=1e-04
                )
                pam_loc, _ = self._find_iterable_(parameters)
                le_dict[pam[pam_loc]] = le_now
            except Exception as exc:
                warnings.warn(f"Skipping parameter {pam} due to {exc}")
                continue
        return le_dict

    def lyapunov_exponent_plot(
        self,
        start_point: Tuple[float],
        parameters: Tuple[Union[Tuple, float]],
        num_points: int = 500,
        points_to_skip: int = 50,
        fig: Union[Figure, None] = None,
        ** kwargs
        ) -> Figure:
        """Get a dictionary with parameter values as key and the lyapunov exponent as value.

        Args:
            start_point (Tuple[float]): The starting point of the trajectory
            parameters (Tuple[Union[Tuple, float]]): The parameters to vary
            num_points (int, optional): The number of points for each trajectory. Defaults to 500.
            points_to_skip (int, optional): Number of points to discard. Defaults to 50.
            fig (Figure, optional): The figure in which the Lyapunov exponent is plotted
            kwargs: plt.plot arguments
        Returns:
            A plt figure object containing the plot of the lyapunov exponent for the selected parameter

        """
        le_dict = self.lyapunov_exponent_dict(
            start_point,
            parameters,
            num_points,
            points_to_skip,
            )

        if fig is None:
            fig = plt.figure()
        else:
            plt.figure(fig.number)

        plt.plot(le_dict.keys(), le_dict.values(), **kwargs)

        return fig
