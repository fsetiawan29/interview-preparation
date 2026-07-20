# Problem

Name: Sort Characters By Frequency

Difficulty: Medium

----------------------------------------

# Pattern

Frequency Count


----------------------------------------

# Recognition

Idea
- get the frequency count
- create bucket with size is `len(s) + 1` 
- iterate from the high to low
- iterate each item in the index, append to result


Steps

- COUNT: build `freq`, a char → count map, one pass over `s`
- BUCKET: init `res`, a list of `len(s) + 1` empty lists — index = frequency, value = chars with that frequency
- FILL: for each `char, count` in `freq`, append `char` to `res[count]`
- SCAN: iterate `i` from `len(res) - 1` down to `0` (highest frequency first)
- APPEND: for each `char` in `res[i]`, append `char * i` to `result`
- RETURN: `"".join(result)`

----------------------------------------

# Complexity

- Time: `O(n)` — one pass to count, one pass over `n + 1` buckets (bounded by `n` total chars across buckets), no comparison sort needed
- Space: `O(n)` — `freq` and `res` both scale with the number of distinct characters / string length
