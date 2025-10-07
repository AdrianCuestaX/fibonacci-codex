from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional


def generate_fibonacci(count: int) -> List[int]:
    """Return the Fibonacci sequence with the given number of terms."""
    if count <= 0:
        return []
    if count == 1:
        return [0]

    sequence = [0, 1]
    while len(sequence) < count:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


@dataclass
class FibonacciSummary:
    count: int
    last_value: Optional[int]
    total_sum: int
    golden_ratio: Optional[float]


def summarize(sequence: Iterable[int]) -> FibonacciSummary:
    """Compute basic metrics for a Fibonacci sequence."""
    numbers = list(sequence)
    count = len(numbers)
    last_value = numbers[-1] if numbers else None
    total_sum = sum(numbers)
    golden_ratio = None
    if count >= 2 and numbers[-2] != 0:
        golden_ratio = numbers[-1] / numbers[-2]
    return FibonacciSummary(
        count=count,
        last_value=last_value,
        total_sum=total_sum,
        golden_ratio=golden_ratio,
    )
