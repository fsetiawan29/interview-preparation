# Problem

Name: Majority Element

Difficulty: Easy

----------------------------------------

# Pattern
There are two approach:
- Hash Map
- Boyer-Moore

----------------------------------------

# Recognition

Idea
- Hash Map
    - Count the `threshold`
    - Iterate the `nums`
        - Count the frequency
        - If count > threshold, return the `n`
- Boyer-Moore
    - Count means summarize all pairwise cancellations
    - Iterate the `nums`
        - Check if current candidate still okay or not
        - Increase and decrease based on candidate and `n`

Steps

- Hash Map
    - INIT: `threshold = len(nums) // 2` and `freq` hash map
    - SCAN: for each `n` in `nums`, increment `freq[n]`
    - RETURN: as soon as `freq[n] > threshold`, return `n`
- Boyer-Moore
    - INIT: `candidate = None`, `count = 0`
    - SCAN: for each `n` in `nums`, if `count == 0` set `candidate = n`
    - VOTE: increment `count` if `n == candidate`, otherwise decrement it
    - RETURN: `candidate` after the full scan — the majority element always survives the cancellations since it outnumbers all others combined

----------------------------------------

# Complexity

- Hash Map
    - Time: `O(n)` — n = len(nums), single pass
    - Space: `O(n)` — worst case every element is distinct before the majority is found
- Boyer-Moore
    - Time: `O(n)` — n = len(nums), single pass
    - Space: `O(1)` — only `candidate` and `count` are tracked
