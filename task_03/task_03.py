"""Compare insertion sort, merge sort and Python's built-in Timsort."""

import argparse
import csv
import platform
import random
import timeit
from pathlib import Path


def insertion_sort(values: list[int]) -> list[int]:
    """Sort a copy by inserting each item into the sorted prefix."""
    result = values.copy()
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def merge_sort(values: list[int]) -> list[int]:
    """Recursively sort halves and merge them into a new list."""
    if len(values) <= 1:
        return values.copy()
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    result = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def make_datasets(size: int, seed: int) -> dict[str, list[int]]:
    """Build reproducible inputs with different ordering and duplicates."""
    rng = random.Random(seed + size)
    ordered = list(range(size))
    nearly_sorted = ordered.copy()
    for _ in range(max(1, size // 100)):
        index = rng.randrange(size - 1)
        nearly_sorted[index], nearly_sorted[index + 1] = (
            nearly_sorted[index + 1],
            nearly_sorted[index],
        )
    return {
        "random": [rng.randrange(size * 10) for _ in range(size)],
        "sorted": ordered,
        "reversed": ordered[::-1],
        "nearly_sorted": nearly_sorted,
        "duplicates": [rng.randrange(10) for _ in range(size)],
    }


def benchmark(sizes: list[int], repeat: int, number: int, seed: int) -> list[dict]:
    """Validate results and measure the best repeated time per call."""
    algorithms = {
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "timsort": sorted,
    }
    rows = []
    print(f"Python {platform.python_version()} ({platform.python_implementation()})")
    print(f"Platform: {platform.platform()}")
    print(f"Seed: {seed}. Repeats: {repeat}. Sorts per repeat: {number}.")
    print(
        f"{'Dataset':<16} {'Size':>7} {'Insertion (ms)':>16} {'Merge (ms)':>13} {'Timsort (ms)':>13}"
    )
    for size in sizes:
        for name, values in make_datasets(size, seed).items():
            expected = sorted(values)
            row = {"dataset": name, "size": size}
            for label, algorithm in algorithms.items():
                original = values.copy()
                if algorithm(values) != expected or values != original:
                    raise AssertionError(f"{label} failed for {name}, size {size}")
                timer = timeit.Timer(lambda: algorithm(values))
                row[label] = min(timer.repeat(repeat=repeat, number=number)) / number
            rows.append(row)
            print(
                f"{name:<16} {size:>7} {row['insertion_sort'] * 1000:>16.6f} "
                f"{row['merge_sort'] * 1000:>13.6f} {row['timsort'] * 1000:>13.6f}"
            )
    return rows


def main() -> None:
    """Run benchmarks and optionally save per-call seconds as CSV."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sizes", nargs="+", type=int, default=[100, 1000, 5000, 10000]
    )
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--number", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, help="CSV output path")
    args = parser.parse_args()
    if any(size < 2 for size in args.sizes):
        parser.error("all sizes must be at least 2")
    if args.repeat < 1 or args.number < 1:
        parser.error("repeat and number must be positive")

    rows = benchmark(args.sizes, args.repeat, args.number, args.seed)
    if args.output:
        try:
            with args.output.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
        except OSError as error:
            parser.exit(1, f"Cannot save CSV: {error}\n")
        print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
