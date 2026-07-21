# Problem

Name: Happy Number

Difficulty: Easy

----------------------------------------

# Pattern

Hash Set



----------------------------------------

# Recognition

Idea
- Calculate square value and use modulo and division to get each value
- Iterate `n` until number 0 return the sum in the `next_number` function
- While `n` not equal 1 and if it's in set, then return if `n == 1`, return `True`

Steps

- LOOP: while `n != 1`, check if `n` was already seen — if so, we're in a cycle that never reaches 1, so return `False`
- TRACK: add `n` to `seen`, then replace `n` with `next_number(n)`
- HELPER: `next_number` repeatedly peels off the last digit (`n % 10`), squares it, adds it to `res`, and strips it from `n` (`n //= 10`) until `n` is 0
- RETURN: once the loop exits, `n == 1`, so return `True`

----------------------------------------

# Complexity

- Time: `O(log n)` per `next_number` call (number of digits); overall bounded by a small constant number of iterations before hitting 1 or a repeat, since sums of squared digits fall into a bounded range quickly
- Space: `O(log n)` — `seen` stores the sequence of intermediate values until a cycle or 1 is found
