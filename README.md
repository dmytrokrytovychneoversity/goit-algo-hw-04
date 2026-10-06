# goit-algo-hw-04

Homework 4: recursion and sorting algorithms.

## Setup

Python 3.10 or newer. No third-party packages are required. Task 2 uses `turtle` and requires Python with Tk support. Drawing in a window also needs a graphical desktop.

## Tasks

| Task | File | Description |
| ---- | ---- | ----------- |
| 1 | `task_01/task_01.py` | Copy files recursively and group them by extension |
| 2 | `task_02/task_02.py` | Draw the Koch snowflake using recursion |
| 3 | `task_03/task_03.py` | Compare insertion sort, merge sort, and Timsort |

## Run

Run the commands from the repository root.

### Task 1

```bash
python3 task_01/task_01.py /path/to/source
python3 task_01/task_01.py /path/to/source /path/to/destination
```

The default destination is `dist`. Original files are kept. Files without an extension go into `no_extension`. Duplicate names get a numbered suffix, such as `report_1.txt`. Symbolic links and the destination directory are skipped during traversal. Access errors are reported without stopping the remaining files.

### Task 2

```bash
python3 task_02/task_02.py 3
python3 task_02/task_02.py 3 --output snowflake.svg
```

The recursion level can be from 0 to 6. The default is 3. Level 0 draws a triangle. Click inside the window to close it. The `--output` option saves an SVG without opening a window.

### Task 3

```bash
python3 task_03/task_03.py
python3 task_03/task_03.py --output task_03/benchmark_results.csv
```

The script tests sizes of 100, 1,000, 5,000, and 10,000 elements. Each measurement is repeated three times using `timeit`, and the shortest time is recorded. The random seed is 42. All algorithms sort the same data and return a new list. Data generation is excluded from timing.

## Sorting results

Measured with CPython 3.11.6 on macOS, ARM64. Times below are in milliseconds. [Full results](task_03/benchmark_results.csv) are saved in seconds.

| Dataset | Size | Insertion sort | Merge sort | Timsort |
| ------- | ---: | -------------: | ---------: | ------: |
| Random | 100 | 0.091 | 0.085 | 0.003 |
| Random | 1,000 | 10.333 | 1.109 | 0.049 |
| Random | 5,000 | 261.292 | 6.599 | 0.354 |
| Random | 10,000 | 1053.421 | 14.261 | 0.785 |
| Sorted | 10,000 | 0.535 | 8.972 | 0.042 |
| Reversed | 10,000 | 2001.930 | 9.600 | 0.041 |
| Nearly sorted | 10,000 | 0.540 | 9.102 | 0.059 |
| With duplicates | 10,000 | 903.029 | 13.871 | 0.509 |

## Conclusions

- Insertion sort slows down quickly on random and reversed data. Doubling the random input from 5,000 to 10,000 increased its time by 4.03 times, which agrees with O(n²). On sorted data it needs no shifts and runs in O(n).
- Merge sort handles larger inputs better. The same size increase took 2.16 times longer, which agrees with O(n log n).
- Timsort was the fastest on every dataset. It uses insertion sort for short runs and merges them to handle larger inputs. It also takes advantage of existing order, which explains the lower times on sorted and nearly sorted data.
- On 10,000 random elements, Timsort was about 18 times faster than merge sort. Its implementation in C also contributes to this difference. For normal Python tasks, I would use `sorted()` or `list.sort()`.
