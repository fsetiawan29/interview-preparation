# Problem

Name: Remove Element

Difficulty: Easy

----------------------------------------

# Pattern
Two Pointer


----------------------------------------

# Recognition

Idea
- Read/Write Pointer
- Opposite-ends pointer. Because "The order of the elements may be changed", then this approach more suitable

Mistakes
- Opposite-ends pointer approach
    - Use the condition left <= right because after replacing the value at left with one from the right, we still need to verify whether the new value at left should be kept or removed.

Steps

- Read/Write Pointer
    - INIT: `j = 0` — the write pointer
    - SCAN: `for i in range(len(nums))` — the read pointer
    - CHECK: if `nums[i] != val` — `nums[i]` is a value to keep
    - WRITE: `nums[j] = nums[i]`, then `j += 1`
    - SKIP: if `nums[i] == val`, do nothing — `j` stays put
    - RETURN: `j` — the count of elements not equal to `val`

- Opposite-ends Pointer
    - INIT: `left = 0`, `right = len(nums) - 1`
    - LOOP: while `left <= right`
    - CHECK: if `nums[left] == val` — replace it with `nums[right]` and `right -= 1` (the new `nums[left]` still needs checking, so `left` does not move)
    - ELSE: `nums[left] != val`, it's already a value to keep — `left += 1`
    - RETURN: `left` — the count of elements not equal to `val`

----------------------------------------

# Complexity

- Read/Write Pointer
    - Time: `O(n)` — single pass, `i` scans every element once
    - Space: `O(1)` — overwritten in place, no extra structures

- Opposite-ends Pointer
    - Time: `O(n)` — `left` and `right` together cross the array once
    - Space: `O(1)` — overwritten in place, no extra structures
