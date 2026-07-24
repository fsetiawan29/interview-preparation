# Problem: Two Sum

## 1. Problem Understanding

### Problem Summary

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`. Each input has exactly one valid answer, and the same element cannot be used twice.

### Input

- An integer array `nums`
- An integer `target`

### Output

- An array of two indices `[i, j]` such that `nums[i] + nums[j] == target`.

### Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists.

### Example

Input:

```text
nums = [2,7,11,15], target = 9
```

Output:

```text
[0,1]
```

Manual walkthrough:

```text
nums = [2, 7, 11, 15], target = 9

At index 0, value 2: need a partner worth 9-2=7 -> not seen yet, remember 2 at index 0
At index 1, value 7: need a partner worth 9-7=2 -> 2 was already seen at index 0!

Return [0, 1]
```

---

# 2. Key Insight

## What makes this problem difficult?

Checking every pair of elements for a matching sum costs `O(n^2)`. It's tempting to loop over the array twice — once to pick a number, once to search for its partner — but that repeats work that could be remembered instead.

## Key Observation

For every number, its required partner (`target - num`) is a single fixed value. If we remember every number we've already visited (along with its index) in a hash map, we can check in `O(1)` average time whether the *current* number's partner has already appeared.

Example:

```text
nums = [3,2,4], target = 6

index 0, num=3: complement=6-3=3 -> not in seen -> remember 3 at index 0
index 1, num=2: complement=6-2=4 -> not in seen -> remember 2 at index 1
index 2, num=4: complement=6-4=2 -> 2 IS in seen (at index 1)! -> return [1, 2]
```

## Why does this observation help?

A single left-to-right pass suffices: for each number, first check if its complement was already seen (an `O(1)` average lookup), and only then store the current number. This turns the `O(n^2)` pairwise search into an `O(n)` pass.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture walking through the array once, carrying a notebook that records "value -> index" for every number already visited. Before writing today's number into the notebook, first ask: "does the notebook already have the exact partner I need?" If yes, you've found the pair. If no, write your own number down and move on.

```text
nums:  2   7   11   15         target = 9
notebook: {}

at 2: need partner 7 -> not in notebook -> write 2:0
notebook: {2:0}

at 7: need partner 2 -> 2 IS in notebook (index 0)! -> pair found: [0, 1]
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize seen = empty map
   │
   ▼
For each i, num in enumerate(nums):
   │
   ▼
complement = target - num
   │
   ▼
Is complement in seen ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return [seen[complement], i]   seen[num] = i
                                     │
                                     ▼
                               Next i (or Done)
```

Explanation of each decision:

- The complement check happens *before* storing the current number — this ordering prevents an element from pairing with itself.
- The moment a complement is found in `seen`, both indices (the earlier one from `seen`, and the current `i`) are returned.
- If no complement is found, the current number is stored for future lookups, and the scan continues.

---

# 5. Plain English Algorithm

1. Create an empty hash map `seen` (value -> index).
2. Scan `nums` left to right with index `i`. For each `num`:
   - Compute `complement = target - num`.
   - If `complement` is already in `seen`, return `[seen[complement], i]` immediately.
   - Otherwise, store `seen[num] = i`.
3. Since the problem guarantees exactly one solution, the function returns before the scan ends.

---

# 6. Pseudocode

```text
seen = empty map

for i, num in enumerate(nums)
    complement = target - num

    if complement in seen
        return [seen[complement], i]

    seen[num] = i
```

---

# 7. Python Solution

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
```

---

# 8. Dry Run

Example:

```text
nums = [2,7,11,15], target = 9
```

| Step | i | num | complement | In seen? | Action | seen after |
|------|---|-----|------------|----------|--------|-------------|
| 1 | 0 | 2 | 7 | No | Store 2:0 | {2:0} |
| 2 | 1 | 7 | 2 | Yes (seen[2]=0) | Return [0, 1] | — |

Result: `[0,1]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- A single pass over `nums`, with average `O(1)` hash map lookup and insert per element.

### Space Complexity

```text
O(n)
```

Why?

- Worst case (the matching pair is the last two elements checked), `seen` grows to hold nearly every element in `nums`.
