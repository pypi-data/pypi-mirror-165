import pytest
import numpy as np
import types

from chaos_map.chaotic_map import ChaoticMap
from chaos_map.plotting.plotting import ChaoticMapPlot

def double_function(x, r):
    x, y = x
    r, w = r
    return r * x * (1 - x), w * np.sin(np.pi * y)

@pytest.fixture
def chaotic_map_plot():
    chaotic_map = ChaoticMap(double_function)
    return ChaoticMapPlot(chaotic_map)


def test_init_wrong_type_input(chaotic_map_plot):
    """ Check if using a function as input for the class raises the appropriate error
    """
    with pytest.raises(TypeError):
        ChaoticMapPlot(lambda x: x)

@pytest.mark.utility
def test__find_iterable_single_iterable(chaotic_map_plot):
    """Test that the iterable is found"""
    assert chaotic_map_plot._find_iterable_([(1, 2, 3)]) == (0, (1, 2, 3))


@pytest.mark.utility
def test__find_iterable__from_list(chaotic_map_plot):
    """Find the location and iterable when iterable is in a list"""
    assert chaotic_map_plot._find_iterable_([(1, 2), 3, 4]) == (0, (1, 2))
    assert chaotic_map_plot._find_iterable_([1, (3, 4), 5]) == (1, (3, 4))
    assert chaotic_map_plot._find_iterable_([1, 4, 6, (3, 4), 5]) == (3, (3, 4))


@pytest.mark.utility
def test__find_iterable__multiple_iterables(chaotic_map_plot):
    """Find the location and iterable when iterable is in a list"""
    assert chaotic_map_plot._find_iterable_([1, (3, 4, 6), (5, 6), 4]) == (1, (3, 4, 6))
    assert chaotic_map_plot._find_iterable_([1, 2, (5, 6), 7, (9, 10)]) == (2, (5, 6))


@pytest.mark.utility
def test__find_iterable_raises_error_no_iterable(chaotic_map_plot):
    """Test that the iterable is found"""
    with pytest.raises(TypeError):
        chaotic_map_plot._find_iterable_([1, 2, 3, 4])


@pytest.mark.utility
def test__find_iterable_raises_error_empty_input(chaotic_map_plot):
    """Test that the iterable is found"""
    with pytest.raises(TypeError):
        chaotic_map_plot._find_iterable_(tuple())


@pytest.mark.utility
def test__iterator_parameter_gen__returns_generator(chaotic_map_plot):
    """Test that the sequence is finite"""
    r = np.random.uniform(0, 3.99, [1, 20])
    sequence = chaotic_map_plot._iterator_parameter_gen_((r,))
    assert isinstance(sequence, types.GeneratorType)


@pytest.mark.utility
def test__iterator_parameter_gen_single_input(chaotic_map_plot):
    """Test that the sequence is finite"""
    r = (1, 2, 3, 4)
    sequence = chaotic_map_plot._iterator_parameter_gen_((r,))
    print(sequence)
    assert list(sequence) == [(1,), (2,), (3,), (4,)]


@pytest.mark.utility
def test__iterator_parameter_gen_iterator_with_floats(chaotic_map_plot):
    """Test that the sequence is finite"""
    r = (1, 2, 3, 4)
    sequence = chaotic_map_plot._iterator_parameter_gen_((2, r, 3))
    assert list(sequence) == [(2, 1, 3), (2, 2, 3), (2, 3, 3), (2, 4, 3)]


@pytest.mark.utility
def test__iterator_parameter_gen_multiple_iterators(chaotic_map_plot):
    """Test that the sequence is finite"""
    r = (1, 2, 3, 4)
    sequence = chaotic_map_plot._iterator_parameter_gen_((2, r, 3, (1, 2, 3)))
    assert list(sequence) == [
        (2, 1, 3, (1, 2, 3)),
        (2, 2, 3, (1, 2, 3)),
        (2, 3, 3, (1, 2, 3)),
        (2, 4, 3, (1, 2, 3)),
    ]
