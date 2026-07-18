# Problem

Name: Two Sum

Difficulty: Easy

----------------------------------------

# Pattern

Hash Table — Complement Lookup

----------------------------------------

# Recognition

Idea
- Dictionary
- Complement idea

Steps

- SHAPE: Complement lookup
- CHECK: before touching `seen`, ask "does my partner already exist?" — look up `target - num` in `seen`
- STORE: only *after* the check, add `seen[num] = i` — storing before checking would let an element pair with itself

----------------------------------------

# Complexity

- Time: `O(n)` — single pass, O(1) average hash map lookup/insert per element
- Space: `O(n)` worst case, if no match is found until every element has been stored
