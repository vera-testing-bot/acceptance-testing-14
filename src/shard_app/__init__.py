"""Trivial module so an acceptance shard repo has code to change."""


def add(left: int, right: int) -> int:
    """Return the sum of two integers."""
    return left + right


def clamp(value: float, low: float, high: float) -> float:
    """Return ``value`` bounded to the closed interval ``[low, high]``."""
    return max(low, min(value, high))
