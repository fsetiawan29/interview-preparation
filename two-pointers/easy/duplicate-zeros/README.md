# Problem: Duplicate Zeros

## 1. Problem Understanding

### Problem Summary

Given a fixed-length integer array, duplicate every occurrence of `0` by shifting the remaining elements to the right.

The array **cannot grow**. Any elements that move beyond the original length are discarded.

The modification must be done **in-place**, meaning we cannot create another array to store the answer.

### Input

- A fixed-length integer array `arr`

### Output

- Modify `arr` in-place after duplicating every zero.

### Constraints

- `1 <= arr.length <= 10^4`
- `0 <= arr[i] <= 9`

### Example

Input:

```text
arr = [1,0,2,3,0,4,5,0]
```

Output:

```text
[1,0,0,2,3,0,0,4]
```

Manual walkthrough:

```text
Original

[1,0,2,3,0,4,5,0]

Pretend the array can expand forever.

↓

[1,0,0,2,3,0,0,4,5,0,0]

The original array length is only 8.

Keep only the first 8 elements.

↓

[1,0,0,2,3,0,0,4]
```

---

## 2. Brute Force Approach

### Idea

Build a new "expanded" array by walking `arr` and appending each value (or two zeros, for a zero), then keep only the first `len(arr)` entries and copy them back.

### Pseudocode

```text
n = length(arr)
expanded = []

for x in arr
    if x == 0
        expanded.append(0)
        expanded.append(0)
    else
        expanded.append(x)

for i = 0 to n - 1
    arr[i] = expanded[i]
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- One pass builds `expanded`, one pass copies the first `n` entries back into `arr`.

#### Space Complexity

```text
O(n)
```

Why?

- `expanded` can grow up to roughly `2n` entries before being trimmed — a full second array, which the problem's in-place constraint explicitly forbids.

### Why this isn't good enough

This works, but it allocates a second array the problem says not to use. Counting the zeros up front and writing from the back of the *same* array — using a virtual "expanded index" instead of an actual expanded array — achieves the same result with `O(1)` extra space.

---

## 3. Key Insight

### What makes this problem difficult?

Duplicating a zero shifts every element to the right.

If we process from left to right, we overwrite values that haven't been processed yet.

### Key Observation

Every zero increases the **virtual length** of the array by one.

Instead of physically expanding the array, imagine a **virtual expanded array**.

Example:

```text
Original

[1,0,2]

Virtual

[1,0,0,2]
```

The virtual array doesn't actually exist.

We only use it to determine where values should be written.

### Why does this observation help?

Instead of shifting elements one by one, we process the array **from right to left**.

We use:

- `i` → reads from the original array.
- `j` → represents the current position in the virtual expanded array.

This avoids overwriting unprocessed values while using only O(1) extra space.

---

## 4. Mental Model

> What picture should I imagine in my head?

Imagine the array magically expands whenever a zero appears.

```text
Original

1 0 2 3 0

↓

Virtual

1 0 0 2 3 0 0
```

The virtual array does **not** exist.

Think of `j` walking through this imaginary array while `i` walks through the original array.

```text
Original

1 0 2 3 0
        ↑
        i

Virtual

1 0 0 2 3 0 0
            ↑
            j
```

Whenever `j` points outside the real array, simply skip writing.

Once `j` enters the real array, begin writing values.

Explanation:

- `i` always points to a real element.
- `j` represents where that element belongs in the virtual array.
- Write only when `j` is inside the real array.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Count number of zeros
   │
   ▼
Initialize

i = last index of original array
j = last index of virtual array

   │
   ▼
Is arr[i] == 0 ?
   │
 ┌─┴───────────────┐
 │                 │
No                Yes
 │                 │
 ▼                 ▼
Is j inside?    Write first 0 (if inside)
 │                 │
 │                 ▼
 │             Move j left
 │                 │
 ▼                 ▼
Copy value      Write second 0 (if inside)
 │                 │
 ▼                 ▼
Move i,j      Move i,j
```

Explanation of each decision:

- Count zeros to determine the virtual length.
- If the current value is not zero, it occupies one position in the virtual array.
- If the current value is zero, it occupies two positions.
- Write only if `j` is within the bounds of the real array.

---

## 6. Plain English Algorithm

1. Count the number of zeros.
2. Let `i` point to the last element of the original array.
3. Let `j` point to the last position of the virtual expanded array.
4. Process the array from right to left.
5. If the current value is not zero:
   - Write it if `j` is inside the real array.
6. If the current value is zero:
   - Write two zeros if their positions are inside the real array.
7. Continue until every original element has been processed.

---

## 7. Pseudocode

```text
count = number of zeros

i = length(arr) - 1
j = length(arr) + count - 1

while i >= 0

    if arr[i] == 0

        if j < length(arr)
            arr[j] = 0

        j--

        if j < length(arr)
            arr[j] = 0

        i--
        j--

    else

        if j < length(arr)
            arr[j] = arr[i]

        i--
        j--
```

---

## 8. Python Solution

```python
class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        zeros = arr.count(0)

        i = len(arr) - 1
        j = len(arr) + zeros - 1

        while i >= 0:
            if arr[i] == 0:
                if j < len(arr):
                    arr[j] = 0
                j -= 1

                if j < len(arr):
                    arr[j] = 0

                i -= 1
                j -= 1
            else:
                if j < len(arr):
                    arr[j] = arr[i]

                i -= 1
                j -= 1
```

---

## 9. Dry Run

Example:

```text
arr = [1,0,2,3,0]

zeros = 2

Virtual array:
[1,0,0,2,3,0,0]
```

| Step | Pointer(s) | Current Values | Action | Array State | Why? |
|------|------------|----------------|--------|-------------|------|
| 1 | i=4, j=6 | 0 | Skip (outside) | [1,0,2,3,0] | Virtual index outside real array |
| 2 | i=3, j=4 | 3 | Write 3 | [1,0,2,3,3] | Index 4 exists |
| 3 | i=2, j=3 | 2 | Write 2 | [1,0,2,2,3] | Index 3 exists |
| 4 | i=1, j=2 | 0 | Write 0 twice | [1,0,0,2,3] | Zero occupies two virtual positions |
| 5 | i=0, j=0 | 1 | Write 1 | [1,0,0,2,3] | Final element |

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- One pass to count zeros.
- One pass from right to left.
- Total work is proportional to the number of elements.

### Space Complexity

```text
O(1)
```

Why?

- No additional array is created.
- Only a few variables (`zeros`, `i`, and `j`) are used.
