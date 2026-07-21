# Sliding Window

## What is this pattern?

A technique for problems about a **contiguous** subarray or substring that
must satisfy some condition (max/min length, sum, frequency, distinct
count, etc.). Instead of recomputing the answer for every possible
subarray (`O(n^2)` or worse), maintain a **window** `[left, right]` and
slide it across the array/string, updating the answer incrementally in
`O(1)` amortized per step. This turns most "find the best contiguous
subarray/substring" problems into a single `O(n)` pass.

Use this pattern when the problem is about:
- A **contiguous** subarray or substring (not a subsequence — order and
  adjacency matter)
- Optimizing (longest/shortest, max/min sum) or counting windows that
  satisfy a condition
- A condition that can be **incrementally maintained** as the window grows
  or shrinks (running sum, frequency map, distinct count) instead of
  recomputed from scratch
- Keywords like "contiguous", "substring", "subarray", "at most K",
  "longest/shortest window"

## The general shape

**Fixed-size window** — slide by one, don't recompute:

```python
def solve(nums, k):
    window_sum = sum(nums[:k])
    best = window_sum

    for right in range(k, len(nums)):
        window_sum += nums[right] - nums[right - k]
        best = max(best, window_sum)

    return best
```

**Variable-size window** — expand right, shrink left while invalid:

```python
def solve(s):
    left = 0
    window = {}
    best = 0

    for right in range(len(s)):
        # 1. EXPAND — add s[right] into the window
        window[s[right]] = window.get(s[right], 0) + 1

        # 2. SHRINK — while the window violates the condition, drop from the left
        while invalid(window):
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
            left += 1

        # 3. RECORD — window [left, right] is now valid
        best = max(best, right - left + 1)

    return best
```

## Common sub-patterns

**Fixed window** (size k, slide by one)
```python
window_sum = sum(nums[:k])
for right in range(k, len(nums)):
    window_sum += nums[right] - nums[right - k]
```

**Variable window — expand until valid, then shrink** (minimum window)
```python
left = 0
for right in range(len(nums)):
    total += nums[right]
    while total >= target:
        best = min(best, right - left + 1)
        total -= nums[left]
        left += 1
```

**Variable window — expand, shrink only when invalid** (maximum window / at most K)
```python
left = 0
count = {}
for right in range(len(s)):
    count[s[right]] = count.get(s[right], 0) + 1
    while len(count) > k:
        count[s[left]] -= 1
        if count[s[left]] == 0:
            del count[s[left]]
        left += 1
    best = max(best, right - left + 1)
```

**Monotonic deque — window maximum/minimum**
```python
from collections import deque

dq = deque()  # stores indices, values decreasing left to right
for i, n in enumerate(nums):
    while dq and nums[dq[-1]] < n:
        dq.pop()
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()
    if i >= k - 1:
        result.append(nums[dq[0]])
```

## Complexity

- **Time:** `O(n)` — each element enters and leaves the window at most
  once, so the two pointers together do at most `2n` work, not `n^2`.
  Monotonic-deque problems are still `O(n)` amortized since each index is
  pushed and popped at most once.
- **Space:** `O(1)` for a running sum/count; `O(k)` or bounded-alphabet
  (`O(26)`/`O(128)`) for a frequency map; `O(n)` worst case for a deque or
  a hash map keyed by arbitrary values.

## Common pitfalls

- **Recomputing the window from scratch on every slide** instead of
  incrementally updating (add the new element, remove the old one) —
  turns `O(n)` into `O(n*k)`.
- **Off-by-one on window size** — `right - left + 1` vs `right - left`,
  and inclusive/exclusive bounds when subtracting `nums[right - k]`.
- **Shrinking too much or too little** — "at most K" and "at least K"
  need different shrink conditions (`while invalid` vs `while valid`).
- **Forgetting to clean up a frequency map entry when its count hits
  zero** — a stale key with count `0` makes `len(count)` report the wrong
  distinct-element count.
- **Reimplementing "exactly K" directly** instead of using
  `atMost(K) - atMost(K - 1)`, the standard trick for exact-count window
  problems.
- **Confusing subarray/substring (contiguous) with subsequence (not
  contiguous)** — sliding window only applies to the former.

## Problems in this folder

No solutions yet — see [PROGRESS.md](./PROGRESS.md) for the learning
roadmap and recommended problem order.
