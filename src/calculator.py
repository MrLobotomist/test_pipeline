"""Простой калькулятор для демонстрации CI-пайплайна."""

from __future__ import annotations


def add(a: float, b: float) -> float:
    """Сложение двух чисел."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Вычитание b из a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Умножение двух чисел."""
    return a * b


def divide(a: float, b: float) -> float:
    """Деление a на b. Выбрасывает ValueError при делении на ноль."""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b


def factorial(n: int) -> int:
    """Вычисление факториала неотрицательного целого числа."""
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
