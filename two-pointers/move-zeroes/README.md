# Problem

Name: Move Zeroes

Difficulty: Easy

----------------------------------------

# Pattern
Read pointer + Write pointer


----------------------------------------

# Recognition

Idea
- i scans every element to find non zero element
- j is zero element and will swap with non zero from i
- if i found non zero, swap with j and increment j


Steps

- INIT: `j = 0` — the write pointer, marks the next slot for a non-zero value
- SCAN: `for i in range(len(nums))` — the read pointer, walks the whole array
- SKIP ZERO: if `nums[i] == 0`, `continue` (leave `j` where it is)
- SWAP: if `i != j`, swap `nums[i]` and `nums[j]` (skip the swap when they're already equal to avoid a no-op write)
- ADVANCE: `j += 1`
- RETURN: nothing — `nums` is mutated in place; every 0 has been pushed past the final `j`

----------------------------------------

# Complexity

- Time: `O(n)` — single pass with `i`, `j` moves at most `n` times
- Space: `O(1)` — swapped in place, no extra structures
