# Problem: Happy Number

## 1. Problem Understanding

### Problem Summary

A happy number is defined by this process: starting with a positive integer, replace it by the sum of the squares of its digits. Repeat until the number equals `1` (happy), or it loops endlessly in a cycle that never reaches `1` (not happy). Determine whether `n` is happy.

### Input

- An integer `n`

### Output

- `true` if `n` is a happy number, `false` otherwise.

### Constraints

- `1 <= n <= 2^31 - 1`

### Example

Input:

```text
n = 19
```

Output:

```text
true
```

Manual walkthrough:

```text
19 -> 1^2 + 9^2 = 1 + 81 = 82
82 -> 8^2 + 2^2 = 64 + 4 = 68
68 -> 6^2 + 8^2 = 36 + 64 = 100
100 -> 1^2 + 0^2 + 0^2 = 1

Reached 1 -> happy -> true
```

---

# 2. Key Insight

## What makes this problem difficult?

Repeatedly applying "sum of squared digits" could, in theory, run forever. Without some way to detect that we're going in circles, there's no obvious stopping condition besides reaching `1`.

## Key Observation

If a number ever repeats during this process, it's guaranteed to repeat forever from that point on — the sequence is deterministic, so revisiting a number means we've entered an unhappy cycle. Tracking every value seen so far in a hash set lets us detect that repeat immediately.

Example:

```text
n=19 -> 82 -> 68 -> 100 -> 1   (reaches 1, stop: happy)

n=2  -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4  (4 repeats!)
                                                    ↑        ↑
                                                 already seen -> cycle -> not happy
```

## Why does this observation help?

Instead of guessing how long to run the process, a `seen` set gives a clean, guaranteed stopping condition: either we hit `1` (happy) or we hit a number we've already visited (not happy, since it will cycle forever). The set turns an open-ended "does this loop forever?" question into a concrete check — "have I computed this exact value before?" — which always terminates.

---

# 3. Mental Model

> What picture should I imagine in my head?

Picture following a trail of numbers, dropping a marker at every number you visit. If you land on `1`, you've reached the destination — happy. If you ever step on a marker you already dropped, you're walking in a loop that will never reach `1` — not happy.

```text
19 --> 82 --> 68 --> 100 --> 1        (no repeats, reaches 1: happy)
 ●      ●      ●       ●       ●

2 --> 4 --> 16 --> 37 --> ... --> 4   (marker on 4 already dropped: not happy)
●      ●      ●      ●              ●(repeat!)
```

---

# 4. Decision Tree

```text
(Start)
   │
   ▼
Initialize seen = empty set
   │
   ▼
Is n == 1 ?
   │
 ┌─┴─────────────────┐
 │                    │
Yes                   No
 │                    │
 ▼                    ▼
Return true       Is n in seen ?
                       │
                     ┌─┴─────────┐
                     │            │
                    Yes           No
                     │            │
                     ▼            ▼
               Return false   Add n to seen
                                   │
                                   ▼
                             n = next_number(n)
                                   │
                                   └──▶ (back to "Is n == 1 ?")
```

Explanation of each decision:

- The loop keeps running as long as `n != 1` and `n` hasn't been seen before.
- Adding `n` to `seen` before transforming it ensures the current value is remembered for future cycle checks.
- Hitting a previously-seen value means the sequence is now looping without ever reaching `1`.

---

# 5. Plain English Algorithm

1. Create an empty hash set `seen`.
2. While `n` is not `1`:
   - If `n` is already in `seen`, we've detected a cycle — return `false`.
   - Add `n` to `seen`.
   - Replace `n` with the sum of the squares of its digits (via a helper `next_number`).
3. Once the loop exits, `n` equals `1`, so return `true`.
4. `next_number(n)`: repeatedly peel off the last digit (`n % 10`), square it and add it to a running sum, then strip that digit (`n //= 10`), until `n` is `0`. Return the sum.

---

# 6. Pseudocode

```text
seen = empty set

while n != 1
    if n in seen
        return false
    seen.add(n)
    n = next_number(n)

return true

function next_number(n)
    res = 0
    while n > 0
        digit = n % 10
        res += digit * digit
        n = n // 10
    return res
```

---

# 7. Python Solution

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()
        while n != 1:
            if n in seen:
                return False

            seen.add(n)
            n = self.next_number(n)

        return True

    def next_number(self, n: int) -> int:
        res = 0
        while n > 0:
            digit = n % 10
            res += (digit * digit)
            n //= 10
        return res
```

---

# 8. Dry Run

Example:

```text
n = 19
```

| Step | n (before) | In seen? | Action | next_number(n) | Why? |
|------|------------|----------|--------|-----------------|------|
| 1 | 19 | No | Add 19 to seen | 1²+9²=82 | n != 1, not seen yet |
| 2 | 82 | No | Add 82 to seen | 8²+2²=68 | n != 1, not seen yet |
| 3 | 68 | No | Add 68 to seen | 6²+8²=100 | n != 1, not seen yet |
| 4 | 100 | No | Add 100 to seen | 1²+0²+0²=1 | n != 1, not seen yet |
| 5 | 1 | — | Loop condition `n != 1` is false, exit | — | Reached 1 |

Result: `true`

---

# 9. Complexity Analysis

### Time Complexity

```text
O(log n) per step, bounded overall
```

Why?

- Each `next_number` call takes time proportional to the number of digits in `n`, i.e. `O(log n)`.
- In practice, the sum-of-squared-digits sequence quickly falls into a small bounded range (well under 1000) regardless of the starting value, so the number of iterations before hitting `1` or a repeat is bounded by a small constant.

### Space Complexity

```text
O(log n)
```

Why?

- `seen` stores every distinct intermediate value visited until a repeat or `1` is found, and each value has `O(log n)` digits.
