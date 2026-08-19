# Problem: Search Insert Position

## 1. Problem Understanding

### Problem Summary

Given a sorted array of distinct integers `nums` and a `target`, return the
index of `target` if it's found. If not, return the index where it would
be inserted to keep `nums` sorted — the first index whose value is
`>= target`.

### Input

- A sorted array of distinct integers, `nums`
- An integer, `target`

### Output

- The index of `target`, or the insertion index that keeps `nums` sorted.

### Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` contains distinct values sorted in ascending order.
- `-10^4 <= target <= 10^4`

### Example

Input:

```text
nums = [1,3,5,6], target = 2
```

Output:

```text
1
```

Manual walkthrough:

```text
2 isn't in [1,3,5,6].
The first value >= 2 is 3, at index 1.
Inserting 2 there keeps the array sorted: [1,2,3,5,6].
```

---

## 2. Brute Force Approach

### Idea

Scan the array left to right and return the index of the first element
that is `>= target`. If every element is smaller, `target` belongs at the
very end.

### Pseudocode

```text
function solve(nums, target)
    for i, num in nums
        if num >= target
            return i
    return len(nums)
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- Every element can be inspected once, and in the worst case (target
  larger than everything in `nums`) all `n` elements are visited.

#### Space Complexity

```text
O(1)
```

Why?

- No extra structure is used beyond the loop index.

### Why this isn't good enough

This is functionally correct and already used as the reference/fallback
implementation (`searchInsertBruteForce`), but it never uses the fact that
`nums` is sorted — it's `O(n)` even though the sortedness lets the same
answer be found in `O(log n)`.

---

## 3. Key Insight

### What makes this problem difficult?

It looks like classic binary search, but the target might not be in the
array at all — the loop has to converge on the *first index where the
condition `nums[i] >= target` becomes true*, not on an exact match. That's
a lower-bound search, not an exact-match search.

### Key Observation

The condition `nums[i] >= target` is monotonic across the sorted array:
it's `False` for every index before the insertion point and `True` for
every index from the insertion point onward. Binary search can find the
boundary between those two regions directly.

Example:

```text
nums = [1, 3, 5, 6], target = 2

nums[i] >= 2 ?  ->  F, T, T, T
                     ^ index 0 (1 < 2)
                        ^ index 1 (3 >= 2) <- boundary, this is the answer
```

### Why does this observation help?

Instead of scanning for the boundary one step at a time, binary search
narrows in on it by halving the range, the same way exact-match binary
search halves the range looking for an equal value.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture the array as a row of lockers, some labeled "too small" and the
rest labeled "big enough", with all the "too small" lockers on the left
and all the "big enough" ones on the right. The answer is the first
"big enough" locker — found by repeatedly checking the middle locker and
throwing away the half that can't contain the boundary.

```text
[1, 3, 5, 6]  target = 2
 lo-mid--hi        mid=1, nums[1]=3 >= 2 -> boundary is at or before mid, hi=mid-1
 lo-hi             mid=0, nums[0]=1 < 2  -> boundary is after mid, lo=mid+1
    lo>hi          loop ends, answer = lo = 1
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
Return left        mid = left + (right-left)//2
                        │
                        ▼
                  target == nums[mid] ?
                        │
              ┌─────────┼─────────┐
              │         │         │
             Yes    target <   otherwise
              │      nums[mid]  (target > nums[mid])
              ▼         │         │
          Return mid    ▼         ▼
                  right = mid-1  left = mid+1
                        │         │
                        └────┬────┘
                             ▼
                     (loop back to left <= right ?)
```

Explanation of each decision:

- `left > right` is the base case — the search space is empty, and `left`
  is exactly the first index where `nums[i] >= target`, i.e. the insertion
  point.
- `target == nums[mid]` is the exact-match case — return immediately.
- `target < nums[mid]` means the insertion point is at `mid` or to its
  left — narrow to `[left, mid-1]`, keeping `mid` as a candidate answer
  via `left`.
- `target > nums[mid]` means the insertion point is strictly to the right
  of `mid` — narrow to `[mid+1, right]`.

---

## 6. Plain English Algorithm

1. Set `left = 0` and `right = len(nums) - 1`.
2. While `left <= right`:
   - Compute `mid = left + (right - left) // 2`.
   - If `target == nums[mid]`, return `mid`.
   - If `target < nums[mid]`, move `right` to `mid - 1` (the insertion
     point is at or before `mid`).
   - Otherwise, move `left` to `mid + 1` (the insertion point is after
     `mid`).
3. When the loop ends, `left` has converged on the first index where
   `nums[i] >= target` — return `left`.

---

## 7. Pseudocode

```text
function solve(nums, target)
    left, right = 0, len(nums) - 1
    while left <= right
        mid = left + (right - left) // 2
        if target == nums[mid]
            return mid
        elif target < nums[mid]
            right = mid - 1
        else
            left = mid + 1
    return left
```

---

## 8. Go Solution

```go
package solution

func searchInsert(nums []int, target int) int {
	left := 0
	right := len(nums) - 1

	for left <= right {
		mid := left + (right-left)/2

		if target == nums[mid] {
			return mid
		} else if target < nums[mid] {
			right = mid - 1
		} else {
			left = mid + 1
		}
	}

	return left
}

func searchInsertBruteForce(nums []int, target int) int {
	for i, num := range nums {
		if num >= target {
			return i
		}
	}

	return len(nums)
}
```

---

## 9. Dry Run

Example:

```text
nums = [1, 3, 5, 6], target = 2
```

| Step | `left` | `right` | `mid` | `nums[mid]` | Action | Why? |
|------|--------|---------|-------|-------------|--------|------|
| 1 | 0 | 3 | 1 | 3 | `2 < 3` -> `right = 0` | Insertion point is at or before `mid` |
| 2 | 0 | 0 | 0 | 1 | `2 > 1` -> `left = 1` | Insertion point is after `mid` |
| 3 | 1 | 0 | — | — | `left > right` -> return `left` | Search space exhausted, `left` is the boundary |

Result: `1`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(log n)
```

Why?

- Each iteration discards half of the remaining search space, so the
  number of iterations before `left > right` is `O(log n)`.

### Space Complexity

```text
O(1)
```

Why?

- Only a fixed number of index variables (`left`, `right`, `mid`) are used,
  regardless of input size.
