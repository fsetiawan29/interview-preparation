# Problem: Product of Array Except Self

## 1. Problem Understanding

### Problem Summary

Given an integer array `nums`, return an array `answer` such that `answer[i]` equals the product of all elements of `nums` except `nums[i]`, without using the division operator, and ideally in `O(1)` extra space (excluding the output array).

### Input

- An array of integers `nums`

### Output

- An array `answer` where `answer[i]` is the product of every element of `nums` except `nums[i]`.

### Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

### Example

Input:

```text
nums = [1,2,3,4]
```

Output:

```text
[24,12,8,6]
```

Manual walkthrough:

```text
nums = [1, 2, 3, 4]

answer[0] = 2*3*4 = 24   (everything except index 0)
answer[1] = 1*3*4 = 12   (everything except index 1)
answer[2] = 1*2*4 = 8    (everything except index 2)
answer[3] = 1*2*3 = 6    (everything except index 3)

Result: [24, 12, 8, 6]
```

---

# 2. Key Insight

## What makes this problem difficult?

The obvious approach — compute the total product, then divide by `nums[i]` for each `i` — is forbidden (no division), and also breaks when `nums` contains a `0`. Computing each `answer[i]` from scratch by multiplying all other elements would cost `O(n)` per index, `O(n^2)` overall — too slow for `n` up to `10^5`.

## Key Observation

`answer[i]` is just **(product of everything to the left of `i`) × (product of everything to the right of `i`)**. Both the "everything to the left" and "everything to the right" products can each be built incrementally in a single linear pass — no division needed, and no recomputation from scratch.

Example:

```text
nums = [1, 2, 3, 4]

prefix products (product of everything strictly before i):
  before index 0: 1 (empty product)
  before index 1: 1
  before index 2: 1*2 = 2
  before index 3: 1*2*3 = 6

suffix products (product of everything strictly after i), multiplied into the same slots,
combine with the prefix values already stored there to give the final answer.
```

## Why does this observation help?

Two linear passes — one left-to-right accumulating a running prefix product, one right-to-left accumulating a running suffix product — together build the full "everything except index i" product for every index, using only the output array and one running accumulator variable as extra space.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture standing at each index `i` and looking in two directions: everything to your left, and everything to your right. Multiply what you see in both directions together, and that's your answer.

```text
nums:     1     2     3     4
index:    0     1     2     3

At i=0: left of you = (nothing = 1), right of you = 2*3*4 = 24  -> answer[0] = 1*24 = 24
At i=1: left of you = 1,             right of you = 3*4 = 12    -> answer[1] = 1*12 = 12
At i=2: left of you = 1*2 = 2,       right of you = 4           -> answer[2] = 2*4 = 8
At i=3: left of you = 1*2*3 = 6,     right of you = (nothing=1) -> answer[3] = 6*1 = 6
```

Rather than recomputing "everything to the left/right" from scratch at every index, a running total is carried along as you sweep left-to-right (building the left side), then again right-to-left (building the right side and combining with what's already stored).

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize answer = [1, 1, ..., 1] (length n)
   │
   ▼
PREFIX PASS: running = 1
For i from 0 to n-1:
   answer[i] = running
   running = running * nums[i]
   │
   ▼
SUFFIX PASS: running = 1
For i from n-1 down to 0:
   answer[i] = answer[i] * running
   running = running * nums[i]
   │
   ▼
Done — return answer
```

Explanation of each decision:

- The prefix pass stores, at each `answer[i]`, the product of everything *before* `i` — `running` is updated with `nums[i]` only *after* storing, so `nums[i]` itself is never included.
- The suffix pass multiplies in the product of everything *after* `i` — again, `running` is updated with `nums[i]` only *after* using it, so `nums[i]` is never included in its own suffix product either.
- No division is used at any point; only running products and one multiplication per index per pass.

---

# 5. Plain English Algorithm

1. Create an `answer` array of the same length as `nums`, initialized to `1`.
2. **Prefix pass** — walk left to right with a running product `running` (starting at `1`):
   - Store `running` into `answer[i]` (this is the product of everything before `i`).
   - Multiply `running` by `nums[i]`.
3. **Suffix pass** — walk right to left with a fresh running product `running` (starting at `1`):
   - Multiply `answer[i]` by `running` (this brings in the product of everything after `i`).
   - Multiply `running` by `nums[i]`.
4. Return `answer`.

---

# 6. Pseudocode

```text
answer = array of 1's, length n

running = 1
for i from 0 to n-1
    answer[i] = running
    running = running * nums[i]

running = 1
for i from n-1 down to 0
    answer[i] = answer[i] * running
    running = running * nums[i]

return answer
```

---

# 7. Python Solution

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        answer = [1] * len(nums)

        running = 1
        for i in range(len(nums)):
            answer[i] = running
            running = running * nums[i]

        running = 1
        for i in range(len(nums)-1,-1,-1):
            answer[i] = answer[i] * running
            running = running * nums[i]

        return answer
```

---

# 8. Dry Run

Example:

```text
nums = [1,2,3,4]
```

Prefix pass (running starts at 1):

| Step | i | answer[i] = running | running after |
|------|---|----------------------|---------------|
| 1 | 0 | answer[0] = 1 | running = 1*1 = 1 |
| 2 | 1 | answer[1] = 1 | running = 1*2 = 2 |
| 3 | 2 | answer[2] = 2 | running = 2*3 = 6 |
| 4 | 3 | answer[3] = 6 | running = 6*4 = 24 |

`answer` after prefix pass: `[1, 1, 2, 6]`

Suffix pass (running resets to 1):

| Step | i | answer[i] = answer[i] * running | running after |
|------|---|-----------------------------------|---------------|
| 5 | 3 | answer[3] = 6*1 = 6 | running = 1*4 = 4 |
| 6 | 2 | answer[2] = 2*4 = 8 | running = 4*3 = 12 |
| 7 | 1 | answer[1] = 1*12 = 12 | running = 12*2 = 24 |
| 8 | 0 | answer[0] = 1*24 = 24 | running = 24*1 = 24 |

Final `answer`: `[24, 12, 8, 6]`, matching the expected output.

---

# 9. Complexity Analysis

### Time Complexity

```text
O(n)
```

Why?

- Two linear passes over `nums` (prefix pass, then suffix pass), each visiting every index exactly once.

### Space Complexity

```text
O(1) extra
```

Why?

- The `answer` array is required as output and isn't counted as extra space.
- Only a single `running` accumulator variable is used as additional state (reused across both passes).
