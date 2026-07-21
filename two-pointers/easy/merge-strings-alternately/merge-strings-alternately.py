class Solution:
    def mergeAlternatelyTwoPointer(self, word1: str, word2: str) -> str:
        res = []
        i = 0
        j = 0
        while i < len(word1) or j < len(word2):
            if i < len(word1):
                res.append(word1[i])
                i += 1
            
            if j < len(word2):
                res.append(word2[j])
                j += 1
        
        return "".join(res)

    def mergeAlternatelySingleIndex(self, word1: str, word2: str) -> str:
        res = []
        
        for i in range(max(len(word1),len(word2))):
            if i < len(word1):
                res.append(word1[i])
            
            if i < len(word2):
                res.append(word2[i])
        
        return "".join(res)


def run_test(name, word1, word2, expected):
    for method in ("mergeAlternatelyTwoPointer", "mergeAlternatelySingleIndex"):
        result = getattr(Solution(), method)(word1, word2)
        passed = result == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name} ({method})")
        print(f"  input:    word1={word1!r}, word2={word2!r}")
        print(f"  expected: {expected!r}")
        print(f"  got:      {result!r}")


if __name__ == "__main__":
    run_test(
        "Example 1",
        "abc",
        "pqr",
        "apbqcr",
    )

    run_test(
        "Example 2",
        "ab",
        "pqrs",
        "apbqrs",
    )

    run_test(
        "Example 3",
        "abcd",
        "pq",
        "apbqcd",
    )
