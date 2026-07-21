# Problem

Name: 4Sum

Difficulty: Medium

----------------------------------------

# Pattern

Two Pointer + Sort

----------------------------------------

# Recognition

Idea
- Choose `i` at first array, `j` right after `i`
- Choose `left = j + 1`
- Choose `right = len(nums) - 1`
- Do iteration and calculation

Steps

- SORT: sort `nums` so duplicates sit next to each other and two-pointer narrowing is possible
- FIX `i`: iterate `i` from `0` to `len(nums) - 4`, skipping `i` if `nums[i] == nums[i-1]` (avoids duplicate quadruplets from the first slot)
- FIX `j`: iterate `j` from `i + 1` to `len(nums) - 3`, skipping `j` if `j > i + 1 and nums[j] == nums[j-1]` (avoids duplicate quadruplets from the second slot, but only relative to the current `i`)
- INIT: set `left = j + 1`, `right = len(nums) - 1`
- SCAN: while `left < right`, compute `total = nums[i] + nums[j] + nums[left] + nums[right]`
- NARROW: if `total < target` move `left += 1`; if `total > target` move `right -= 1`
- RECORD: if `total == target`, append `[nums[i], nums[j], nums[left], nums[right]]`, then move both `left += 1` and `right -= 1`, skipping any duplicate values at the new `left`/`right` before continuing the scan

Mistakes
- Chose the wrong starting position for `j`.
  - I initialized `j` at the end of the array.
  - The general solution is to initialize `j` immediately after `i` (`j = i + 1`).

- Incorrect early termination logic.
  - I stopped searching when the sum exceeded the target.
  - This optimization is only valid when the target is `0`; it does not apply to the general case.

- Skipped duplicate `j` values incorrectly.
  - **Before**
    ```python
    if j > 0 and nums[j] == nums[j - 1]:
        continue
    ```
  - **Correct**
    ```python
    if j > i + 1 and nums[j] == nums[j - 1]:
        continue
    ```
  - Only skip duplicates for the current `i`, not globally.

- Skipped duplicate values on the left pointer incorrectly after finding a valid triplet.
  - **Before**
    ```python
    while left < right and nums[left] == nums[left + 1]:
        left += 1
    ```
  - **Correct**
    ```python
    while left < right and nums[left] == nums[left - 1]:
        left += 1
    ```
  - Compare with the previously processed value after incrementing `left`.

- Skipped duplicate values on the right pointer incorrectly after finding a valid triplet.
  - **Before**
    ```python
    while left < right and nums[right - 1] == nums[right]:
        right -= 1
    ```
  - **Correct**
    ```python
    while left < right and nums[right] == nums[right + 1]:
        right -= 1
    ```
  - Compare with the previously processed value after decrementing `right`.

- Used the wrong upper bound for the `i` loop.
  - **Before**
    ```python
    range(len(nums) - 2)
    ```
  - **Correct**
    ```python
    range(len(nums) - 3)
    ```
  - Since `j = i + 1` and the two-pointer search requires at least two remaining elements, `i` should stop at `len(nums) - 4` (i.e., `range(len(nums) - 3)`).
    

----------------------------------------

# Complexity

- Time: `O(n^3)` — sorting is `O(n log n)`, then two nested loops over `i` and `j` (`O(n^2)`) each run a two-pointer scan across the rest of the array (`O(n)`), and the nested work dominates
- Space: `O(1)` extra — excluding the output array, only a constant number of pointers/indices are tracked (sorting itself may use `O(log n)`–`O(n)` auxiliary space depending on implementation)
