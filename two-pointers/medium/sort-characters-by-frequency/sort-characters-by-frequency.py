from collections import Counter


class Solution:
    def frequencySort(self, s: str) -> str:
        freq = {}
        for char in s:
           freq[char] = freq.get(char, 0) + 1
        
        res = [[] for _ in range(len(s) + 1)]
        for char, count in freq.items():
            res[count].append(char)

        result = []
        for i in range(len(res)-1, -1, -1):
            for char in res[i]:
                result.append(char * i)

        return "".join(result)


def is_valid_arrangement(result, original):
    if Counter(result) != Counter(original):
        return False

    runs = []
    i = 0
    while i < len(result):
        j = i
        while j < len(result) and result[j] == result[i]:
            j += 1
        runs.append((result[i], j - i))
        i = j

    chars_seen = [char for char, _ in runs]
    if len(chars_seen) != len(set(chars_seen)):
        return False

    freqs = [freq for _, freq in runs]
    return freqs == sorted(freqs, reverse=True)


def run_test(name, s):
    result = Solution().frequencySort(s)
    passed = is_valid_arrangement(result, s)
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:  s={s!r}")
    print(f"  got:    {result!r}")


if __name__ == "__main__":
    run_test("Example 1", "tree")
    run_test("Example 2", "cccaaa")
    run_test("Example 3", "Aabb")
