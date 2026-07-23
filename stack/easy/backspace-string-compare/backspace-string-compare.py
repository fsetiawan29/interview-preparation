class Solution:
    def backspaceCompare_stack(self, s: str, t: str) -> bool:
        return self.build(s) == self.build(t)

    def build(self, s: str) -> list[str]:
        stack = []
        for ch in s:
            if ch == "#":
                if stack:
                    stack.pop()
            else:
                stack.append(ch)

        return stack

    def backspaceCompare_twopointer(self, s: str, t: str) -> bool:
        i = len(s) - 1
        j = len(t) - 1
        skip_s = 0
        skip_t = 0

        while i >= 0 or j >= 0:
            while i >= 0:
                if s[i] == "#":
                    skip_s += 1
                    i -= 1
                else:
                    if skip_s > 0:
                        skip_s -= 1
                        i -= 1
                    else:
                        break
            
            while j >= 0:
                if t[j] == "#":
                    skip_t += 1
                    j -= 1
                else:
                    if skip_t > 0:
                        skip_t -= 1
                        j -= 1
                    else:
                        break


            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:
                return False

            i -= 1
            j -= 1
        
        return True


def run_test(name, s, t, expected):
    for method in ("backspaceCompare_stack", "backspaceCompare_twopointer"):
        result = getattr(Solution(), method)(s, t)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    s={s!r}, t={t!r}")
        print(f"  expected: {expected}")
        print(f"  got:      {result}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "ab#c",
        "ad#c",
        True,
    )

    run_test(
        "Example 2",
        "ab##",
        "c#d#",
        True,
    )

    run_test(
        "Example 3",
        "a#c",
        "b",
        False,
    )
