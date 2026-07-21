# Problem

Name: Longest Consecutive Sequence

Difficulty: Medium

----------------------------------------

# Pattern

Hash Set + Detect sequence starts

----------------------------------------

# Recognition

Idea

- Change into hash set to easy detect sequence start
- Sequence start means if we choose x then there's no x-1 in the hash set
- From each start, walk forward (x+1, x+2, ...) while the next number exists in the set, counting the streak length

Steps

- SET: dump `nums` into a hash set to get O(1) membership checks and drop duplicates
- FIND STARTS: for each `n` in the set, treat it as a sequence start only if `n-1` is not in the set
- WALK: from a start `n`, keep checking `n+1`, `n+2`, ... while present in the set, incrementing the streak length
- TRACK: keep the max streak length seen across all starts

----------------------------------------

# Complexity

- Time: `O(n)` — building the set is `O(n)`; the inner while loop only runs for true sequence starts, so across all iterations every number is visited by the inner loop at most once, keeping the total work `O(n)`
- Space: `O(n)` — the hash set holds up to `n` elements
