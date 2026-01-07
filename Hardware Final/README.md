# Memory Allocation Algorithms Project

This repository contains the implementation of three memory allocation algorithms:
1. **Best Fit**
2. **Worst Fit**
3. **Next Fit**

It also includes experiments to test their behavior regarding fragmentation and speed.

## Directory Structure
- `experiment_1_trace.py`: Performs the allocation trace test with a fixed sequence.
- `experiment_2_fragmentation.py`: Tests random allocations and a large allocation failure/success scenario.
- `experiment_3_speed.py`: Measures the execution time of each algorithm.

## How to Run the Code
You can run each experiment using Python from the terminal:

### 1. Run Allocation Trace
```bash
python experiment_1_trace.py