# Problem: 3Sum

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums`, find all unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. The returned triplets must not contain duplicate sets of three numbers.

### Input

- An integer array `nums`

### Output

- A list of all unique triplets that sum to zero.

### Constraints

- `3 <= nums.length <= 3000`
- `-10^5 <= nums[i] <= 10^5`

### Example

Input:

```text
nums = [-1,0,1,2,-1,-4]
```

Output:

```text
[[-1,-1,2],[-1,0,1]]
```

Manual walkthrough:

```text
Original

[-1,0,1,2,-1,-4]

Sort first

↓

[-4,-1,-1,0,1,2]

Fix the first number i, then use two pointers on the rest:

i=-4: no pair on the right sums to 4 -> nothing found
i=-1 (first -1): left=-1, right=2 -> sum=0 -> [-1,-1,2]
             left=0,  right=1 -> sum=0 -> [-1,0,1]
i=-1 (second -1): duplicate of previous i -> skipped
i=0: no pair sums to 0
```

---

## 2. Brute Force Approach

### Idea

Check every triplet of indices directly, using a set to drop duplicate triplets.

### Pseudocode

```text
n = length(nums)
res = empty set of sorted tuples

for i = 0 to n - 1
    for j = i + 1 to n - 1
        for k = j + 1 to n - 1
            if nums[i] + nums[j] + nums[k] == 0
                triplet = sorted([nums[i], nums[j], nums[k]])
                res.add(tuple(triplet))

return list(res)
```

### Complexity Analysis

#### Time Complexity

```text
O(n^3)
```

Why?

- There are `O(n^3)` triplets `(i, j, k)` with `i < j < k`, each checked in `O(1)`.

#### Space Complexity

```text
O(n)
```

Why?

- `res`, a set of sorted tuples used to drop duplicates, holds at most `O(n)` unique triplets in the worst case.

### Why this isn't good enough

Every triplet is checked individually, and duplicates are only caught after the fact by hashing sorted tuples. Sorting `nums` first turns "find two numbers summing to `-nums[i]`" into a linear two-pointer scan, and lets duplicate values be skipped directly (since they sit adjacent) instead of relying on a set — dropping the whole search from `O(n^3)` to `O(n^2)`.

---

## 3. Key Insight

### What makes this problem difficult?

A brute-force check of every triplet is `O(n^3)`. On top of that, the problem demands **unique** triplets, so naively collecting results and then deduplicating (e.g. with a set of sorted tuples) wastes time and space compared to avoiding duplicates during the scan itself.

### Key Observation

Once `nums` is **sorted**, fixing one number `nums[i]` reduces the problem to "find two numbers in the remainder that sum to `-nums[i]`" — exactly the opposite-ends two-pointer pattern used in Two Sum II. Sorting also makes duplicate values sit next to each other, so they can be skipped with a simple adjacent-value check.

Example:

```text
[-4,-1,-1,0,1,2], fix i=1 (nums[i]=-1)
      ↑                  ↑
    left                right

nums[left] + nums[right] = -1 + 2 = 1
target for the pair = -nums[i] = 1 -> match!
```

### Why does this observation help?

Instead of a third nested loop, the inner search becomes a linear two-pointer scan (`O(n)`), so the whole algorithm is `O(n^2)` instead of `O(n^3)`. Skipping a repeated `nums[i]` (and repeated `left`/`right` values after a match) guarantees each distinct triplet is only recorded once.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture the sorted array as a line. Walk `i` forward one step at a time as the "anchor". For each anchor, drop two readers at the opposite ends of the remaining line and let them walk inward exactly like Two Sum II, chasing a target of `-nums[i]`.

```text
[-4, -1, -1, 0, 1, 2]
 i                        (anchor)
     left              right   (two pointers over the rest)

sum too small -> move left right
sum too big   -> move right left
sum == 0      -> record triplet, then move both inward (skipping duplicates)
```

Whenever the anchor `i` repeats a value already tried, skip it entirely — it would only reproduce triplets already found.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Sort nums
Initialize i = 0
   │
   ▼
Is i < len(nums) ?
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
i += 1     left = i+1, right = len(nums)-1
continue      │
              ▼
          Is left < right ?
              │
            ┌─┴─────────────────┐
            │                   │
           Yes                  No
            │                   │
            ▼                   ▼
       total = nums[i]+nums[left]+nums[right]   i += 1
            │                                   (back to top)
            ▼
       Is total == 0 ?
            │
      ┌─────┴──────┐
      │             │
     Yes            No
      │             │
      ▼             ▼
  Record triplet   total < 0 ? left += 1 : right -= 1
  left+=1, right-=1
  skip dup left/right
      │
      └──▶ (back to "Is left < right ?")
```

Explanation of each decision:

- Sorting first is what makes both the duplicate-skip and the pointer-narrowing logic work.
- Skipping a repeated `nums[i]` avoids re-finding triplets already produced by an earlier, identical anchor.
- A negative `total` means the pair is too small — advance `left` (bigger sorted values lie to the right).
- A positive `total` means the pair is too big — retreat `right` (smaller sorted values lie to the left).
- After recording a match, both pointers move inward and skip past any duplicate values, so the same triplet can't be recorded twice.

---

## 6. Plain English Algorithm

1. Sort `nums`.
2. For each index `i` from `0` to `len(nums) - 1`:
   - If `nums[i]` equals `nums[i-1]`, skip it (avoids duplicate triplets from the anchor slot).
   - Set `left = i + 1` and `right = len(nums) - 1`.
   - While `left < right`:
     - Compute `total = nums[i] + nums[left] + nums[right]`.
     - If `total < 0`, advance `left`.
     - If `total > 0`, retreat `right`.
     - If `total == 0`, record `[nums[i], nums[left], nums[right]]`, advance `left`, retreat `right`, then keep advancing `left` past duplicates and keep retreating `right` past duplicates.
3. Return all recorded triplets.

---

## 7. Pseudocode

```text
sort(nums)
res = []

for i from 0 to length(nums) - 1
    if i > 0 and nums[i] == nums[i-1]
        continue

    left = i + 1
    right = length(nums) - 1

    while left < right
        total = nums[i] + nums[left] + nums[right]

        if total < 0
            left++
        else if total > 0
            right--
        else
            res.append([nums[i], nums[left], nums[right]])
            left++
            right--

            while left < right and nums[left] == nums[left-1]
                left++
            while left < right and nums[right] == nums[right+1]
                right--

return res
```

---

## 8. Python Solution

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()

        res = []
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i-1]:
                continue

            left = i + 1
            right = len(nums) - 1
            while left < right:
                count = nums[i] + nums[left] + nums[right]

                if count < 0:
                    left += 1
                elif count > 0:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1

                    while left < right and nums[left] == nums[left-1]:
                        left += 1
                    while left < right and nums[right] == nums[right+1]:
                        right -= 1
        return res
```

---

## 9. Dry Run

Example:

```text
nums = [-1,0,1,2,-1,-4]

Sorted: [-4,-1,-1,0,1,2]
Indices: 0   1  2  3 4 5
```

| Step | i (val) | left,right (vals) | total | Action | Why? |
|------|---------|--------------------|-------|--------|------|
| 1 | i=0 (-4) | left=1(-1), right=5(2) | -3 | left=2 | total < 0 |
| 2 | i=0 (-4) | left=2(-1), right=5(2) | -3 | left=3 | total < 0 |
| 3 | i=0 (-4) | left=3(0), right=5(2) | -2 | left=4 | total < 0 |
| 4 | i=0 (-4) | left=4(1), right=5(2) | -1 | left=5, stop | `left < right` now false |
| 5 | i=1 (-1) | left=2(-1), right=5(2) | 0 | Record `[-1,-1,2]`, left=3, right=4 | Match, no dup at new positions |
| 6 | i=1 (-1) | left=3(0), right=4(1) | 0 | Record `[-1,0,1]`, left=4, right=3, stop | Match; loop ends since `left < right` false |
| 7 | i=2 (-1) | — | — | Skip `i` | `nums[2] == nums[1]` (duplicate anchor) |
| 8 | i=3 (0) | left=4(1), right=5(2) | 3 | right=4 | total > 0 |
| 9 | i=3 (0) | left=4, right=4 | — | Stop | `left < right` false |
| 10 | i=4, i=5 | — | — | Loop bodies don't run | `left < right` false immediately |

Result: `[[-1,-1,2],[-1,0,1]]` — matches the expected output.

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n^2)
```

Why?

- Sorting costs `O(n log n)`.
- The outer loop over `i` is `O(n)`, and for each `i` the two-pointer scan across the remaining elements is `O(n)`.
- The nested `O(n) * O(n)` work dominates the sort.

### Space Complexity

```text
O(1)
```

Why?

- Excluding the output array `res`, only a constant number of indices (`i`, `left`, `right`) are tracked.
- Sorting itself may use `O(log n)` to `O(n)` auxiliary space depending on the implementation, but no additional data structure is allocated by the algorithm.
