# Problem: Search in Rotated Sorted Array

## 1. Problem Understanding

### Problem Summary

`nums` was originally sorted in ascending order, then rotated at some
unknown pivot (e.g. `[0,1,2,4,5,6,7]` becomes `[4,5,6,7,0,1,2]`). Given the
rotated array and a `target`, return the index of `target` in `nums`, or
`-1` if it isn't present. The solution must run in `O(log n)` time.

### Input

- A possibly-rotated array of distinct integers, `nums`
- An integer, `target`

### Output

- The index of `target` in `nums`, or `-1` if `target` isn't in `nums`.

### Constraints

- `1 <= nums.length <= 5000`
- `-10^4 <= nums[i] <= 10^4`
- All values in `nums` are unique.
- `nums` is an ascending array that has possibly been rotated.
- `-10^4 <= target <= 10^4`

### Example

Input:

```text
nums = [4,5,6,7,0,1,2], target = 0
```

Output:

```text
4
```

Manual walkthrough:

```text
left=0, right=6 -> mid=3, nums[mid]=7. Left half [4..7] is sorted but
0 isn't in [4,7] -> search the right half, left=4
left=4, right=6 -> mid=5, nums[mid]=1. Left half [0,1] is sorted and
0 is in [0,1], but nums[mid]=1 != 0 and 1 > 0 -> right=4
left=4, right=4 -> mid=4, nums[mid]=0 == target -> return 4
```

---

## 2. Brute Force Approach

### Idea

Scan the array left to right and compare every element against `target`.
Rotation doesn't matter at all if every element is simply checked.

### Pseudocode

```text
function solve(nums, target)
    for i, num in nums
        if num == target
            return i
    return -1
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- Every element can be checked once, and in the worst case (target missing,
  or at the very end) all `n` elements are visited.

#### Space Complexity

```text
O(1)
```

Why?

- No extra structure is used beyond the loop index.

### Why this isn't good enough

The array is still "sorted" in pieces — rotation only breaks it into two
sorted runs glued together at one seam. A linear scan throws that structure
away entirely, even though half of the remaining search space could be
discarded on every comparison instead of just one.

---

## 3. Key Insight

### What makes this problem difficult?

A plain binary search assumes `nums[mid] < target` means the answer is
strictly to the right, but that's false once the array is rotated — the
seam can put small values on the right side and large values on the left.
The array can't be searched as a single sorted range.

### Key Observation

Even though the whole array isn't sorted, splitting it at `mid` always
leaves **at least one half completely sorted** (no seam in it). Comparing
`nums[left]` to `nums[mid]` reveals which half that is:

- `nums[left] <= nums[mid]` -> the left half `[left..mid]` is sorted.
- otherwise -> the right half `[mid..right]` is sorted.

Once the sorted half is known, a normal range check (`nums[left] <= target
<= nums[mid]`, or the mirror on the right) decides whether `target` lives
in that clean half or must be in the other, still-rotated half.

Example:

```text
nums = [4, 5, 6, 7, 0, 1, 2], target = 0

left=0, mid=3 -> nums[left]=4 <= nums[mid]=7, so [4,5,6,7] is sorted.
target=0 is not in [4,7], so it must be in the other half -> go right.
```

### Why does this observation help?

Every step still eliminates half the search space — it's ordinary binary
search, just with an extra check up front to figure out which comparison
rule (`<=` against the left half or `<=` against the right half) currently
applies.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture two sorted ramps glued end to end at the rotation point, like a
sorted list that got cut and swapped: `[4,5,6,7 | 0,1,2]`. Splitting at
`mid` always lands the seam entirely inside one of the two halves — the
other half is a clean, gap-free ramp. Check the clean ramp's range first;
if `target` isn't in it, the seam (and the answer, if it exists) must be on
the other side.

```text
[4, 5, 6, 7, 0, 1, 2]  target = 0
 left--------mid------right   mid=3, left half [4..7] is clean, 0 not in it -> go right
             [0, 1, 2]
             left-mid-right   mid=5, left half [0,1] is clean, 0 is in it -> narrow inside it
             [0]
             found
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
left <= right ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return -1          mid = left + (right-left)//2
                        │
                        ▼
                nums[left] <= nums[mid] ?
                        │
              ┌─────────┴─────────┐
              │                   │
             Yes                 No
        (left half sorted)  (right half sorted)
              │                   │
              ▼                   ▼
   nums[left] <= target      nums[mid] <= target
   <= nums[mid] ?            <= nums[right] ?
        │                         │
   ┌────┴────┐               ┌────┴────┐
   │         │               │         │
  Yes        No              Yes        No
   │         │               │         │
   ▼         ▼               ▼         ▼
target in            left = mid+1  target in           right = mid-1
left half          (search right   right half         (search left
   │               half, seam is       │               half, seam is
   ▼               there)              ▼               there)
nums[mid]==target?                nums[mid]==target?
   │                                    │
 ┌─┴──────────┐                    ┌────┴───────┐
 │            │                    │            │
Yes    nums[mid]<target?          Yes    nums[mid]<target?
 │            │                    │            │
 ▼            ▼                    ▼            ▼
Return mid  Yes: left=mid+1     Return mid   Yes: left=mid+1
            No: right=mid-1                  No: right=mid-1
   │                                    │
   └──────────────┬─────────────────────┘
                  ▼
        (loop back to left <= right ?)
```

Explanation of each decision:

- `left > right` is the base case — the search space is empty, so `target`
  isn't in the array.
- `nums[left] <= nums[mid]` tells which half has no seam: true means the
  left half `[left..mid]` is a clean ascending run.
- Inside a clean half, `nums[low] <= target <= nums[high]` decides whether
  `target` can only be in that half; if so, narrow with the ordinary
  `nums[mid] == / < / > target` rule. If not, `target` must be on the other
  (still-rotated) side, so the whole clean half is discarded in one step.

---

## 6. Plain English Algorithm

1. Set `left = 0` and `right = len(nums) - 1`.
2. While `left <= right`:
   - Compute `mid = left + (right - left) / 2`.
   - If `nums[left] <= nums[mid]`, the left half `[left..mid]` is sorted:
     - If `nums[left] <= target <= nums[mid]`, `target` belongs in this
       half — apply the usual rule: return `mid` on a match, otherwise move
       `left` to `mid + 1` if `nums[mid] < target`, else move `right` to
       `mid - 1`.
     - Otherwise `target` must be in the right half — move `left` to
       `mid + 1`.
   - Otherwise the right half `[mid..right]` is sorted:
     - If `nums[mid] <= target <= nums[right]`, `target` belongs in this
       half — apply the same match/narrow rule.
     - Otherwise `target` must be in the left half — move `right` to
       `mid - 1`.
3. If the loop ends without returning, `target` isn't in the array — return
   `-1`.

---

## 7. Pseudocode

```text
function solve(nums, target)
    left, right = 0, len(nums) - 1
    while left <= right
        mid = left + (right - left) // 2
        if nums[left] <= nums[mid]          # left half is sorted
            if nums[left] <= target <= nums[mid]
                if nums[mid] == target: return mid
                elif nums[mid] < target: left = mid + 1
                else: right = mid - 1
            else
                left = mid + 1
        else                                  # right half is sorted
            if nums[mid] <= target <= nums[right]
                if nums[mid] == target: return mid
                elif nums[mid] < target: left = mid + 1
                else: right = mid - 1
            else
                right = mid - 1
    return -1
```

---

## 8. Go Solution

```go
package solution

func search(nums []int, target int) int {
	left := 0
	right := len(nums) - 1

	for left <= right {
		mid := left + (right-left)/2

		if nums[left] <= nums[mid] {
			// sorted here
			if nums[left] <= target && nums[mid] >= target {
				if nums[mid] == target {
					return mid
				}

				if nums[mid] < target {
					left = mid + 1
				} else {
					right = mid - 1
				}
			} else {
				left = mid + 1
			}
		} else {
			// sorted here
			if nums[mid] <= target && nums[right] >= target {
				if nums[mid] == target {
					return mid
				}

				if nums[mid] < target {
					left = mid + 1
				} else {
					right = mid - 1
				}
			} else {
				right = mid - 1
			}
		}
	}

	return -1
}
```

---

## 9. Dry Run

Example:

```text
nums = [4, 5, 6, 7, 0, 1, 2], target = 0
```

| Step | `left` | `right` | `mid` | `nums[mid]` | Sorted half | Action | Why? |
|------|--------|---------|-------|-------------|-------------|--------|------|
| 1 | 0 | 6 | 3 | 7 | left `[4,5,6,7]` | `left = 4` | `0` not in `[4,7]`, must be in right half |
| 2 | 4 | 6 | 5 | 1 | left `[0,1]` | `right = 4` | `0` in `[0,1]` but `1 > 0`, narrow left |
| 3 | 4 | 4 | 4 | 0 | left `[0]` | Return `4` | `nums[mid] == target` |

Result: `4`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log n)
```

Why?

- Every iteration inspects one half to see if it's the sorted, seam-free
  one, then either narrows inside it or discards it entirely — either way
  the remaining search space halves each time, so the loop runs `O(log n)`
  times.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of index variables (`left`, `right`, `mid`) are used,
  regardless of input size.
