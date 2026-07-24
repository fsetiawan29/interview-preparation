# Problem: Two Sum II - Input Array Is Sorted

## 1. Problem Understanding

### Problem Summary

Given a 1-indexed array `numbers` sorted in non-decreasing order, find two numbers that add up to a specific `target`. Return the 1-indexed positions `[index1, index2]` of the two numbers, where `index1 < index2`. There is exactly one solution, and the same element may not be used twice.

### Input

- An integer array `numbers`, sorted in non-decreasing order
- An integer `target`

### Output

- A two-element list `[index1, index2]`, 1-indexed, such that `numbers[index1-1] + numbers[index2-1] == target`.

### Constraints

- `2 <= numbers.length <= 3 * 10^4`
- `-1000 <= numbers[i] <= 1000`
- `numbers` is sorted in non-decreasing order.
- `-1000 <= target <= 1000`
- Exactly one valid answer exists.

### Example

Input:

```text
numbers = [2,7,11,15], target = 9
```

Output:

```text
[1,2]
```

Manual walkthrough:

```text
Original

[2,7,11,15], target = 9

Try opposite ends:

2 + 15 = 17, too big -> move right end in
2 + 11 = 13, too big -> move right end in
2 + 7  = 9,  match!

↓

[1,2]  (1-indexed positions of 2 and 7)
```

---

# 2. Key Insight

## What makes this problem difficult?

The classic hash-map "complement lookup" solves this in `O(n)` time but uses `O(n)` extra space. Since `numbers` is already sorted, the problem is really asking whether there's a way to solve it in `O(n)` time **and** `O(1)` extra space by exploiting that order.

## Key Observation

In a sorted array, a pair's sum only moves in one predictable direction when a pointer moves: shifting the left pointer right strictly increases the sum, shifting the right pointer left strictly decreases it. That means the two-pointer scan can be steered directly by comparing the current sum to `target`.

Example:

```text
[2, 7, 11, 15], target = 9
 ↑            ↑
left        right

numbers[left] + numbers[right] = 2 + 15 = 17 > 9 -> sum too big, need smaller
```

## Why does this observation help?

If the current sum is too big, the only way to shrink it is to retreat `right` (advancing `left` could only make it bigger). If the sum is too small, the only way to grow it is to advance `left`. If the sum matches exactly, the answer is found. This lets the search finish in a single linear pass with no extra memory.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture two readers standing at opposite ends of the sorted array. Whenever their combined value is too big, the right reader steps inward to shrink it. Whenever it's too small, the left reader steps inward to grow it. They stop the instant their combined value matches `target`.

```text
[2, 7, 11, 15], target = 9
 left         right

2 + 15 = 17, too big -> right moves left

[2, 7, 11, 15]
 left      right

2 + 11 = 13, too big -> right moves left

[2, 7, 11, 15]
 left   right

2 + 7 = 9, match! -> return positions
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize left = 0, right = len(numbers) - 1
   │
   ▼
Is left < right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
candidate = numbers[left] + numbers[right]   (unreachable — a
   │                                          solution is guaranteed)
   ▼
Is candidate == target ?
   │
 ┌─┴────────┐
 │          │
Yes         No
 │          │
 ▼          ▼
Return       Is candidate > target ?
[left+1,        │
 right+1]  ┌────┴────┐
           │         │
          Yes        No
           │         │
           ▼         ▼
        right -= 1   left += 1
           │         │
           └────┬────┘
                ▼
     (back to "Is left < right ?")
```

Explanation of each decision:

- Sorting is already given, which is exactly what makes the pointer movement predictable.
- `candidate > target` means the sum is too big — retreat `right`, since that's the only direction that can shrink it.
- `candidate < target` means the sum is too small — advance `left`, since that's the only direction that can grow it.
- The problem guarantees exactly one solution, so the loop always terminates via the match branch.

---

# 5. Plain English Algorithm

1. Point `left` at index `0` and `right` at the last index.
2. While `left` is left of `right`:
   - Compute `candidate = numbers[left] + numbers[right]`.
   - If `candidate == target`, return `[left + 1, right + 1]` (1-indexed).
   - If `candidate > target`, retreat `right`.
   - Otherwise, advance `left`.

---

# 6. Pseudocode

```text
left = 0
right = length(numbers) - 1

while left < right
    candidate = numbers[left] + numbers[right]

    if candidate == target
        return [left + 1, right + 1]

    if candidate > target
        right--
    else
        left++
```

---

# 7. Python Solution

```python
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1

        while left < right:
            candidate = numbers[left] + numbers[right]
            if candidate == target:
                return [left + 1, right + 1]

            if candidate > target:
                right -= 1
            else:
                left += 1
```

---

# 8. Dry Run

Example:

```text
numbers = [2,7,11,15], target = 9
Indices:   0 1  2  3
```

| Step | left,right (vals) | candidate | Action | Why? |
|------|--------------------|-----------|--------|------|
| 1 | left=0(2), right=3(15) | 17 | right=2 | 17 > 9, too big |
| 2 | left=0(2), right=2(11) | 13 | right=1 | 13 > 9, too big |
| 3 | left=0(2), right=1(7) | 9 | Return `[1,2]` | 9 == target |

Result: `[1,2]` — matches the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `left` and `right` move toward each other and together cross the array at most once.
- Each iteration does constant work (one sum, one comparison).

### Space Complexity

```text
O(1)
```

Why?

- Only `left` and `right` are tracked as extra state.
- No hash map or auxiliary array is used.
