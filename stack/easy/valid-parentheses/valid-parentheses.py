class Solution:
    def isValid(self, s: str) -> bool:
        mapping = {
            '(': ')',
            "{": "}",
            "[": "]"
        }

        stack = []
        for ch in s:
            if ch in mapping:
                stack.append(ch)
            else:
                if not stack:
                    return False
                
                if mapping[stack.pop()] != ch:
                    return False

        return not stack


def run_test(name, s, expected):
    result = Solution().isValid(s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "()",
        True,
    )

    run_test(
        "Example 2",
        "()[]{}",
        True,
    )

    run_test(
        "Example 3",
        "(]",
        False,
    )

    run_test(
        "Example 4",
        "([])",
        True,
    )

    run_test(
        "Example 5",
        "([)]",
        False,
    )
