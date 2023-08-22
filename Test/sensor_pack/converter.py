"""Преобразование значений из одной единицы измерения в другую.
Сonverting values from one unit of measure to another"""


def pa_mmhg(value: float) -> float:
    """Convert air pressure from Pa to mm Hg."""
    return 7.50062E-3 * value