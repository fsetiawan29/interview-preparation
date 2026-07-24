# Sliding Window — Progress Tracker

## Blind 75 Sliding Window Problems

| Problem | Difficulty | Status |
|---|---|---|
| #3 Longest Substring Without Repeating Characters | Medium | Done |
| #424 Longest Repeating Character Replacement | Medium | Done |
| #567 Permutation in String | Medium | |
| #76 Minimum Window Substring | Hard | |
| #239 Sliding Window Maximum | Hard | |

## Level 1 — Fixed Window (Warm-up)

Goal: learn to slide a fixed-size window.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 1 | #643 Maximum Average Subarray I | Easy | | Done |
| 2 | #1456 Maximum Number of Vowels in a Substring of Given Length | Medium | | Done |
| 3 | #1343 Number of Sub-arrays of Size K and Average ≥ Threshold | Medium | | Done |
| 4 | #219 Contains Duplicate II | Easy | | Done |
| 5 | #2461 Maximum Sum of Distinct Subarrays With Length K | Medium | | Done |

- [x] #643 Maximum Average Subarray I
- [x] #1456 Maximum Number of Vowels in a Substring of Given Length
- [x] #1343 Number of Sub-arrays of Size K and Average ≥ Threshold
- [x] #219 Contains Duplicate II
- [x] #2461 Maximum Sum of Distinct Subarrays With Length K

**Patterns learned:** fixed window, running sum, hash set, hash map.

## Level 2 — Basic Variable Window

Goal: learn when to expand and shrink.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 6 | #209 Minimum Size Subarray Sum | Medium | | |
| 7 | #3 Longest Substring Without Repeating Characters | Medium | ✅ | Done |
| 8 | #904 Fruit Into Baskets | Medium | | |
| 9 | #1004 Max Consecutive Ones III | Medium | | |
| 10 | #1493 Longest Subarray of 1's After Deleting One Element | Medium | | |

- [ ] #209 Minimum Size Subarray Sum
- [x] #3 Longest Substring Without Repeating Characters (Blind 75)
- [ ] #904 Fruit Into Baskets
- [ ] #1004 Max Consecutive Ones III
- [ ] #1493 Longest Subarray of 1's After Deleting One Element

**Patterns learned:** expand right, shrink left, maintain a valid window.

## Level 3 — Sliding Window + Frequency

Goal: frequency arrays and hash maps.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 11 | #567 Permutation in String | Medium | ✅ | |
| 12 | #438 Find All Anagrams in a String | Medium | | Done |
| 13 | #424 Longest Repeating Character Replacement | Medium | ✅ | Done |
| 14 | #1208 Get Equal Substrings Within Budget | Medium | | |
| 15 | #1838 Frequency of the Most Frequent Element | Medium | | |

- [ ] #567 Permutation in String (Blind 75)
- [x] #438 Find All Anagrams in a String
- [x] #424 Longest Repeating Character Replacement (Blind 75)
- [ ] #1208 Get Equal Substrings Within Budget
- [ ] #1838 Frequency of the Most Frequent Element

**Patterns learned:** character counts, window validity, frequency maps.

## Level 4 — At Most K / Exactly K

Extremely common interview patterns.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 16 | #340 Longest Substring with At Most K Distinct Characters | Medium | | |
| 17 | #159 Longest Substring with At Most Two Distinct Characters | Medium | | |
| 18 | #992 Subarrays with K Different Integers | Hard | | |
| 19 | #713 Subarray Product Less Than K | Medium | | |
| 20 | #930 Binary Subarrays With Sum | Medium | | |

- [ ] #340 Longest Substring with At Most K Distinct Characters
- [ ] #159 Longest Substring with At Most Two Distinct Characters
- [ ] #992 Subarrays with K Different Integers
- [ ] #713 Subarray Product Less Than K
- [ ] #930 Binary Subarrays With Sum

**Patterns learned:** at most K, exactly K (via `atMost(K) - atMost(K-1)`), distinct elements.

## Level 5 — Advanced Variable Window

Interview favorites.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 21 | #76 Minimum Window Substring | Hard | ✅ | |
| 22 | #1358 Number of Substrings Containing All Three Characters | Medium | | |
| 23 | #1234 Replace the Substring for Balanced String | Medium | | |
| 24 | #2024 Maximize the Confusion of an Exam | Medium | | |
| 25 | #2781 Length of the Longest Valid Substring | Hard | | |

- [ ] #76 Minimum Window Substring (Blind 75)
- [ ] #1358 Number of Substrings Containing All Three Characters
- [ ] #1234 Replace the Substring for Balanced String
- [ ] #2024 Maximize the Confusion of an Exam
- [ ] #2781 Length of the Longest Valid Substring

**Patterns learned:** multiple conditions, frequency balancing, minimum valid window.

## Level 6 — Monotonic Queue (Sliding Window Maximum)

A different pattern than the previous levels.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 26 | #239 Sliding Window Maximum | Hard | ✅ | |
| 27 | #862 Shortest Subarray with Sum at Least K | Hard | | |

- [ ] #239 Sliding Window Maximum (Blind 75)
- [ ] #862 Shortest Subarray with Sum at Least K

**Patterns learned:** deque, monotonic queue.

## Level 7 — Interview Challenge

These combine multiple ideas.

| # | Problem | Difficulty | Blind 75 | Status |
|---|---|---|---|---|
| 28 | #30 Substring with Concatenation of All Words | Hard | | |
| 29 | #632 Smallest Range Covering Elements from K Lists | Hard | | |
| 30 | #480 Sliding Window Median | Hard | | |

- [ ] #30 Substring with Concatenation of All Words
- [ ] #632 Smallest Range Covering Elements from K Lists
- [ ] #480 Sliding Window Median

## Must-Know Problems

If short on time before interviews, prioritize these:

**Beginner**
- [x] #643 Maximum Average Subarray I
- [ ] #209 Minimum Size Subarray Sum

**Core**
- [x] #3 Longest Substring Without Repeating Characters (Blind 75)
- [ ] #567 Permutation in String (Blind 75)
- [ ] #438 Find All Anagrams in a String
- [x] #424 Longest Repeating Character Replacement (Blind 75)

**Advanced**
- [ ] #76 Minimum Window Substring (Blind 75)
- [ ] #239 Sliding Window Maximum (Blind 75)

## Recommended Order

1. **Stage 1 – Learn the basics:** #643, #219
2. **Stage 2 – Learn variable windows:** #3, #209
3. **Stage 3 – Learn frequency maps:** #567, #438
4. **Stage 4 – More advanced windows:** #424, #904, #1004
5. **Stage 5 – Interview-level mastery:** #76, #239
