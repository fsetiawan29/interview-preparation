# Problem

Name: Product of Array Except Self

Difficulty: Medium

----------------------------------------

# Pattern

Prefix + Suffix

----------------------------------------

# Recognition

Idea

- Create list array `answer` as response
- Count the prefix and store it onto `answer` 
- Count the suffix and calculate with `answer` and update the `answer` data

Steps

- PREFIX PASS: walk left to right, keeping a `running` product of everything before index `i`; store it in `answer[i]` before multiplying `running` by `nums[i]`
- SUFFIX PASS: walk right to left with a fresh `running` product of everything after index `i`; multiply it into the existing `answer[i]`, then update `running` by `nums[i]`
- No division is used, and only the output array plus one `running` variable are needed, satisfying the `O(1)` extra space follow-up

----------------------------------------

# Complexity

- Time: `O(n)` — two linear passes over `nums`
- Space: `O(1)` extra — only the output array (not counted) and a single `running` accumulator

