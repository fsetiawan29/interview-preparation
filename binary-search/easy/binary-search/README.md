# Problem: Binary Search

## 1. Problem Understanding

### Problem Summary

Given a **sorted** array of distinct integers `nums` and a `target` value,
return the index of `target` in `nums`, or `-1` if it isn't present. The
solution must run in `O(log n)` time.

### Input

- A sorted array of distinct integers, `nums`
- An integer, `target`

### Output

- The index of `target` in `nums`, or `-1` if `target` isn't in `nums`.

### Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 < nums[i], target < 10^4`
- All the integers in `nums` are unique.
- `nums` is sorted in ascending order.

### Example

Input:

```text
nums = [-1,0,3,5,9,12], target = 9
```

Output:

```text
4
```

Manual walkthrough:

```text
lo=0, hi=5 -> mid=2, nums[2]=3 < 9 -> lo=3
lo=3, hi=5 -> mid=4, nums[4]=9 == 9 -> return 4
```

---

## 2. Brute Force Approach

### Idea

Scan the array left to right and compare every element against `target`.

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

The array is sorted, but a linear scan throws that ordering away — it
never uses the fact that everything to the left of a smaller element is
also smaller, and everything to the right of a bigger element is also
bigger. That ordering is exactly what lets half the remaining candidates
be discarded on every comparison instead of just one.

---

## 3. Key Insight

### What makes this problem difficult?

It's tempting to just walk the array, but the problem explicitly asks for
`O(log n)`, which a single pass can never deliver. The array being sorted
is the whole point — it's the signal to reach for binary search instead of
a scan.

### Key Observation

Because `nums` is sorted, comparing `target` against the middle element
tells you which half the answer must be in (if it's there at all) — the
other half can be thrown away entirely, without ever looking at it.

Example:

```text
nums = [-1, 0, 3, 5, 9, 12], target = 9

mid = 2 -> nums[2] = 3 < 9
everything at indices 0..2 is <= 3, so it can't be 9 -> discard the left half
```

### Why does this observation help?

Each comparison eliminates half of what's left, so the search space shrinks
from `n` to `n/2` to `n/4` ... down to `1`, which is `O(log n)` steps
instead of `O(n)`.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture the array as a phone book: instead of reading every name, you open
it to the middle, see whether the name you want comes before or after that
page, and throw away the half you now know doesn't matter. Repeat on the
remaining half until only one page (or none) is left.

```text
[-1, 0, 3, 5, 9, 12]  target = 9
 lo------mid------hi        mid=3, discard left half (indices 0..2)
          [5, 9, 12]
          lo-mid-hi         mid=4, nums[4]=9 -> found
```

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
lo = 0, hi = len(nums) - 1
   │
   ▼
lo <= hi ?
   │
 ┌─┴──────────────────┐
 │                     │
No                    Yes
 │                     │
 ▼                     ▼
Return -1          mid = (lo + hi) // 2
                        │
                        ▼
                  nums[mid] == target ?
                        │
              ┌─────────┼─────────┐
              │         │         │
             Yes    nums[mid]  nums[mid]
              │      < target   > target
              ▼         │         │
          Return mid    ▼         ▼
                    lo = mid+1  hi = mid-1
                        │         │
                        └────┬────┘
                             ▼
                        (loop back to lo <= hi ?)
```

Explanation of each decision:

- `lo > hi` is the base case — the search space is empty, so `target` isn't
  in the array.
- `nums[mid] == target` is the success case — return immediately.
- `nums[mid] < target` means `target`, if present, is strictly to the
  right of `mid` — narrow to `[mid+1, hi]`.
- `nums[mid] > target` means `target`, if present, is strictly to the
  left of `mid` — narrow to `[lo, mid-1]`.

---

## 6. Plain English Algorithm

1. Set `lo = 0` and `hi = len(nums) - 1`.
2. While `lo <= hi`:
   - Compute `mid = lo + (hi - lo) // 2`.
   - If `nums[mid] == target`, return `mid`.
   - If `nums[mid] < target`, move `lo` to `mid + 1` (search the right
     half).
   - Otherwise, move `hi` to `mid - 1` (search the left half).
3. If the loop ends without returning, `target` isn't in the array —
   return `-1`.

---

## 7. Pseudocode

```text
function solve(nums, target)
    lo, hi = 0, len(nums) - 1
    while lo <= hi
        mid = lo + (hi - lo) // 2
        if nums[mid] == target
            return mid
        elif nums[mid] < target
            lo = mid + 1
        else
            hi = mid - 1
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
		if nums[mid] == target {
			return mid
		} else if nums[mid] < target {
			left = mid + 1
		} else {
			right = mid - 1
		}
	}

	return -1
}
```

---

## 9. Dry Run

Example:

```text
nums = [-1, 0, 3, 5, 9, 12], target = 9
```

| Step | `left` | `right` | `mid` | `nums[mid]` | Action | Why? |
|------|--------|---------|-------|-------------|--------|------|
| 1 | 0 | 5 | 2 | 3 | `3 < 9` -> `left = 3` | Target must be right of `mid` |
| 2 | 3 | 5 | 4 | 9 | `9 == 9` -> return `4` | Found the target |

Result: `4`

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
