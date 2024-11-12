from unittest.mock import patch
from log_decorator import log
import pytest

RANDINT_RETURN_RESULT = 128


# Фикстурa
@pytest.fixture(autouse=True)
def mock_randint():
    """Фикстура для имитации значения randint"""
    with patch("random.randint", return_value=RANDINT_RETURN_RESULT):
        yield


def test_log_without_template(capsys, mock_randint):
    @log
    def test_func():
        """My Docstring"""
        return "Test result"

    assert test_func() == "Test result"
    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == """My Docstring"""
    captured = capsys.readouterr()
    assert captured.out == f"test_func - {RANDINT_RETURN_RESULT}c!\n"


def test_log_with_string_template(capsys, mock_randint):
    @log("Execution time: {0}s")
    def test_func():
        return "Test result"

    assert test_func() == "Test result"
    captured = capsys.readouterr()
    assert captured.out == f"Execution time: {RANDINT_RETURN_RESULT}s\n"


def test_log_with_args(capsys, mock_randint):
    @log
    def complex_function(arg1, arg2):
        return f"Result: {arg1} + {arg2}"

    assert complex_function(1, 2) == "Result: 1 + 2"
    captured = capsys.readouterr()
    assert captured.out == f"complex_function - {RANDINT_RETURN_RESULT}c!\n"


def test_log_with_kwargs(capsys, mock_randint):
    @log
    def kwargs_function(**kwargs):
        return f"kwargs: {kwargs}"

    assert kwargs_function(a=1, b=2) == "kwargs: {'a': 1, 'b': 2}"
    captured = capsys.readouterr()
    assert captured.out == f"kwargs_function - {RANDINT_RETURN_RESULT}c!\n"
