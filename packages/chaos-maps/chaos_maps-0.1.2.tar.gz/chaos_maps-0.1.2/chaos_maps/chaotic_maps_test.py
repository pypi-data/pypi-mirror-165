from operator import xor
import numpy as np
import pytest
import types

from chaos_maps.chaotic_map import ChaoticMap


def logistic_function(x, r):
    """Logistic map iteration step"""
    (x,) = x
    (r,) = r
    return (r * x * (1 - x),)


def henon_function(x, r):
    """Henon map iteration step"""
    xn, yn = x
    a, b = r

    x_new = 1 - a * xn**2 + yn
    y_new = b * xn
    return x_new, y_new


@pytest.fixture
def logistic_map():
    return ChaoticMap(logistic_function)


@pytest.fixture
def henon_map():
    return ChaoticMap(henon_function)


@pytest.mark.utility
def test_move_by_d_zero_displace(logistic_map):
    """Test that the sequence is finite"""
    n = np.random.randint(1, 10)
    x = np.random.uniform(0, 1, n)
    x = tuple([w for w in x])
    sequence = logistic_map.move_by_d(x, 0)
    assert sequence == x


@pytest.mark.utility
def test_tuple_dist_tuples_with_known_dist(logistic_map):
    """Test that the sequence is finite"""
    x = (1, 2, 3)
    y = (5, 7, 9)
    assert logistic_map.tuple_dist(x, y) == np.sqrt(
        np.sum((np.array(x) - np.array(y)) ** 2)
    )


@pytest.mark.utility
def test_tuple_dist_tuples_symmetric(logistic_map):
    """Test that the sequence is finite"""
    n = np.random.randint(1, 10)
    x = np.random.uniform(0, 1, n)
    x = tuple([w for w in x])

    y = np.random.uniform(0, 1, n)
    y = tuple([w for w in y])

    assert logistic_map.tuple_dist(x, y) == logistic_map.tuple_dist(y, x)


@pytest.mark.utility
def test_tuple_dist_tuples_with_zero_tuple(logistic_map):
    """Test that the sequence is finite"""
    n = np.random.randint(1, 10)
    x = np.random.uniform(0, 1, n)
    x = tuple([w for w in x])
    y = tuple(n * [0])
    assert logistic_map.tuple_dist(x, y) == np.linalg.norm(np.array(x))


@pytest.mark.utility
def test_tuple_dist_tuples_different_length_error(logistic_map):
    """Test that the sequence is finite"""
    x = (1, 2)
    y = (1, 2, 3)
    with pytest.raises(ValueError):
        logistic_map.tuple_dist(x, y)


@pytest.mark.utility
def test_alter_tuple_value_correct_change(logistic_map):
    """Test if the tuple value is altered correctly"""
    n = np.random.randint(1, 10)
    xs = np.random.uniform(0, 1, n)
    xs = tuple([w for w in xs])
    idx = np.random.randint(0, n)
    displacement = np.random.uniform(0, 1)
    ys = logistic_map.alter_tuple_value(xs, idx, displacement)
    assert ys[idx] == xs[idx] + displacement


@pytest.mark.utility
def test_alter_tuple_value_error_in_empty_tuple(logistic_map):
    with pytest.raises(ValueError):
        assert logistic_map.alter_tuple_value(tuple(), 0, 0)


# * One dimensional tests
@pytest.mark.one_dimensional
def test_next_point_returns_tuple(logistic_map):
    """Test that the next point is a tuple"""
    x, r = np.random.uniform(0, 1), np.random.uniform(0, 3.99)
    assert isinstance(logistic_map.next_point((x,), (r,)), tuple)


@pytest.mark.one_dimensional
def test_next_point_initial_zero(logistic_map):
    """Test that the initial point is zero"""
    print(logistic_map.next_point((0,), (1,)))
    assert logistic_map.next_point((0,), (1,)) == (0,)


@pytest.mark.one_dimensional
def test_next_point_initial_one(logistic_map):
    """Test that the initial point is one"""
    assert logistic_map.next_point((1,), (1,)) == (0,)


@pytest.mark.one_dimensional
def test_next_point_returns_nan(logistic_map):
    """Verify a value error is raised when np.nan is returned"""
    x, r = np.nan, np.random.uniform(0, 3.99)
    with pytest.raises(ValueError):
        logistic_map.next_point((x,), (r,))


@pytest.mark.one_dimensional
def test_gen_sequence_finite_returns_generator(logistic_map):
    """Test that the sequence is finite"""
    x, r = np.random.uniform(0, 1), np.random.uniform(0, 3.99)
    sequence = logistic_map.trajectory((x,), (r,), num_point=2000)
    print(f"x: {x}, r: {r}")
    assert isinstance(sequence, types.GeneratorType)


@pytest.mark.one_dimensional
def test_gen_sequence_finite_returns_correct_length(logistic_map):
    """Test that the sequence is finite"""
    x, r = np.random.uniform(0, 1), np.random.uniform(0, 3.99)
    num_points = np.random.randint(10, 200)
    sequence = logistic_map.trajectory((x,), (r,), num_point=num_points)
    assert len(list(sequence)) == num_points


@pytest.mark.one_dimensional
def test_gen_sequence_infinite_returns_generator(logistic_map):
    """Test that the sequence is finite"""
    x, r = np.random.uniform(0, 1), np.random.uniform(0, 3.99)
    sequence = logistic_map.sequence_gen_infinite((x,), (r,))
    print(f"x: {x}, r: {r}")
    assert isinstance(sequence, types.GeneratorType)


@pytest.mark.one_dimensional
def test_approximate_lyapunov_exponents_negative_value_for_non_chaotic(logistic_map):
    """Test that the sequence is finite"""
    x = np.random.uniform(0, 1)
    r = np.random.uniform(0, 3)
    print(f"Problematic values: x = {x}, r = {r}")
    assert logistic_map.approximate_lyapunov_exponents(x, r) < 0


@pytest.mark.one_dimensional
def test_approximate_lyapunov_exponents_negative_value_for_non_chaotic(logistic_map):
    """Test that the sequence is finite"""
    x = np.random.uniform(0.1, 1)
    r = np.random.uniform(3.9, 3.99)
    print(f"Problematic values: x = {x}, r = {r}")
    assert logistic_map.approximate_lyapunov_exponents((x,), (r,)) > 0


@pytest.mark.one_dimensional
def test_is_divergent_divergent(logistic_map):
    """Test that the sequence is finite"""
    x = np.random.uniform(0.1, 1)
    r = np.random.uniform(5, 9)
    assert logistic_map.is_divergent((x,), (r,))


@pytest.mark.one_dimensional
def test_is_divergent_convergent(logistic_map):
    """Test that the sequence is finite"""
    x = np.random.uniform(0.1, 1)
    r = np.random.uniform(0, 3.99)
    assert not logistic_map.is_divergent((x,), (r,))


# Two dimensional
@pytest.mark.two_dimensional
def test_next_point_returns_tuple(henon_map):
    """Test that the next point is a tuple"""
    x, r = tuple(np.random.uniform(0, 1, 2)), np.random.uniform(0, 3.99, 2)
    print(f"Problematic values: x = {x}, r = {r}")
    assert isinstance(henon_map.next_point(x, r), tuple)


@pytest.mark.two_dimensional
def test_next_point_returns_nan_1(henon_map):
    """Verify a value error is raised when np.nan is returned"""
    x = np.nan, 1
    r = 1, 2
    with pytest.raises(ValueError):
        henon_map.next_point(x, r)


@pytest.mark.two_dimensional
def test_next_point_returns_nan_2(henon_map):
    """Verify a value error is raised when np.nan is returned"""
    x = 0, np.nan
    r = 1, 2
    with pytest.raises(ValueError):
        henon_map.next_point(x, r)


@pytest.mark.two_dimensional
def test_next_point_returns_nan_3(henon_map):
    """Verify a value error is raised when np.nan is returned"""
    x = 0, 0
    r = 1, np.nan
    with pytest.raises(ValueError):
        henon_map.next_point(x, r)


@pytest.mark.two_dimensional
def test_gen_sequence_finite_returns_generator(henon_map):
    """Test that the sequence is finite"""
    x = tuple(np.random.uniform(0, 1, 2))
    r = tuple(np.random.uniform(0, 3.99, 2))
    sequence = henon_map.trajectory(x, r, num_point=2000)
    print(f"x: {x}, r: {r}")
    assert isinstance(sequence, types.GeneratorType)


@pytest.mark.two_dimensional
def test_gen_sequence_finite_returns_correct_length(henon_map):
    """Test that the sequence is finite"""
    x = tuple(np.random.uniform(0, 1, 2))
    r = tuple(np.random.uniform(0, 1, 2))
    num_points = np.random.randint(10, 200)
    sequence = henon_map.trajectory(x, r, num_point=num_points)
    assert len(list(sequence)) == num_points


@pytest.mark.two_dimensional
def test_gen_sequence_infinite_returns_generator(henon_map):
    """Test that the sequence is finite"""
    x = tuple(np.random.uniform(0, 1, 2))
    r = tuple(np.random.uniform(0, 3.99, 2))
    sequence = henon_map.sequence_gen_infinite(x, r)
    print(f"x: {x}, r: {r}")
    assert isinstance(sequence, types.GeneratorType)


@pytest.mark.two_dimensional
def test_is_divergent_divergent(henon_map):
    """Test that the sequence is finite"""
    x = tuple(np.random.uniform(0.1, 1, 2))
    r = tuple(np.random.uniform(5, 9, 2))
    assert henon_map.is_divergent(x, r)


@pytest.mark.two_dimensional
def test_is_divergent_convergent(henon_map):
    """Test that the sequence is finite"""
    x = tuple(np.random.uniform(0.1, 0.1, 2))
    r = tuple(np.random.uniform(0, 0.3, 2))
    assert not henon_map.is_divergent(x, r)
