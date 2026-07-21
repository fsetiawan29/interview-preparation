# Two Pointers

## What is this pattern?

A broad bucket of problems solved by walking an array/string with two indices
instead of nesting loops or allocating extra structures. The two pointers
either start at **opposite ends and move inward**, or move in the
**same direction** at different speeds (a slow "write" pointer trailing a
fast "read" pointer). Either shape turns an `O(n^2)` brute force into a
single `O(n)` pass.

Use this pattern when the problem is about:
- Comparing/matching elements from **both ends** of a sorted array or string
  (palindromes, sorted two-sum, reversing in place)
- **Filtering or compacting in place** — keep/drop elements without extra
  space (remove duplicates, move zeroes, remove element)
- **Merging or matching two sequences** in lockstep (merge alternately,
  subsequence check)

## The general shape

**Opposite-ends pointers** — converge toward the middle:

```python
def solve(s):
    l, r = 0, len(s) - 1

    while l < r:
        # 1. CHECK — compare/act on s[l] and s[r]
        if condition_on(s[l], s[r]):
            return answer

        # 2. MOVE — advance one or both pointers inward
        l += 1
        r -= 1

    return default_answer
```

**Read/write pointers** — same direction, different speeds:

```python
def solve(nums):
    j = 0  # write pointer — next slot to fill

    for i in range(len(nums)):  # read pointer — scans everything
        if keep(nums[i]):
            nums[j] = nums[i]
            j += 1

    return j  # count of kept elements
```

## Common sub-patterns

**Opposite ends — converge and compare** (palindrome, reverse in place)
```python
l, r = 0, len(s) - 1
while l < r:
    s[l], s[r] = s[r], s[l]
    l += 1
    r -= 1
```

**Opposite ends — sorted two-sum** (narrow based on comparison to target)
```python
left, right = 0, len(nums) - 1
while left < right:
    total = nums[left] + nums[right]
    if total == target:
        return [left, right]
    elif total > target:
        right -= 1
    else:
        left += 1
```

**Read/write — filter in place** (remove element, remove duplicates)
```python
j = 0
for i in range(len(nums)):
    if nums[i] != val:
        nums[j] = nums[i]
        j += 1
```

**Same-direction — merge two sequences in lockstep**
```python
i = j = 0
res = []
while i < len(a) or j < len(b):
    if i < len(a):
        res.append(a[i]); i += 1
    if j < len(b):
        res.append(b[j]); j += 1
```

## Complexity

- **Time:** `O(n)` — each pointer crosses the array/string at most once, so
  the two pointers together do at most `2n` work, not `n^2`.
- **Space:** `O(1)` when mutating in place (swaps, read/write compaction);
  `O(n)` when the input must be copied first (immutable strings) or the
  output is a new array/string.

## Common pitfalls

- **Squaring/transforming before comparing when comparing magnitudes is
  enough** — e.g. `squares-of-sorted-array` only needs `abs()` to pick the
  bigger end, not the actual square.
- **Off-by-one on the loop condition** — `left < right` vs `left <= right`
  depends on whether the pointers are allowed to land on the same index
  (e.g. `remove-element`'s opposite-ends approach needs `<=` because a
  freshly-swapped `left` value still needs checking).
- **Forgetting a bound check on one pointer** while advancing the other in a
  merge-style loop (e.g. `is-subsequence`'s `j` must stop at `len(s)`).
- **Using a hash set for membership when the input is already sorted** —
  two pointers gives the same `O(n)` result with `O(1)` space instead of
  `O(n)`.

## Problems in this folder

### Easy

- [reverse-string](./easy/reverse-string) — opposite-ends pointers, swap and
  converge; the canonical in-place reversal.
- [valid-palindrome](./easy/valid-palindrome) — opposite-ends pointers that
  skip non-alphanumeric characters before comparing.
- [reverse-vowels-of-a-string](./easy/reverse-vowels-of-a-string) —
  opposite-ends pointers that skip non-vowel characters before swapping.
- [squares-of-sorted-array](./easy/squares-of-sorted-array) — opposite-ends
  read pointers plus a write pointer filled from the back, since the
  largest square is always at one of the two ends.
- [move-zeroes](./easy/move-zeroes) — read/write pointers, swap non-zero
  values into place instead of just overwriting.
- [remove-element](./easy/remove-element) — read/write pointers (or
  opposite-ends swap) to compact the array around values to keep.
- [remove-duplicates-from-sorted-array](./easy/remove-duplicates-from-sorted-array) —
  read/write pointers over an already-sorted array; no set needed since
  duplicates are always adjacent.
- [merge-strings-alternately](./easy/merge-strings-alternately) —
  same-direction pointers advancing through two strings in lockstep.
- [is-subsequence](./easy/is-subsequence) — same-direction pointers where
  one advances every step and the other only on a match.

### Medium

- [two-sum-ii](./medium/two-sum-ii) — opposite-ends pointers narrowing based
  on comparison to target; the sorted-array counterpart to the hash-map
  two-sum.
- [sort-characters-by-frequency](./medium/sort-characters-by-frequency) —
  not two pointers, but the same "frequency count feeding a bucket" shape
  as arrays-hashing's top-k-frequent-elements.
