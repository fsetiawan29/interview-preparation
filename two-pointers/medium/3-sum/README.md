# Problem

Name: 3Sum

Difficulty: Medium

----------------------------------------

# Pattern

Two Pointer + Sort

----------------------------------------

# Recognition

Idea
- Choose `i` at first array
- Choose `left = i + 1`
- Choose `right = len(nums) - 2`
- Do iteration and calculation

Steps

- SORT: sort `nums` so duplicates sit next to each other and two-pointer narrowing is possible
- FIX: iterate `i` from `0` to `len(nums) - 1`, skipping `i` if `nums[i] == nums[i-1]` (avoids duplicate triplets from the first slot)
- INIT: set `left = i + 1`, `right = len(nums) - 1`
- SCAN: while `left < right`, compute `total = nums[i] + nums[left] + nums[right]`
- NARROW: if `total < 0` move `left += 1`; if `total > 0` move `right -= 1`
- RECORD: if `total == 0`, append `[nums[i], nums[left], nums[right]]`, then move both `left += 1` and `right -= 1`, skipping any duplicate values at the new `left`/`right` before continuing the scan

Mistakes

- Forget to sort the `nums`
- Forget to skip it after we found it the triplet values.
- Forget to skip if `nums[i] > 0` then should be greater than 0, so we can skip it
- Because we need to two pointer after `i`, so we end loop until `len(nums) - 2`

----------------------------------------

# Complexity

- Time: `O(n^2)` — sorting is `O(n log n)`, then the outer loop over `i` (`O(n)`) runs a two-pointer scan across the rest of the array (`O(n)`), and the nested work dominates
- Space: `O(1)` extra — excluding the output array, only a constant number of pointers/indices are tracked (sorting itself may use `O(log n)`–`O(n)` auxiliary space depending on implementation)
