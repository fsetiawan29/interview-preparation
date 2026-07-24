# Problem: Contains Duplicate II

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` and an integer `k`, determine whether there are two distinct indices `i` and `j` such that `nums[i] == nums[j]` and the absolute difference between `i` and `j` is at most `k`.

### Input

- An integer array `nums`
- An integer `k`

### Output

- `true` if such a pair of indices exists, `false` otherwise.

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`
- `0 <= k <= 10^5`

### Example

Input:

```text
nums = [1,2,3,1], k = 3
```

Output:

```text
true
```

Manual walkthrough:

```text
nums: 1 2 3 1
      0 1 2 3   (indices)

nums[0] == nums[3] == 1
|0 - 3| = 3 <= k (3)

-> true
```

---

## 2. Brute Force Approach

### Idea

For every index `i`, look ahead at the next `k` positions and check whether any of them holds the same value. If a match with `nums[i]` turns up within that window, a valid duplicate exists.

### Pseudocode

```text
n = length(nums)

for i = 0 to n - 1
    for j = i + 1 to min(i + k, n - 1)
        if nums[i] == nums[j]
            return true

return false
```

### Complexity Analysis

#### Time Complexity

```text
O(n * k)
```

Why?

- There are `n = len(nums)` starting indices `i`.
- For each one, the inner loop checks up to `k` following elements.
- Total: `O(n * k)`, which hits `~10^10` operations at the given constraint (`n, k` up to `10^5`) — too slow.

#### Space Complexity

```text
O(1)
```

Why?

- No extra data structure is used — just the two loop indices.

### Why this isn't good enough

Every index `i` re-scans up to `k` elements ahead of it, even though the elements between `i` and `i + k` were mostly already looked at from a previous `i`. That repeated look-ahead is exactly what the sliding-window `set` eliminates.

---

## 3. Key Insight

### What makes this problem difficult?

Checking every pair `(i, j)` for equal values within distance `k` is an `O(n * k)` brute force — too slow when both `n` and `k` can reach `10^5`. We need to recognize a duplicate the moment it appears, without re-scanning the array around every index.

### Key Observation

Only the **last `k` elements** ever matter for a valid match at the current position — anything farther back is already too far away to satisfy `|i - j| <= k`. So instead of remembering the whole array, keep a sliding window of at most `k` recent values in a set. If the current value is already in that set, a valid duplicate exists.

Example:

```text
nums = [1, 0, 1, 1], k = 1

window after index 0: {1}
window after index 1: {0, 1}   (index 0 falls out once window exceeds size k)
index 2: nums[2] = 1 is in window -> duplicate within distance k
```

### Why does this observation help?

The set membership check is `O(1)` on average, and the window is maintained incrementally — one insert and at most one removal per step — so the whole scan stays `O(n)` instead of re-checking a range for every index.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture a "recent memory" of size `k` sliding across the array. Each new element is checked against that memory before being added to it. Once the memory holds more than `k` elements, the oldest one is forgotten.

```text
nums: 1  2  3  1
      [------]        window = {1, 2, 3} (size k=3)
         window slides, oldest entries forgotten as new ones arrive

nums[3] = 1 -> already in the window's memory -> duplicate found
```

If a value is ever seen while still in memory, it must be within `k` positions of its earlier occurrence — the window's size is the enforcement mechanism.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize window = {}, left = 0
   │
   ▼
For right = 0 .. len(nums)-1
   │
   ▼
Is nums[right] in window ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return true       Add nums[right] to window
                       │
                       ▼
                  Is right - left == k ?
                       │
                    ┌─┴─────────┐
                    │           │
                   Yes          No
                    │           │
                    ▼           ▼
             Remove nums[left]  (continue to next right)
             left += 1
                    │
                    └──▶ next right
                                │
                                ▼
                     Loop finished -> Return false
```

Explanation of each decision:

- Checking membership *before* inserting is what lets a match be detected — inserting first would let a value match itself.
- `right - left == k` means the window currently spans `k + 1` indices, one too many, so the oldest element is evicted to keep the window's span at `k`.
- Reaching the end of the loop without a match means no duplicate exists within distance `k` anywhere in the array.

---

## 6. Plain English Algorithm

1. Initialize an empty set `window` and `left = 0`.
2. For each `right` from `0` to `len(nums) - 1`:
   - If `nums[right]` is already in `window`, return `true` immediately.
   - Add `nums[right]` to `window`.
   - If `right - left == k`, the window has grown past size `k`, so remove `nums[left]` from `window` and advance `left`.
3. If the loop finishes without finding a match, return `false`.

---

## 7. Pseudocode

```text
window = {}
left = 0

for right = 0 to length(nums) - 1
    if nums[right] in window
        return true

    add nums[right] to window

    if right - left == k
        remove nums[left] from window
        left++

return false
```

---

## 8. Python Solution

```python
class Solution:
    def containsNearbyDuplicate_hashset(self, nums: List[int], k: int) -> bool:
        window = set()
        left = 0

        for right in range(len(nums)):
            if nums[right] in window:
                return True

            window.add(nums[right])

            if right - left == k:
                window.remove(nums[left])
                left += 1

        return False
```

---

## 9. Dry Run

Example:

```text
nums = [1, 0, 1, 1], k = 1
```

| Step | Pointer(s) | nums[right] | Action | window | Why? |
|------|------------|--------------|--------|--------|------|
| 1 | right=0, left=0 | 1 | Add 1 | {1} | Not in window; span (0) < k |
| 2 | right=1, left=0 | 0 | Add 0, then evict nums[0] | {0}, left=1 | 0 not in window; span (1) == k, evict oldest |
| 3 | right=2, left=1 | 1 | 1 is in window | {0} | Match found |
| — | — | — | Return `true` | — | Duplicate within distance k=1 |

Result: `true`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `n = len(nums)`; each index is added to the window exactly once and removed at most once.
- Set membership checks and insert/remove operations are `O(1)` on average.

### Space Complexity

```text
O(min(n, k))
```

Why?

- The window never holds more than `k` elements at a time.
- If `k >= n`, the window is bounded by `n` instead.
