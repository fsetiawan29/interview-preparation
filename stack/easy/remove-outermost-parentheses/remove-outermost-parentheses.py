class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        res = []
        depth = 0
        i = 0
        
        while i < len(s):
            if s[i] == "(":
                if depth > 0:
                    res.append(s[i])
                
                depth += 1
            else:
                depth -= 1

                if depth > 0:
                    res.append(s[i])

            i += 1
        
        return "".join(res)


def run_test(name, s, expected):
    result = Solution().removeOuterParentheses(s)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  input:    s={s!r}")
    print(f"  expected: {expected!r}")
    print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "(()())(())",
        "()()()",
    )

    run_test(
        "Example 2",
        "(()())(())(()(()))",
        "()()()()(())",
    )

    run_test(
        "Example 3",
        "()()",
        "",
    )
