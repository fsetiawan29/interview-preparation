# Problem: 4Sum

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` and an integer `target`, find all unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that `a`, `b`, `c`, `d` are distinct indices and `nums[a] + nums[b] + nums[c] + nums[d] == target`. The returned quadruplets must not contain duplicate sets of four numbers.

### Input

- An integer array `nums`
- An integer `target`

### Output

- A list of all unique quadruplets that sum to `target`.

### Constraints

- `1 <= nums.length <= 200`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`

### Example

Input:

```text
nums = [1,0,-1,0,-2,2], target = 0
```

Output:

```text
[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
```

Manual walkthrough:

```text
Original

[1,0,-1,0,-2,2], target = 0

Sort first

↓

[-2,-1,0,0,1,2]

Fix i and j, then two-pointer the rest:

i=-2, j=-1: left=1, right=2 -> sum=0 -> [-2,-1,1,2]
i=-2, j=0(first 0): left=0, right=2 -> sum=0 -> [-2,0,0,2]
i=-2, j=0(second 0): duplicate j -> skipped
i=-1, j=0: left=0, right=1 -> sum=0 -> [-1,0,0,1]
i=0, j=0: no pair left sums to 0
```

---

# 2. Key Insight

## What makes this problem difficult?

4Sum is one dimension bigger than 3Sum — a brute-force check of every quadruplet is `O(n^4)`. It also carries the same duplicate-triplet trap as 3Sum, but now with **two** fixed indices instead of one, so duplicates must be skipped independently for each fixed slot.

## Key Observation

3Sum reduces to "fix one number, two-pointer the rest." 4Sum reduces the same way one level further: **fix two numbers** (`i` and `j`, both walked forward over the sorted array) and two-pointer the remaining two slots. Sorting again keeps duplicate values adjacent so they can be skipped cheaply, and it makes pointer narrowing predictable.

Example:

```text
[-2,-1,0,0,1,2], fix i=0 (-2), j=1 (-1)
         ↑              ↑
       left            right

nums[left] + nums[right] = 1 + 2 = 3
needed = target - nums[i] - nums[j] = 0 - (-2) - (-1) = 3 -> match!
```

## Why does this observation help?

Two nested loops (`i`, `j`) plus an inner two-pointer scan give `O(n^2)` for the fixed pair and `O(n)` for the scan, so the whole algorithm is `O(n^3)` instead of `O(n^4)`. Skipping repeated `nums[i]` and repeated `nums[j]` (relative to the current `i`), plus skipping repeated `left`/`right` values after a match, guarantees each distinct quadruplet is recorded only once.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture the sorted array as a line. Walk `i` forward as the outer anchor, and for each `i`, walk `j` forward right after it as the inner anchor. For each `(i, j)` pair, drop two readers at the opposite ends of what remains and let them walk inward exactly like Two Sum II, chasing a target of `target - nums[i] - nums[j]`.

```text
[-2, -1, 0, 0, 1, 2]
 i    j                      (two anchors)
        left           right (two pointers over the rest)

sum too small -> move left right
sum too big   -> move right left
sum == needed -> record quadruplet, then move both inward (skipping duplicates)
```

Whenever `i` or `j` repeats a value already tried (for the current outer context), skip it entirely — it would only reproduce quadruplets already found.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Sort nums
Initialize i = 0
   │
   ▼
Is i <= len(nums) - 4 ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is nums[i] == nums[i-1] ?   Return res
 │
┌─┴────────┐
│          │
Yes        No
│          │
▼          ▼
i += 1     Initialize j = i + 1
continue      │
              ▼
          Is j <= len(nums) - 3 ?
              │
        ┌─────┴──────┐
        │             │
       Yes            No
        │             │
        ▼             ▼
   Is nums[j]==nums[j-1] (and j>i+1)?    i += 1 (back to top)
        │
   ┌────┴────┐
   │         │
  Yes        No
   │         │
   ▼         ▼
  j+=1    left=j+1, right=len(nums)-1
  continue    │
              ▼
          Is left < right ?
              │
        ┌─────┴──────┐
        │             │
       Yes            No
        │             │
        ▼             ▼
   total = nums[i]+nums[j]+nums[left]+nums[right]   j += 1
        │                                            (back up)
        ▼
   Is total == target ?
        │
   ┌────┴─────┐
   │          │
  Yes         No
   │          │
   ▼          ▼
Record quad   total<target ? left+=1 : right-=1
left+=1, right-=1
skip dup left/right
   │
   └──▶ (back to "Is left < right ?")
```

Explanation of each decision:

- Sorting first is what makes duplicate-skipping and pointer-narrowing both work.
- Skipping a repeated `nums[i]` avoids re-finding quadruplets already produced by an earlier, identical outer anchor.
- Skipping a repeated `nums[j]` is scoped with `j > i + 1` — it only compares against the previous `j` under the *same* `i`, not globally.
- A `total` below target means the pair is too small — advance `left`. Above target means too big — retreat `right`.
- After recording a match, both pointers move inward and skip past duplicate values so the same quadruplet isn't recorded twice.

---

# 5. Plain English Algorithm

1. Sort `nums`.
2. For each index `i` from `0` to `len(nums) - 4`:
   - If `nums[i]` equals `nums[i-1]`, skip it.
   - For each index `j` from `i + 1` to `len(nums) - 3`:
     - If `j > i + 1` and `nums[j]` equals `nums[j-1]`, skip it.
     - Set `left = j + 1` and `right = len(nums) - 1`.
     - While `left < right`:
       - Compute `total = nums[i] + nums[j] + nums[left] + nums[right]`.
       - If `total < target`, advance `left`.
       - If `total > target`, retreat `right`.
       - If `total == target`, record `[nums[i], nums[j], nums[left], nums[right]]`, advance `left`, retreat `right`, then skip past duplicates on both sides.
3. Return all recorded quadruplets.

---

# 6. Pseudocode

```text
sort(nums)
res = []

for i from 0 to length(nums) - 4
    if i > 0 and nums[i] == nums[i-1]
        continue

    for j from i + 1 to length(nums) - 3
        if j > i + 1 and nums[j] == nums[j-1]
            continue

        left = j + 1
        right = length(nums) - 1

        while left < right
            total = nums[i] + nums[j] + nums[left] + nums[right]

            if total < target
                left++
            else if total > target
                right--
            else
                res.append([nums[i], nums[j], nums[left], nums[right]])
                left++
                right--

                while left < right and nums[left] == nums[left-1]
                    left++
                while left < right and nums[right] == nums[right+1]
                    right--

return res
```

---

# 7. Python Solution

```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()

        res = []
        for i in range(len(nums) - 3):
            if i > 0 and nums[i] == nums[i-1]:
                continue

            for j in range(i + 1, len(nums) - 2):
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue

                left = j + 1
                right = len(nums) - 1
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]

                    if total < target:
                        left += 1
                    elif total > target:
                        right -= 1
                    else:
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        right -= 1

                        while left < right and nums[left] == nums[left-1]:
                            left += 1
                        while left < right and nums[right] == nums[right+1]:
                            right -= 1
        return res
```

---

# 8. Dry Run

Example:

```text
nums = [1,0,-1,0,-2,2], target = 0

Sorted: [-2,-1,0,0,1,2]
Indices: 0   1  2 3 4 5
```

| Step | i,j (vals) | left,right (vals) | total | Action | Why? |
|------|------------|--------------------|-------|--------|------|
| 1 | i=0(-2), j=1(-1) | left=2(0), right=5(2) | -1 | left=3 | total < target (0) |
| 2 | i=0(-2), j=1(-1) | left=3(0), right=5(2) | -1 | left=4 | total < target |
| 3 | i=0(-2), j=1(-1) | left=4(1), right=5(2) | 0 | Record `[-2,-1,1,2]`, left=5, right=4, stop | Match; `left<right` now false |
| 4 | i=0(-2), j=2(0) | left=3(0), right=5(2) | 0 | Record `[-2,0,0,2]`, left=4, right=4, stop | Match; `left<right` now false |
| 5 | i=0(-2), j=3(0) | — | — | Skip `j` | `nums[3]==nums[2]` and `j>i+1` |
| 6 | i=1(-1), j=2(0) | left=3(0), right=5(2) | 1 | right=4 | total > target |
| 7 | i=1(-1), j=2(0) | left=3(0), right=4(1) | 0 | Record `[-1,0,0,1]`, left=4, right=3, stop | Match; `left<right` now false |
| 8 | i=1(-1), j=3(0) | — | — | Skip `j` | `nums[3]==nums[2]` and `j>i+1` |
| 9 | i=2(0), j=3(0) | left=4(1), right=5(2) | 3 | right=4, stop | total > target; `left<right` now false |

Result: `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]` — matches the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n^3)
```

Why?

- Sorting costs `O(n log n)`.
- Two nested loops over `i` and `j` are `O(n^2)`, and for each `(i, j)` pair the two-pointer scan is `O(n)`.
- The nested `O(n^2) * O(n)` work dominates the sort.

### Space Complexity

```text
O(1)
```

Why?

- Excluding the output array `res`, only a constant number of indices (`i`, `j`, `left`, `right`) are tracked.
- Sorting itself may use `O(log n)` to `O(n)` auxiliary space depending on the implementation, but no additional data structure is allocated by the algorithm.
