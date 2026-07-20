# Problem

Name: Remove Duplicates from Sorted Array

Difficulty: Easy

----------------------------------------

# Pattern

Read Pointer + Write Pointer



----------------------------------------

# Recognition

Idea
- Choose first element as unique element so start `j = 1` and `i = 1`
- No need to swap because the matters is only k-unique position
- Anything the `j` as write pointer

Mistakes
- Create `set` to check uniqueness. no need because already sorted
- Do swap logic and change with '_'. No need because the matteris is only k-unique position
- Do not return anything

Steps

- INIT: `j = 1` — the write pointer; `nums[0]` is always kept as the first unique value
- SCAN: `for i in range(1, len(nums))` — the read pointer
- CHECK: if `nums[i] != nums[j-1]` — `nums[i]` differs from the last written unique value, so it's a new unique value
- WRITE: `nums[j] = nums[i]`, then `j += 1`
- SKIP: if `nums[i] == nums[j-1]`, it's a duplicate — do nothing, `j` stays put
- RETURN: `j` — the count of unique elements; `nums[:j]` holds them in sorted order

----------------------------------------

# Complexity

- Time: `O(n)` — single pass, `i` scans every element once
- Space: `O(1)` — overwritten in place, no extra structures
