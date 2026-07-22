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
*(used by: [maximum-average-subarray-1](./easy/maximum-average-subarray-1), [contains-duplicate-2](./easy/contains-duplicate-2), [max-number-of-vowels](./medium/max-number-of-vowels), [number-of-sub-array-size-k](./medium/number-of-sub-array-size-k), [max-sum-of-distinct](./medium/max-sum-of-distinct))*

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
*(no solutions yet)*

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
*(problems: [maximum-average-subarray-1](./easy/maximum-average-subarray-1), [contains-duplicate-2](./easy/contains-duplicate-2), [max-number-of-vowels](./medium/max-number-of-vowels), [number-of-sub-array-size-k](./medium/number-of-sub-array-size-k), [max-sum-of-distinct](./medium/max-sum-of-distinct))*
```python
window_sum = sum(nums[:k])
for right in range(k, len(nums)):
    window_sum += nums[right] - nums[right - k]
```

**Variable window — expand until valid, then shrink** (minimum window)
*(no solutions yet)*
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
*(no solutions yet)*
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
*(no solutions yet)*
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

### Easy

- [maximum-average-subarray-1](./easy/maximum-average-subarray-1) —
  fixed-size window sliding by one: subtract the outgoing element, add the
  incoming one, divide by `k` once at the end instead of every iteration.
- [contains-duplicate-2](./easy/contains-duplicate-2) — fixed-size window
  (hash set or hash map) checking for a duplicate within distance `k`;
  clamp the initial window when `k > len(nums)`, and delete map keys once
  their count hits `0` so stale zero-count entries don't linger. The
  sliding-window sequel to arrays-hashing's
  [contains-duplicate](../arrays-hashing/easy/contains-duplicate), which
  checks for a duplicate anywhere in the array with no distance limit.

### Medium

- [max-number-of-vowels](./medium/max-number-of-vowels) — same fixed-size
  slide as maximum-average-subarray-1, but tracking a count (vowels
  in/out of the window) instead of a sum.
- [number-of-sub-array-size-k](./medium/number-of-sub-array-size-k) —
  fixed-size window counting how many windows meet a threshold; compare
  `window_sum >= k * threshold` instead of dividing every window to avoid
  floating-point division per step.
- [max-sum-of-distinct](./medium/max-sum-of-distinct) — fixed-size window
  tracking both a running sum and a frequency map; the window is
  all-distinct exactly when `len(freq) == k`, so no separate set check is
  needed.
