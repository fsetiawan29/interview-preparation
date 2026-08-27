# Problem: Find Minimum in Rotated Sorted Array

## 1. Problem Understanding

### Problem Summary

`nums` was originally sorted in ascending order with all unique values,
then rotated between `1` and `n` times at an unknown pivot (e.g.
`[0,1,2,4,5,6,7]` becomes `[4,5,6,7,0,1,2]` after 4 rotations). Given the
rotated array, return its minimum element. The solution must run in
`O(log n)` time.

### Input

- A rotated, ascending array of unique integers, `nums`

### Output

- An integer: the minimum value in `nums`.

### Constraints

- `1 <= nums.length <= 5000`
- `-5000 <= nums[i] <= 5000`
- All the integers of `nums` are unique.
- `nums` is sorted and rotated between `1` and `n` times.

### Example

Input:

```text
nums = [4,5,6,7,0,1,2]
```

Output:

```text
0
```

Manual walkthrough:

```text
left=0, right=6 -> mid=3, nums[mid]=7 > nums[right]=2 -> the minimum is
past mid -> left=4
left=4, right=6 -> mid=5, nums[mid]=1 <= nums[right]=2 -> the minimum is
at mid or before it -> right=5
left=4, right=5 -> mid=4, nums[mid]=0 <= nums[right]=1 -> right=4
left=4, right=4 -> loop ends, return nums[4] = 0
```

---

## 2. Brute Force Approach

### Idea

Scan the array left to right, keeping track of the smallest value seen so
far. Rotation doesn't matter at all if every element is simply compared.

### Pseudocode

```text
function solve(nums)
    minVal = nums[0]
    for num in nums
        if num < minVal
            minVal = num
    return minVal
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- Every element is visited exactly once to compare it against the running
  minimum.

#### Space Complexity

```text
O(1)
```

Why?

- Only a single variable is kept beyond the loop index.

### Why this isn't good enough

The array is still "sorted" in pieces — rotation only breaks it into two
ascending runs glued together at one seam, and the minimum always sits
right at that seam. A linear scan finds it correctly but ignores the
ordering that would let the seam be located directly, without comparing
every element along the way.

---

## 3. Key Insight

### What makes this problem difficult?

There's no `target` to compare against, so the usual "which half contains
the target" binary search rule doesn't directly apply. What's needed
instead is a rule that decides which half contains the *seam* (the point
where the array drops from a large value back down to a small one).

### Key Observation

Comparing `nums[mid]` to `nums[right]` always reveals which side the seam
is on:

- `nums[mid] > nums[right]` -> the seam (and the minimum) is somewhere in
  `(mid, right]`, so it's safe to discard everything up to and including
  `mid` -> `left = mid + 1`.
- `nums[mid] <= nums[right]` -> the range `[mid..right]` is already a
  clean ascending run with no seam in it, so the minimum is at `mid` or to
  its left -> `right = mid` (keep `mid`, since it could be the answer).

Example:

```text
nums = [4, 5, 6, 7, 0, 1, 2]

left=0, mid=3 -> nums[mid]=7 > nums[right]=2, so the seam is to the right
of mid -> the minimum can't be in [left..mid] -> go right.
```

### Why does this observation help?

Every comparison eliminates half the search space, same as ordinary binary
search — it's just narrowing in on the seam instead of a target value.
Because `right` is set to `mid` (not `mid - 1`) on a match, `mid` is never
wrongly discarded when it could be the minimum itself, and the loop
naturally converges to the single index holding the smallest value.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture two sorted ramps glued end to end at a seam, like a sorted list
that got cut and swapped: `[4,5,6,7 | 0,1,2]`. The minimum always sits at
the start of the second ramp. Comparing `nums[mid]` to `nums[right]` says
whether the seam is still ahead of `mid` (values climbed too high, so it's
somewhere past `mid`) or already behind it (the range from `mid` onward is
already smooth, so the seam is at or before `mid`).

```text
[4, 5, 6, 7, 0, 1, 2]
 left--------mid------right   mid=3, nums[mid]=7 > nums[right]=2 -> seam is right of mid -> go right
             [0, 1, 2]
             left-mid-right   mid=5, nums[mid]=1 <= nums[right]=2 -> seam is at/before mid -> keep mid
             [0, 1]
             left-mid=right   mid=4, nums[mid]=0 <= nums[right]=1 -> keep mid
             found: nums[4] = 0
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
left = 0, right = len(nums) - 1
   │
   ▼
left < right ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return nums[left]  mid = left + (right-left)//2
                        │
                        ▼
                nums[mid] > nums[right] ?
                        │
              ┌─────────┴─────────┐
              │                   │
             Yes                 No
      (seam is right of mid) (mid..right is clean,
              │                seam is at/before mid)
              ▼                   │
        left = mid + 1            ▼
        (discard left half,   right = mid
         it can't hold the    (keep mid, it might
         minimum)              be the minimum)
              │                   │
              └─────────┬─────────┘
                        ▼
              (loop back to left < right ?)
```

Explanation of each decision:

- `left == right` is the base case — the search space has narrowed to one
  index, which must hold the minimum.
- `nums[mid] > nums[right]` means `mid` is still on the "high" ramp before
  the seam, so the minimum is strictly to the right of `mid` -> narrow to
  `[mid+1..right]`.
- `nums[mid] <= nums[right]` means `[mid..right]` is already a clean
  ascending run, so the minimum is `mid` or something to its left ->
  narrow to `[left..mid]`, keeping `mid` in play.

---

## 6. Plain English Algorithm

1. Set `left = 0` and `right = len(nums) - 1`.
2. While `left < right`:
   - Compute `mid = left + (right - left) / 2`.
   - If `nums[mid] > nums[right]`, the seam lies to the right of `mid`, so
     the minimum can't be in `[left..mid]` — move `left` to `mid + 1`.
   - Otherwise, `[mid..right]` is already a clean ascending run, so the
     minimum is `mid` or to its left — move `right` to `mid` (not
     `mid - 1`, since `mid` itself could be the answer).
3. When the loop ends, `left == right` and that single index holds the
   minimum — return `nums[left]`.

---

## 7. Pseudocode

```text
function solve(nums)
    left, right = 0, len(nums) - 1
    while left < right
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]
            left = mid + 1
        else
            right = mid
    return nums[left]
```

---

## 8. Go Solution

```go
package solution

func findMin(nums []int) int {
	left := 0
	right := len(nums) - 1

	for left < right {
		mid := left + (right-left)/2

		if nums[mid] > nums[right] {
			left = mid + 1
		} else {
			right = mid
		}
	}

	return nums[left]
}
```

---

## 9. Dry Run

Example:

```text
nums = [4, 5, 6, 7, 0, 1, 2]
```

| Step | `left` | `right` | `mid` | `nums[mid]` | `nums[right]` | Action | Why? |
|------|--------|---------|-------|-------------|----------------|--------|------|
| 1 | 0 | 6 | 3 | 7 | 2 | `7 > 2` -> `left = 4` | Seam is right of mid |
| 2 | 4 | 6 | 5 | 1 | 2 | `1 <= 2` -> `right = 5` | `[5..6]` is clean, keep mid |
| 3 | 4 | 5 | 4 | 0 | 1 | `0 <= 1` -> `right = 4` | `[4..5]` is clean, keep mid |
| 4 | 4 | 4 | — | — | — | `left == right` -> return `nums[4]` | Search space narrowed to one index |

Result: `0`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log n)
```

Why?

- Each iteration compares `nums[mid]` against `nums[right]` and discards
  half the remaining range, so the loop runs `O(log n)` times.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of index variables (`left`, `right`, `mid`) are
  used, regardless of input size.
