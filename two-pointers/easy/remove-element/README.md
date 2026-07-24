# Problem: Remove Element

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums` and an integer `val`, remove every occurrence of `val` in-place. The relative order of the remaining elements **may be changed**. Return `k`, the number of elements not equal to `val`, with those `k` values placed at the front of `nums`.

The modification must be done **in-place**, without allocating another array.

### Input

- An integer array `nums`
- An integer `val`

### Output

- An integer `k` — the count of elements not equal to `val`.
- `nums` modified in-place so its first `k` elements are the values to keep (order doesn't matter).

### Constraints

- `0 <= nums.length <= 100`
- `0 <= nums[i] <= 50`
- `0 <= val <= 100`

### Example

Input:

```text
nums = [0,1,2,2,3,0,4,2], val = 2
```

Output:

```text
5, nums = [0,1,4,0,3,_,_,_]
```

Manual walkthrough:

```text
Original

[0,1,2,2,3,0,4,2], val = 2

Every element equal to val (index 2, 3, 7) needs to disappear.

Since order doesn't matter, fill those gaps with values from the
end of the array instead of shifting everything left.

↓

Final kept values (order may vary): 0,1,4,0,3

k = 5
```

---

## 2. Brute Force Approach

### Idea

Build a new list of every value that isn't `val`, then copy it back into `nums`.

### Pseudocode

```text
kept = []
for x in nums
    if x != val
        kept.append(x)

k = length(kept)
for i = 0 to k - 1
    nums[i] = kept[i]

return k
```

### Complexity Analysis

#### Time Complexity

```text
O(n)
```

Why?

- One pass filters into `kept`, one pass copies back.

#### Space Complexity

```text
O(n)
```

Why?

- `kept` is a full second array — extra space the in-place constraint forbids.

### Why this isn't good enough

Since the problem explicitly allows the remaining elements' order to change, there's no need to preserve it (or use a second array) at all. Overwriting a `val` found at the front with a value taken from the back — shrinking the "active" range by one each time — removes every occurrence in `O(1)` extra space.

---

## 3. Key Insight

### What makes this problem difficult?

A naive approach shifts every element after a removed one — that's `O(n)` work per removal, and it feels necessary if you assume order must be preserved. But the problem explicitly says order **may** change, which opens up a much cheaper trick.

### Key Observation

Since order doesn't matter, whenever we find a `val` at the front, we don't need to shift the whole array — we can just **overwrite it with a value from the back** instead, and shrink the array's "active" range by one from the right.

Example:

```text
[0, 1, 2, 2, 3, 0, 4, 2], val = 2
       ↑                 ↑
     left               right

nums[left] == val -> replace it with nums[right], shrink from the right
```

### Why does this observation help?

This turns every removal into an `O(1)` operation — no shifting required. Two pointers closing in from opposite ends means each element is examined at most once, and the "back" values get reused to plug holes left by removed values at the front.

---

## 4. Mental Model

> What picture should I imagine in my head?

Picture `left` walking forward looking for values to remove, and `right` acting as a supply of "replacement" values from the unexamined tail. Whenever `left` finds a bad value, it grabs whatever `right` is holding, and `right` steps back — the new value at `left` hasn't been checked yet, so `left` doesn't move until it passes inspection.

```text
[0, 1, 2, 2, 3, 0, 4, 2], val = 2
 left                 right

nums[left]=0 != val -> keep, left advances

[0, 1, 2, 2, 3, 0, 4, 2]
    left              right

nums[left]=1 != val -> keep, left advances

[0, 1, 2, 2, 3, 0, 4, 2]
       left           right

nums[left]=2 == val -> overwrite with nums[right]=2... still bad, right shrinks and retries
```

The region `[left, right]` is the only part of the array still "in question" — everything outside it has already been decided.

---

## 5. Decision Tree

```text
(Start)
   │
   ▼
Initialize
left = 0
right = len(nums) - 1
   │
   ▼
Is left <= right ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Is nums[left] == val ?  Done — return left
 │
 ┌─┴────────────┐
 │              │
Yes             No
 │              │
 ▼              ▼
nums[left] = nums[right]   left is already a value to keep
right -= 1                 left += 1
(left stays — the new
 value still needs checking)
 │              │
 └──────┬───────┘
        ▼
 (back to "Is left <= right ?")
```

Explanation of each decision:

- `left <= right` (not `<`) matters: after copying `nums[right]` into `nums[left]`, that new value at `left` hasn't been validated yet, so the loop must run at least once more even if `left == right`.
- When `nums[left] == val`, `left` does **not** advance — the freshly copied value needs its own check next iteration.
- When `nums[left] != val`, it's confirmed good, so `left` advances.

---

## 6. Plain English Algorithm

1. Point `left` at the first index and `right` at the last index.
2. While `left` is less than or equal to `right`:
   - If `nums[left] == val`, overwrite it with `nums[right]` and shrink `right` by one — don't move `left` yet, since the new value needs checking.
   - Otherwise `nums[left]` is a value to keep — advance `left`.
3. Once `left > right`, every remaining value in `nums[0..left-1]` is a value to keep; return `left`.

---

## 7. Pseudocode

```text
left = 0
right = length(nums) - 1

while left <= right
    if nums[left] == val
        nums[left] = nums[right]
        right--
    else
        left++

return left
```

---

## 8. Python Solution

```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            if nums[left] == val:
                nums[left] = nums[right]
                right -= 1
            else:
                left += 1

        return left
```

---

## 9. Dry Run

Example:

```text
nums = [3,2,2,3], val = 3
```

| Step | Pointer(s) | Current Values | Action | Array State | Why? |
|------|------------|-----------------|--------|-------------|------|
| 1 | left=0, right=3 | nums[left]=3 | Overwrite with nums[right]=3, right=2 | [3,2,2,3] | left matches val |
| 2 | left=0, right=2 | nums[left]=3 | Overwrite with nums[right]=2, right=1 | [2,2,2,3] | New value at left still matches val |
| 3 | left=0, right=1 | nums[left]=2 | Keep, left=1 | [2,2,2,3] | left no longer matches val |
| 4 | left=1, right=1 | nums[left]=2 | Keep, left=2 | [2,2,2,3] | left no longer matches val |
| 5 | left=2, right=1 | — | Stop | [2,2,2,3] | `left <= right` is false |

Result: `k = 2`, kept values `[2, 2]`

---

## 10. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- `left` and `right` together cross the array once.
- Every element is examined at most once by `left`, and copied at most once by `right`.

### Space Complexity

```text
O(1)
```

Why?

- Overwritten in place.
- Only the two pointers `left` and `right` are used as extra state.
