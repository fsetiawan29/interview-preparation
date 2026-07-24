# Problem: Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

## 1. Problem Understanding

### Problem Summary

Given an integer array `arr`, an integer `k`, and an integer `threshold`, count the number of contiguous subarrays of length `k` whose average is greater than or equal to `threshold`.

### Input

- An integer array `arr`
- An integer `k`
- An integer `threshold`

### Output

- An integer: the count of length-`k` subarrays whose average is `>= threshold`.

### Constraints

- `1 <= arr.length <= 10^5`
- `1 <= arr[i] <= 10^4`
- `1 <= k <= arr.length`
- `0 <= threshold <= 10^4`

### Example

Input:

```text
arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4
```

Output:

```text
3
```

Explanation: Sub-arrays [2,5,5],[5,5,5] and [5,5,8] have averages 4, 5 and 6 respectively. All are >= threshold = 4.

Manual walkthrough:

```text
arr: 2 2 2 2 5 5 5 8

[2,2,2] sum=6  avg=2.0  < 4
[2,2,2] sum=6  avg=2.0  < 4
[2,2,5] sum=9  avg=3.0  < 4
[2,5,5] sum=12 avg=4.0  >= 4  <- count
[5,5,5] sum=15 avg=5.0  >= 4  <- count
[5,5,8] sum=18 avg=6.0  >= 4  <- count

-> 3
```

---

# 2. Key Insight

## What makes this problem difficult?

Computing a fresh average (with a division) for every one of the `O(n)` windows works, but floating-point division per window is unnecessary overhead, and recomputing each window's sum from scratch would make it `O(n * k)`.

## Key Observation

`window_sum / k >= threshold` is mathematically equivalent to `window_sum >= k * threshold`. So instead of dividing on every window, multiply `k` and `threshold` together **once** into a fixed integer `limit`, and just compare sums against it.

Example:

```text
k = 3, threshold = 4 -> limit = 12
window [2,5,5] sum = 12 -> 12 >= 12 -> counts
```

## Why does this observation help?

The comparison becomes pure integer arithmetic with no repeated division, and the window sum itself is maintained incrementally (drop the outgoing element, add the incoming one), so each slide is `O(1)` and the whole scan is `O(n)`.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture a window of fixed width `k` sliding across the array, carrying a running sum. At each position, that sum is compared against a precomputed threshold-times-`k` value — no division needed inside the loop.

```text
arr:  2  2  2  2  5  5  5  8
            [-----]
     window_sum = 12   limit = k * threshold = 12
     12 >= 12 -> qualifies, count++

slide ->

arr:  2  2  2  2  5  5  5  8
               [-----]
     window_sum = 12 - 2 + 5 = 15   15 >= 12 -> qualifies, count++
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, right = k - 1
window_sum = sum(arr[0..k-1])
limit = k * threshold
count = 0
   │
   ▼
Is right < len(arr) ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is window_sum >= limit ?   Return count
 │
┌─┴───────┐
│         │
Yes       No
│         │
▼         │
count += 1│
│         │
└────┬────┘
     ▼
Is right == len(arr) - 1 ?
     │
  ┌──┴──────┐
  │         │
 Yes        No
  │         │
  ▼         ▼
break     Slide: window_sum -= arr[left]
          window_sum += arr[right + 1]
          left += 1, right += 1
          │
          └──▶ (back to "Is right < len(arr) ?")
```

Explanation of each decision:

- `limit = k * threshold` is computed once, replacing a per-window division with a per-window comparison.
- `window_sum >= limit` is checked *before* sliding, so every window position of size `k` gets counted exactly once.
- Stopping when `right` reaches the last index avoids sliding past the end of the array.

---

# 5. Plain English Algorithm

1. Set `left = 0` and `right = k - 1` — the first window covers indices `0` through `k - 1`.
2. Compute `window_sum` as the sum of that first window, and `limit = k * threshold`.
3. While `right` is within the array:
   - If `window_sum >= limit`, increment `count`.
   - If `right` is already the last index, stop sliding.
   - Otherwise, remove `arr[left]` and add `arr[right + 1]` to `window_sum`, then advance both `left` and `right`.
4. Return `count`.

---

# 6. Pseudocode

```text
left = 0
right = k - 1
window_sum = sum(arr[0..k-1])
limit = k * threshold
count = 0

while right < length(arr)
    if window_sum >= limit
        count++

    if right == length(arr) - 1
        break

    window_sum -= arr[left]
    window_sum += arr[right + 1]

    left++
    right++

return count
```

---

# 7. Python Solution

```python
class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        left = 0
        right = k - 1
        window_sum = sum(arr[:k])
        limit = k * threshold

        count = 0
        while right < len(arr):
            if window_sum >= limit:
                count += 1

            if right == len(arr) - 1:
                break

            window_sum -= arr[left]
            window_sum += arr[right + 1]

            left += 1
            right += 1

        return count
```

---

# 8. Dry Run

Example:

```text
arr = [2, 2, 2, 2, 5, 5, 5, 8], k = 3, threshold = 4

limit = k * threshold = 12
```

| Step | left, right | window_sum | >= limit? | count | Action |
|------|-------------|------------|-----------|-------|--------|
| 1 | 0, 2 | 6 | No | 0 | slide: sum -= arr[0]=2, += arr[3]=2 -> 6 |
| 2 | 1, 3 | 6 | No | 0 | slide: sum -= arr[1]=2, += arr[4]=5 -> 9 |
| 3 | 2, 4 | 9 | No | 0 | slide: sum -= arr[2]=2, += arr[5]=5 -> 12 |
| 4 | 3, 5 | 12 | Yes | 1 | slide: sum -= arr[3]=2, += arr[6]=5 -> 15 |
| 5 | 4, 6 | 15 | Yes | 2 | slide: sum -= arr[4]=5, += arr[7]=8 -> 18 |
| 6 | 5, 7 | 18 | Yes | 3 | right == last index (7) -> break |

Result: `count = 3`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(arr)`; the initial window sum is computed once in `O(k)`.
- Each subsequent slide does `O(1)` work, and there are `O(n)` slides total.

### Space Complexity

```text
O(1)
```

Why?

- Only `window_sum`, `limit`, `count`, and two pointers are used.
- No additional array or data structure is created.
