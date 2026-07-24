# Problem: Majority Element

## 1. Problem Understanding

### Problem Summary

Given an array `nums` of size `n`, return the majority element — the element that appears more than `⌊n / 2⌋` times. The array is guaranteed to always have a majority element.

### Input

- An integer array `nums`

### Output

- The integer value that appears more than `n / 2` times.

### Constraints

- `n == nums.length`
- `1 <= n <= 5 * 10^4`
- `-10^9 <= nums[i] <= 10^9`
- The array is guaranteed to have a majority element.

### Example

Input:

```text
nums = [2,2,1,1,1,2,2]
```

Output:

```text
2
```

Manual walkthrough:

```text
nums = [2,2,1,1,1,2,2]   (n=7, threshold = 7 // 2 = 3)

Counts as we scan: 2:1, 2:2, 1:1, 1:2, 1:3, 2:3, 2:4

The count of 2 reaches 4, which is greater than threshold 3
-> 2 is the majority element
```

---

## 2. Brute Force Approach

### Idea

For every candidate value in `nums`, count how many times it occurs by scanning the whole array again, and return the first one whose count exceeds `n / 2`.

### Pseudocode

```text
n = length(nums)
threshold = n // 2

for i = 0 to n - 1
    count = 0
    for j = 0 to n - 1
        if nums[j] == nums[i]
            count += 1

    if count > threshold
        return nums[i]
```

### Complexity Analysis

#### Time Complexity

```text
O(n^2)
```

Why?

- For each of the `n` candidate positions, counting its occurrences costs another `O(n)` scan.

#### Space Complexity

```text
O(1)
```

Why?

- Only the running `count` and `threshold` are used.

### Why this isn't good enough

The same value's count gets recomputed from scratch every time it's encountered as a candidate. A single frequency map, updated once per element as the array is scanned, tracks every value's running count in one pass, letting the majority be detected the moment any count crosses the threshold.

---

## 3. Key Insight

### What makes this problem difficult?

Sorting the array to find the middle element works, but costs `O(n log n)`. A brute-force count of every distinct value against every other position is `O(n^2)`. Since the array is guaranteed to have a true majority element (appearing more than half the time), there's a faster way to detect it in a single pass.

### Key Observation

Since the guaranteed majority element occurs more than `n / 2` times, tracking each value's running count as we scan the array will eventually cause exactly one value's count to exceed the threshold `n / 2` — and it must be the majority element, since no other value can also exceed half the array.

Example:

```text
nums = [2,2,1,1,1,2,2], threshold = 3

freq: {2:1} -> {2:2} -> {2:2,1:1} -> {2:2,1:2} -> {2:2,1:3} -> {2:3,1:3} -> {2:4,1:3}
                                                                                 ↑
                                                                    4 > 3 -> return 2
```

### Why does this observation help?

A hash map lets us count every value's occurrences in a single left-to-right pass, and we can return as soon as any count crosses the majority threshold — no sorting and no nested comparisons required.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a scoreboard where each distinct value gets its own running tally as we scan left to right. Since the problem guarantees a true majority exists, one tally is destined to climb past `n / 2` before the scan finishes — the moment that happens, that value is the answer.

```text
nums:   2   2   1   1   1   2   2
tally:  2:1 2:2 1:1 1:2 1:3 2:3 2:4
                                  ↑
                          4 > threshold(3) -> return 2
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize threshold = len(nums) // 2, freq = {}
   │
   ▼
For each n in nums:
   │
   ▼
count = freq.get(n, 0) + 1
freq[n] = count
   │
   ▼
Is count > threshold ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return n           Next n (or Done)
```

Explanation of each decision:

- `threshold` is fixed once as `len(nums) // 2` — any value's count strictly greater than this must be the majority.
- Every value's count is updated on every occurrence, so the check always reflects the running total up to the current position.
- Because the problem guarantees a majority element exists, this check is guaranteed to succeed before the scan runs out of elements.

---

## 6. Plain English Algorithm

1. Compute `threshold = len(nums) // 2`.
2. Create an empty frequency map `freq`.
3. Scan `nums` left to right. For each value `n`:
   - Increment `freq[n]` (starting from `0` if unseen).
   - If `freq[n]` now exceeds `threshold`, return `n` immediately.

---

## 7. Pseudocode

```text
threshold = length(nums) // 2
freq = empty map

for n in nums
    count = freq.get(n, 0) + 1
    freq[n] = count

    if count > threshold
        return n
```

---

## 8. Python Solution

```python
class Solution:
    def majorityElementHashMap(self, nums: List[int]) -> int:
        threshold = len(nums) // 2
        freq = {}

        for n in nums:
            count = freq.get(n, 0) + 1
            freq[n] = count

            if count > threshold:
                return n
```

---

## 9. Dry Run

Example:

```text
nums = [2,2,1,1,1,2,2]

threshold = 7 // 2 = 3
```

| Step | n | freq[n] after increment | count > threshold(3)? | Action |
|------|---|--------------------------|-------------------------|--------|
| 1 | 2 | 1 | No | Continue |
| 2 | 2 | 2 | No | Continue |
| 3 | 1 | 1 | No | Continue |
| 4 | 1 | 2 | No | Continue |
| 5 | 1 | 3 | No | Continue |
| 6 | 2 | 3 | No | Continue |
| 7 | 2 | 4 | Yes (4 > 3) | Return 2 |

Result: `2`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- A single pass over `nums`, with average `O(1)` hash map lookup and update per element.

### Space Complexity

```text
O(n)
```

Why?

- Worst case, `freq` grows to hold every distinct value in `nums` before the majority count is detected.
