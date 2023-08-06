"""Unit test model for the byoml resource."""
import numpy as np
import pandas as pd
import pytest

from waylay.service.byoml.model import model_execution_request_decorator


@model_execution_request_decorator
def execute(*args, **kwargs):
    """Execute the request decorator.

    Transforms any input data into a list, and provides it
    as `instances` in the request body.
    """
    assert args == ('model_name', )
    return kwargs


def test_model_execution_empty_list():
    """Tests the request decorator against an empty list."""
    assert execute('model_name', []) == {'body': {'instances': []}}


def test_model_execution_empty_list_with_body():
    """Tests the request decorator against an empty list, but with a body."""
    assert execute('model_name', [], body={'probabilities': True}) == {
        'body': {'instances': [], 'probabilities': True}
    }


def test_model_execution_body_and_params():
    """Tests the request decorator against a body and params."""
    assert execute(
        'model_name', None,
        body={'probabilities': True, 'instances': 'xxxx'},
        params={'foo': 'bar'}
    ) == {
        'body': {'instances': 'xxxx', 'probabilities': True},
        'params': {'foo': 'bar'}
    }


@pytest.mark.parametrize("test_params", ([], [0, 1], [[0, 1], [2, 3]]))
def test_model_execution_np_array(test_params):
    """Tests the request decorator against a numpy array."""
    assert execute('model_name', np.array(test_params)) == {
        'body': {'instances': test_params}
    }


def test_model_execution_list_of_numpy_array():
    """Tests the request decorator against a list of a numpy array."""
    assert execute('model_name', [np.array([[0, 1], [2, 3]])]) == {
        'body': {'instances': [[[0, 1], [2, 3]]]}
    }


def test_model_execution_empty_pandas_series():
    """Tests the request decorator against an empty pandas Series."""
    assert execute('model_name', pd.Series([], dtype=np.float64)) == {
        'body': {'instances': []}
    }


@pytest.mark.parametrize("test_params", ([0, 1], [[0, 1], [2, 3]]))
def test_model_execution_pandas_series(test_params):
    """Tests the request decorator against a pandas Series."""
    assert execute('model_name', pd.Series(test_params)) == {
        'body': {'instances': test_params}
    }


@pytest.mark.parametrize("test_input,expected", [([], []), ([0, 1], [[0], [1]]), ([[0, 1], [2, 3]], [[0, 1], [2, 3]])])
def test_model_execution_dataframe(test_input, expected):
    """Tests the request decorator against a pandas DataFrame."""
    assert execute('model_name', pd.DataFrame(test_input)) == {
        'body': {'instances': expected}
    }
