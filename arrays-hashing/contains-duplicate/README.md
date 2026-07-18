# Problem

Name: Contains Duplicate

Difficulty: Easy

----------------------------------------

# Pattern

Hash Set

----------------------------------------

# Recognition

Idea
- Set
- Membership checking

Steps

- SHAPE: Hash Set
- CHECK: during iterate check if it's already in `seen`
- STORE: add `.add(n)` — storing the number

----------------------------------------

# Complexity

- Time: `O(n)` — single pass, O(1) average hash map lookup/insert per element
- Space: `O(n)` worst case, if no match is found until every element has been stored
