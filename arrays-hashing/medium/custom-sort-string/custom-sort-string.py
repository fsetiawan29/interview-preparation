class Solution:
    def customSortString(self, order: str, s: str) -> str:
        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1
        
        res = []
        for ch in order:
            if ch in freq:
                res.append(ch * freq[ch])
                del freq[ch]
            
        for ch, count in freq.items():
            res.append(ch * count)

        return "".join(res)


def is_valid_output(order, s, result):
    if sorted(result) != sorted(s):
        return False

    rank = {char: i for i, char in enumerate(order)}
    ranked_positions = [rank[char] for char in result if char in rank]

    return ranked_positions == sorted(ranked_positions)


def run_test(name, order, s, expected):
    result = Solution().customSortString(order, s)
    passed = is_valid_output(order, s, result) if result else False
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    order={order!r}, s={s!r}")
    print(f"  expected: {expected!r} (any valid permutation accepted)")
    print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "cba",
        "abcd",
        "cbad",
    )

    run_test(
        "Example 2",
        "bcafg",
        "abcd",
        "bcad",
    )
