# Problem: Find First and Last Position of Element in Sorted Array

## 1. Problem Understanding

### Problem Summary

Given an array `nums` sorted in non-decreasing order and a `target` value,
find the starting and ending index of `target` in the array. If `target`
isn't found, return `[-1, -1]`. The solution must run in `O(log n)` time.

### Input

- An array sorted in non-decreasing order, `nums` (values may repeat)
- An integer, `target`

### Output

- A two-element slice `[first, last]`: the first and last index of
  `target` in `nums`, or `[-1, -1]` if `target` isn't present.

### Constraints

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `nums` is a non-decreasing array.
- `-10^9 <= target <= 10^9`

### Example

Input:

```text
nums = [5,7,7,8,8,10], target = 8
```

Output:

```text
[3,4]
```

Manual walkthrough:

```text
8 appears at indices 3 and 4 in [5,7,7,8,8,10].
First occurrence: index 3. Last occurrence: index 4.
```

---

## 2. Brute Force Approach

### Idea

Scan the array left to right, recording the index of the first match and
the index of the last match seen.

### Pseudocode

```text
function solve(nums, target)
    first, last = -1, -1
    for i, num in nums
        if num == target
            if first == -1
                first = i
            last = i
    return [first, last]
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- Every element can be visited once; in the worst case (target missing, or
  every element equals `target`) all `n` elements are checked.

#### Space Complexity

```text
O(1)
```

Why?

- Only two index variables are kept beyond the loop counter.

### Why this isn't good enough

`nums` is sorted, so every occurrence of `target` sits in one contiguous
block. A linear scan finds that block correctly but ignores the ordering
that would let both edges of the block be located directly, without
walking through every value inside it.

---

## 3. Key Insight

### What makes this problem difficult?

Plain binary search stops as soon as it finds *any* index equal to
`target`, but with duplicates that index could be anywhere inside the
matching block — not necessarily the first or last one. Finding a
boundary requires the search to keep going *past* a match instead of
stopping there.

### Key Observation

The first and last positions of `target` are two independent boundary
searches:

- **First occurrence**: on a match, the answer might still be further
  left — record it and keep searching the left half (`right = mid - 1`).
- **Last occurrence**: on a match, the answer might still be further
  right — record it and keep searching the right half (`left = mid + 1`).

Both are still plain binary search; only what happens on `nums[mid] ==
target` changes.

Example:

```text
nums = [5, 7, 7, 8, 8, 10], target = 8

Finding the first 8: on hitting index 4 (a match), don't stop — keep
searching [left..3] in case an earlier 8 exists. It does, at index 3.

Finding the last 8: on hitting index 4 (a match), don't stop — keep
searching [5..right] in case a later 8 exists. It doesn't, so 4 stands.
```

### Why does this observation help?

Each boundary search is still `O(log n)`, and running the two searches
back to back is still `O(log n)` overall — far better than scanning the
whole matching block, which could be up to `n` elements long.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture the sorted array as a hallway with a block of identical doors
(the matching values) somewhere in it. Two separate searches walk toward
that block from binary search's usual "narrow by half" strategy: one
search treats "found a door" as "keep pushing left to find the block's
first door", the other treats it as "keep pushing right to find the
block's last door".

```text
[5, 7, 7, 8, 8, 10]  target = 8
          ^  ^
          first=3, last=4

findLeft:  on match at mid, remember it, then search left of mid
findRight: on match at mid, remember it, then search right of mid
```

---

## 5. Decision Tree

Both `findLeft` and `findRight` share the same shape; only the branch
taken on a match differs.

```text
(Start: findLeft / findRight)
   │
   ▼
left = 0, right = len(nums) - 1, res = -1
   │
   ▼
left <= right ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return res         mid = left + (right-left)//2
                        │
                        ▼
                  nums[mid] vs target ?
                        │
              ┌─────────┼─────────────┐
              │         │             │
          nums[mid]   nums[mid]    nums[mid]
           < target    > target    == target
              │         │             │
              ▼         ▼             ▼
        left = mid+1  right = mid-1  res = mid
                                       │
                              ┌────────┴────────┐
                              │                  │
                        findLeft:           findRight:
                        right = mid-1       left = mid+1
                        (keep looking        (keep looking
                         further left)        further right)
                              │                  │
                              └────────┬─────────┘
                                       ▼
                             (loop back to left <= right ?)
```

Explanation of each decision:

- `left > right` is the base case — the search space is empty; `res`
  holds the last match found (or `-1` if none was ever seen).
- `nums[mid] < target` means the target range is strictly to the right —
  narrow to `[mid+1, right]`.
- `nums[mid] > target` means the target range is strictly to the left —
  narrow to `[left, mid-1]`.
- `nums[mid] == target` records `mid` as a candidate, then keeps
  searching the direction that could still improve the boundary:
  further left for the first occurrence, further right for the last.

---

## 6. Plain English Algorithm

1. Run two independent binary searches over `nums`, both bounded by
   `left = 0` and `right = len(nums) - 1`.
2. **`findLeft`** — while `left <= right`:
   - Compute `mid = left + (right - left) / 2`.
   - If `nums[mid] < target`, move `left` to `mid + 1`.
   - If `nums[mid] > target`, move `right` to `mid - 1`.
   - If `nums[mid] == target`, record `res = mid`, then move `right` to
     `mid - 1` to keep checking for an earlier match.
   - Return `res` once the loop ends.
3. **`findRight`** — identical, except on a match move `left` to
   `mid + 1` instead, to keep checking for a later match.
4. Return `[findLeft(nums, target), findRight(nums, target)]`. If
   `target` never matched, both helpers return `-1`, giving `[-1, -1]`.

---

## 7. Pseudocode

```text
function solve(nums, target)
    return [findLeft(nums, target), findRight(nums, target)]

function findLeft(nums, target)
    left, right, res = 0, len(nums) - 1, -1
    while left <= right
        mid = left + (right - left) // 2
        if nums[mid] < target
            left = mid + 1
        elif nums[mid] > target
            right = mid - 1
        else
            res = mid
            right = mid - 1   # keep looking left for an earlier match
    return res

function findRight(nums, target)
    left, right, res = 0, len(nums) - 1, -1
    while left <= right
        mid = left + (right - left) // 2
        if nums[mid] < target
            left = mid + 1
        elif nums[mid] > target
            right = mid - 1
        else
            res = mid
            left = mid + 1    # keep looking right for a later match
    return res
```

---

## 8. Go Solution

```go
package solution

func searchRange(nums []int, target int) []int {
	left := findLeft(nums, target)
	right := findRight(nums, target)

	return []int{left, right}
}

func findLeft(nums []int, target int) int {
	left := 0
	right := len(nums) - 1
	res := -1

	for left <= right {
		mid := left + (right-left)/2

		if nums[mid] < target {
			left = mid + 1
		} else if nums[mid] > target {
			right = mid - 1
		} else {
			res = mid
			right = mid - 1
		}
	}

	return res
}

func findRight(nums []int, target int) int {
	left := 0
	right := len(nums) - 1
	res := -1

	for left <= right {
		mid := left + (right-left)/2

		if nums[mid] < target {
			left = mid + 1
		} else if nums[mid] > target {
			right = mid - 1
		} else {
			res = mid
			left = mid + 1
		}
	}

	return res
}
```

---

## 9. Dry Run

Example:

```text
nums = [5, 7, 7, 8, 8, 10], target = 8
```

`findLeft`:

| Step | `left` | `right` | `mid` | `nums[mid]` | Action | Why? |
|------|--------|---------|-------|-------------|--------|------|
| 1 | 0 | 5 | 2 | 7 | `7 < 8` -> `left = 3` | Target range is to the right |
| 2 | 3 | 5 | 4 | 8 | Match -> `res = 4`, `right = 3` | Keep checking for an earlier `8` |
| 3 | 3 | 3 | 3 | 8 | Match -> `res = 3`, `right = 2` | Keep checking for an earlier `8` |
| 4 | 3 | 2 | — | — | `left > right` -> return `3` | Search space exhausted |

`findRight`:

| Step | `left` | `right` | `mid` | `nums[mid]` | Action | Why? |
|------|--------|---------|-------|-------------|--------|------|
| 1 | 0 | 5 | 2 | 7 | `7 < 8` -> `left = 3` | Target range is to the right |
| 2 | 3 | 5 | 4 | 8 | Match -> `res = 4`, `left = 5` | Keep checking for a later `8` |
| 3 | 5 | 5 | 5 | 10 | `10 > 8` -> `right = 4` | Target range is to the left |
| 4 | 5 | 4 | — | — | `left > right` -> return `4` | Search space exhausted |

Result: `[3, 4]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log n)
```

Why?

- `findLeft` and `findRight` are each ordinary binary searches that halve
  the remaining range every iteration, so each runs in `O(log n)`.
  Running them one after another is still `O(log n) + O(log n) = O(log
  n)`.

### Space Complexity

```text
O(1)
```

Why?

- Each search only tracks a fixed number of index variables (`left`,
  `right`, `mid`, `res`), regardless of input size.
