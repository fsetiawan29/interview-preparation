# Problem

Name: Top K Frequent Elements

Difficulty: Medium

----------------------------------------

# Pattern

Hashing + Bucket Sort

----------------------------------------

# Recognition

Idea

- Count by frequency with key is the integer itself and store it in a dictionary
- Bucket sort by frequency instead of sorting — frequency can never exceed `len(nums)`, so it's a bounded value we can use as an index
- Store each number in the bucket whose index is its count

Steps

- COUNT: build `freq[n]` = how many times `n` appears in `nums`
- BUCKET: make `len(nums)+1` buckets (index 0..len(nums)); for each `n, c` in `freq`, append `n` to `buckets[c]`
- HARVEST: walk buckets from the highest index down to 1, appending every number found until `len(res) == k`

----------------------------------------

# Complexity

- Time: `O(n)` — counting is `O(n)`, bucketing is `O(n)` (at most `n` distinct keys), and harvesting visits at most `n` bucket slots
- Space: `O(n)` — the frequency dict and the buckets each hold at most `n` elements

