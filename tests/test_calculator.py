"""Тесты для модуля calculator."""

import pytest

from src.calculator import add, divide, factorial, multiply, subtract


class TestAdd:
    def test_positive_numbers(self) -> None:
        assert add(2, 3) == 5

    def test_negative_numbers(self) -> None:
        assert add(-1, -2) == -3

    def test_zero(self) -> None:
        assert add(0, 0) == 0

    def test_floats(self) -> None:
        assert add(1.5, 2.5) == 4.0


class TestSubtract:
    def test_positive_result(self) -> None:
        assert subtract(5, 3) == 2

    def test_negative_result(self) -> None:
        assert subtract(3, 5) == -2


class TestMultiply:
    def test_positive_numbers(self) -> None:
        assert multiply(3, 4) == 12

    def test_by_zero(self) -> None:
        assert multiply(5, 0) == 0


class TestDivide:
    def test_normal_division(self) -> None:
        assert divide(10, 2) == 5.0

    def test_float_result(self) -> None:
        assert divide(7, 2) == 3.5

    def test_division_by_zero(self) -> None:
        with pytest.raises(ValueError, match="Деление на ноль"):
            divide(1, 0)


class TestFactorial:
    def test_zero(self) -> None:
        assert factorial(0) == 1

    def test_one(self) -> None:
        assert factorial(1) == 1

    def test_five(self) -> None:
        assert factorial(5) == 120

    def test_negative(self) -> None:
        with pytest.raises(ValueError, match="неотрицательных"):
            factorial(-1)
