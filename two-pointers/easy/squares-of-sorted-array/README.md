# Problem: Squares of a Sorted Array

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` sorted in non-decreasing order, return a new array of the squares of each number, also sorted in non-decreasing order.

### Input

- An integer array `nums`, sorted in non-decreasing order (may contain negative numbers)

### Output

- A new array containing `nums[i] * nums[i]` for every `i`, sorted in non-decreasing order.

### Constraints

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is sorted in non-decreasing order.

### Example

Input:

```text
nums = [-4,-1,0,3,10]
```

Output:

```text
[0,1,9,16,100]
```

Manual walkthrough:

```text
Original

[-4,-1,0,3,10]

Square each value

↓

[16,1,0,9,100]

Sort the squares

↓

[0,1,9,16,100]
```

---

# 2. Key Insight

## What makes this problem difficult?

The array is sorted, but squaring can reorder things — negative numbers with large magnitude become large positive squares. Simply squaring in place and returning does **not** stay sorted, and re-sorting afterward costs `O(n log n)` when a linear solution is possible.

## Key Observation

Because `nums` is sorted, the value with the **largest square** is always at one of the two ends — either the most negative number (largest magnitude on the left) or the largest positive number (on the right). Whichever end has the bigger absolute value produces the next-largest square.

Example:

```text
[-4, -1, 0, 3, 10]
  ↑              ↑
 left           right

abs(-4)=4 < abs(10)=10 -> right has the bigger square right now
```

## Why does this observation help?

By comparing absolute values at both ends and always taking the bigger one, the biggest remaining square can be identified in `O(1)` per step. Filling the result array **from the back forward** means each comparison directly produces the next correctly-sorted position — no separate sort step needed.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture two readers standing at opposite ends of `nums`, and a writer starting at the back of a same-sized result array. On each step, the readers compare who has the bigger magnitude — that one's square gets written into the writer's current slot, and the writer steps one position to the left.

```text
nums:   [-4, -1, 0, 3, 10]
          ↑              ↑
        left            right

result: [_, _, _, _, _]
                        ↑
                      write

abs(-4)=4 < abs(10)=10 -> take nums[right]=10, square=100

result: [_, _, _, _, 100]
                     ↑
                   write (moved left)
```

Each step permanently fixes the correct value for the current write position — starting from the largest and working down to the smallest.

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize
left = 0
right = len(nums) - 1
write = len(nums) - 1
result = [0] * len(nums)
   │
   ▼
Is left <= right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is abs(nums[left]) >= abs(nums[right]) ?   Done — return result
 │
┌─┴────────┐
│          │
Yes        No
│          │
▼          ▼
result[write] = nums[left]^2   result[write] = nums[right]^2
left += 1                      right -= 1
│          │
└────┬─────┘
     ▼
  write -= 1
     │
     └──▶ (back to "Is left <= right ?")
```

Explanation of each decision:

- Comparing `abs(nums[left])` vs `abs(nums[right])` (not the raw values) is what correctly identifies the bigger square, since a large negative number squares to a large positive result.
- The loop condition is `left <= right`, not `<` — when only one element remains (`left == right`), it still needs to be placed.

---

# 5. Plain English Algorithm

1. Point `left` at the first index, `right` at the last index, and `write` at the last index of a new `result` array.
2. While `left` is less than or equal to `right`:
   - Compare `abs(nums[left])` and `abs(nums[right])`.
   - Whichever is bigger, square it and place it at `result[write]`, then move that pointer inward (`left` forward or `right` backward).
   - Move `write` one step left.
3. Once `left` passes `right`, `result` is fully filled in sorted order.

---

# 6. Pseudocode

```text
left = 0
right = length(nums) - 1
write = length(nums) - 1
result = new array of size length(nums)

while left <= right
    if abs(nums[left]) >= abs(nums[right])
        result[write] = nums[left] * nums[left]
        left++
    else
        result[write] = nums[right] * nums[right]
        right--

    write--

return result
```

---

# 7. Python Solution

```python
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        left = 0
        right = len(nums) - 1
        write = len(nums) - 1

        result = [0] * len(nums)
        while left <= right:
            if abs(nums[left]) >= abs(nums[right]):
                result[write] = nums[left] * nums[left]
                left += 1
            else:
                result[write] = nums[right] * nums[right]
                right -= 1

            write -= 1

        return result
```

---

# 8. Dry Run

Example:

```text
nums = [-7,-3,2,3,11]
```

| Step | Pointer(s) | Current Values | Action | Result State | Why? |
|------|------------|-----------------|--------|---------------|------|
| 1 | left=0, right=4, write=4 | -7, 11 | abs(11) bigger, write 121, right=3 | [_,_,_,_,121] | Right has bigger magnitude |
| 2 | left=0, right=3, write=3 | -7, 3 | abs(-7) bigger, write 49, left=1 | [_,_,_,49,121] | Left has bigger magnitude |
| 3 | left=1, right=3, write=2 | -3, 3 | abs equal, take left, write 9, left=2 | [_,_,9,49,121] | Tie resolved by taking left |
| 4 | left=2, right=3, write=1 | 2, 3 | abs(3) bigger, write 9, right=2 | [_,9,9,49,121] | Right has bigger magnitude |
| 5 | left=2, right=2, write=0 | 2 | Last element, write 4, left=3 | [4,9,9,49,121] | Only one element left |

Result: `[4,9,9,49,121]`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `left` and `right` together cross the array exactly once.
- `write` moves exactly `n` times, once per element.

### Space Complexity

```text
O(n)
```

Why?

- The `result` array holds `n` squared values.
- Excluding the output array, the extra state (`left`, `right`, `write`) is `O(1)`.
