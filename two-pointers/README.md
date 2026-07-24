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
*(used by: [reverse-string](./easy/reverse-string), [valid-palindrome](./easy/valid-palindrome), [reverse-vowels-of-a-string](./easy/reverse-vowels-of-a-string), [two-sum-ii](./medium/two-sum-ii), [container-with-most-water](./medium/container-with-most-water), [3-sum](./medium/3-sum), [4sum](./medium/4sum), [trapping-rain-water](./hard/trapping-rain-water))*

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
*(used by: [move-zeroes](./easy/move-zeroes), [remove-element](./easy/remove-element), [remove-duplicates-from-sorted-array](./easy/remove-duplicates-from-sorted-array), [squares-of-sorted-array](./easy/squares-of-sorted-array), [sort-colors](./medium/sort-colors))*

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

**Opposite ends — converge and compare**
*(problems: [reverse-string](./easy/reverse-string), [valid-palindrome](./easy/valid-palindrome), [reverse-vowels-of-a-string](./easy/reverse-vowels-of-a-string))*
```python
l, r = 0, len(s) - 1
while l < r:
    s[l], s[r] = s[r], s[l]
    l += 1
    r -= 1
```

**Opposite ends — sorted two-sum** (narrow based on comparison to target)
*(problems: [two-sum-ii](./medium/two-sum-ii), [two-sum-less-than-k](./easy/two-sum-less-than-k), [count-pairs-whose-sum-less-than-target](./easy/count-pairs-whose-sum-less-than-target))*
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

**Read/write — filter in place**
*(problems: [remove-element](./easy/remove-element), [remove-duplicates-from-sorted-array](./easy/remove-duplicates-from-sorted-array), [move-zeroes](./easy/move-zeroes))*
```python
j = 0
for i in range(len(nums)):
    if nums[i] != val:
        nums[j] = nums[i]
        j += 1
```

**Same-direction — merge two sequences in lockstep**
*(problems: [merge-strings-alternately](./easy/merge-strings-alternately), [is-subsequence](./easy/is-subsequence))*
```python
i = j = 0
res = []
while i < len(a) or j < len(b):
    if i < len(a):
        res.append(a[i]); i += 1
    if j < len(b):
        res.append(b[j]); j += 1
```

**Opposite ends — greedy narrowing** (discard the shorter wall)
*(problems: [container-with-most-water](./medium/container-with-most-water))*
```python
left, right = 0, len(height) - 1
max_area = 0
while left < right:
    max_area = max(max_area, (right - left) * min(height[left], height[right]))
    if height[left] < height[right]:
        left += 1
    else:
        right -= 1
```

**Opposite ends — running max on each side** (trap water between walls)
*(problems: [trapping-rain-water](./hard/trapping-rain-water))*
```python
left, right = 0, len(height) - 1
left_max, right_max = height[left], height[right]
water = 0
while left < right:
    if left_max < right_max:
        left += 1
        left_max = max(left_max, height[left])
        water += left_max - height[left]
    else:
        right -= 1
        right_max = max(right_max, height[right])
        water += right_max - height[right]
```

**Sort + fix index(es) — k-sum family** (skip duplicates at every level)
*(problems: [3-sum](./medium/3-sum), [4sum](./medium/4sum))*
```python
nums.sort()
for i in range(len(nums) - 2):
    if i > 0 and nums[i] == nums[i - 1]:
        continue
    left, right = i + 1, len(nums) - 1
    while left < right:
        total = nums[i] + nums[left] + nums[right]
        if total == 0:
            left += 1; right -= 1
            while left < right and nums[left] == nums[left - 1]:
                left += 1
        elif total < 0:
            left += 1
        else:
            right -= 1
```

**Three pointers — partition into three buckets** (Dutch National Flag)
*(problems: [sort-colors](./medium/sort-colors))*
```python
low, mid, high = 0, 0, len(nums) - 1
while mid <= high:
    if nums[mid] == 0:
        nums[low], nums[mid] = nums[mid], nums[low]
        low += 1; mid += 1
    elif nums[mid] == 1:
        mid += 1
    else:
        nums[mid], nums[high] = nums[high], nums[mid]
        high -= 1
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
- **Skipping duplicates against the wrong neighbor** — in `3-sum`/`4sum`,
  the second fixed index must skip duplicates relative to the *current*
  outer index (`j > i + 1`), not globally (`j > 0`); after moving
  `left`/`right` past a match, compare against the value just left behind
  (`nums[left - 1]`), not the value ahead.
- **Advancing `mid` after a swap with `high`** in a three-way partition
  (`sort-colors`) — the swapped-in value hasn't been checked yet, so only
  swaps with `low` are safe to advance past.
- **Not trusting the smaller running max** in `trapping-rain-water` — when
  `left_max < right_max`, the water above `left` is bounded by `left_max`
  no matter how tall unseen bars on the right turn out to be, so it's
  safe to finalize and advance `left` without ever looking past `right`.

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
- [two-sum-less-than-k](./easy/two-sum-less-than-k) — sort first, then
  opposite-ends pointers narrowing based on comparison to `k`; unlike
  two-sum-ii, keeps searching after a valid pair to maximize the sum instead
  of returning immediately.
- [count-pairs-whose-sum-less-than-target](./easy/count-pairs-whose-sum-less-than-target) —
  sort first, then opposite-ends pointers; a valid pair at `(left, right)`
  means every index between them also pairs validly with `left`, so add
  `right - left` to the count in one shot instead of counting pairs
  individually.
- [duplicate-zeros](./easy/duplicate-zeros) — read/write pointers filled
  from the back instead of the front, so writing a duplicated zero never
  overwrites a value that still needs to be read.

### Medium

- [two-sum-ii](./medium/two-sum-ii) — opposite-ends pointers narrowing based
  on comparison to target; the sorted-array counterpart to arrays-hashing's
  hash-map [two-sum](../arrays-hashing/easy/two-sum).
- [container-with-most-water](./medium/container-with-most-water) —
  opposite-ends pointers with a greedy narrow: always move the shorter
  wall, since moving the taller one can only shrink width without ever
  raising the limiting height.
- [3-sum](./medium/3-sum) — sort first, fix one index, then opposite-ends
  two-pointer on the rest; skip duplicates at the fixed index and at both
  pointers after every match.
- [4sum](./medium/4sum) — same shape as 3-sum with a second fixed index;
  duplicate-skipping and loop bounds get one level trickier (skip the
  second index only relative to the current outer index, not globally).
- [sort-colors](./medium/sort-colors) — three pointers (`low`, `mid`,
  `high`) partitioning into three buckets in one pass; swapping with `high`
  doesn't advance `mid`, since the swapped-in value is still unchecked.
- [sort-characters-by-frequency](./medium/sort-characters-by-frequency) —
  not two pointers, but the same "frequency count feeding a bucket" shape
  as arrays-hashing's
  [top-k-frequent-elements](../arrays-hashing/medium/top-k-frequent-elements).

### Hard

- [trapping-rain-water](./hard/trapping-rain-water) — three approaches
  side by side: brute force (rescan both directions per index,
  `O(n^2)`), prefix/suffix max arrays (`O(n)` time and space), and
  opposite-ends two pointers tracking a running max on each side
  (`O(n)` time, `O(1)` space) — the two-pointer version collapses the
  two arrays into two running values by only ever trusting whichever
  side currently has the smaller max.
