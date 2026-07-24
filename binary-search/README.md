# Binary Search

## What is this pattern?

A technique for finding a target (or a boundary, or the smallest/largest
feasible value) in a **monotonic search space** by repeatedly halving the
range. Instead of scanning every candidate (`O(n)`), each comparison
eliminates half of what's left, giving `O(log n)`. The search space doesn't
have to be a sorted array — it can be an index range, a rotated array, or an
abstract range of *possible answers* (a capacity, a speed, a distance) as
long as there's a monotonic "feasible / not feasible" boundary to search
for.

Use this pattern when the problem is about:
- Searching a **sorted** (or rotated-sorted, or otherwise monotonic)
  array for a value or a boundary
- Finding the **first/last** position satisfying a condition (lower bound /
  upper bound)
- **"Minimize the maximum"** or **"maximize the minimum"** of some
  feasibility condition — binary search on the answer instead of the array
- Keywords like "sorted array", "rotated", "peak", "kth smallest",
  "minimum/maximum such that", "at least/at most days/capacity/speed"

## The general shape

**Standard binary search** — find an exact target:
*(used by: [binary-search](./easy/binary-search))*

```python
def solve(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**Lower bound / upper bound** — find the first index where a condition
becomes true (works because the condition is monotonic: `False...False
True...True`):
*(used by: [search-insert-position](./easy/search-insert-position))*

```python
def lower_bound(nums, target):
    lo, hi = 0, len(nums)  # hi is exclusive — one past the last index
    while lo < hi:
        mid = (lo + hi) // 2
        if condition(nums[mid], target):  # e.g. nums[mid] >= target
            hi = mid
        else:
            lo = mid + 1
    return lo  # first index where condition is True
```

**Binary search on answer** — search the space of *possible answers*, not
the array itself; requires a `feasible(x)` check that is monotonic (once
true, stays true as `x` grows, or vice versa):
*(used by: [koko-eating-bananas](./medium/koko-eating-bananas))*

```python
def solve(nums, condition):
    lo, hi = min_possible_answer, max_possible_answer
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid       # mid works — try to do better
        else:
            lo = mid + 1   # mid doesn't work — need more
    return lo
```

## Common sub-patterns

**Exact match** (classic binary search)
*(problems: [binary-search](./easy/binary-search))*
```python
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
```

**Boundary search** (first/last occurrence, insert position)
*(no solutions yet)*
```python
lo, hi = 0, len(nums)
while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] >= target:
        hi = mid
    else:
        lo = mid + 1
```

**Rotated sorted array** (one half is always sorted — decide which half,
then decide whether the target lies inside it)
*(no solutions yet)*
```python
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target:
        return mid
    if nums[lo] <= nums[mid]:          # left half is sorted
        if nums[lo] <= target < nums[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    else:                               # right half is sorted
        if nums[mid] < target <= nums[hi]:
            lo = mid + 1
        else:
            hi = mid - 1
```

**Binary search on answer** (minimize the max / maximize the min under a
feasibility check)
*(no solutions yet)*
```python
lo, hi = min_possible, max_possible
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
        hi = mid
    else:
        lo = mid + 1
```

## Complexity

- **Time:** `O(log n)` for a fixed-size search space; `O(n log n)` or
  `O(log(range))` when combined with an `O(n)` feasibility check per step
  (typical for binary search on answer).
- **Space:** `O(1)` iterative; `O(log n)` if implemented recursively (call
  stack).

## Common pitfalls

- **Infinite loops from the wrong midpoint/update pair** — `lo <= hi` with
  `lo = mid + 1` / `hi = mid - 1` (closed interval) must not be mixed with
  `lo < hi` with `hi = mid` (half-open interval); mixing them causes `mid`
  to never move or to skip past the answer.
- **Off-by-one on the boundary** — deciding between `hi = mid` and
  `hi = mid - 1` (or `lo = mid` and `lo = mid + 1`) depends on whether
  `mid` itself can still be the answer; picking the wrong one drops the
  correct index or loops forever.
- **Non-monotonic feasibility check** — binary search on answer only works
  if `feasible(x)` is `False...False True...True` (or the reverse) across
  the search range; applying it to a non-monotonic condition silently
  gives a wrong answer instead of an error.
- **Forgetting duplicates break the rotated-array trick** — `nums[lo] <=
  nums[mid]` can't tell which half is sorted when `nums[lo] == nums[mid] ==
  nums[hi]`; those cases need a linear fallback (shrink `lo`/`hi` by one).
- **Wrong initial bounds for "search on answer"** — `lo`/`hi` must be the
  true min/max of the *answer*, not of the input array (e.g. Koko's `hi`
  is `max(piles)`, not `len(piles)`).

## Problems in this folder

No problems solved yet in this folder — see [PROGRESS.md](./PROGRESS.md)
for the full problem queue and recommended order.
