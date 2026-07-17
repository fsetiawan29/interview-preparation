from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r, c, index):
            # 1. BASE CASE (matched full word)
            if index == len(word):
                return True
            
            # 2. PRUNE (out of bounds / mismatch / already visited)
            if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
                return False
            # 2.b if letter doesn't match
            if board[r][c] != word[index]:
                return False
            if board[r][c] == "#":
                return False

            # 3. PROCESS (mark cell as visited)
            board[r][c] = "#"

            # 4. RECURSE (explore 4 directions)
            found = dfs(r+1,c,index+1) or dfs(r-1,c,index+1) or dfs(r,c+1,index+1) or dfs(r,c-1,index+1)

            # 5. BACKTRACK (restore cell)
            board[r][c] = word[index]

            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False


def run_test(name, board, word, expected):
    result = Solution().exist([row[:] for row in board], word)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    print(f"  word:     {word}")
    print(f"  expected: {expected}")
    print(f"  got:      {result}")


if __name__ == "__main__":
    board1 = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]

    run_test("Example 1", board1, "ABCCED", True)
    run_test("Example 2", board1, "SEE", True)
    run_test("Example 3", board1, "ABCB", False)

    run_test(
        "Single cell match",
        [["A"]],
        "A",
        True,
    )

    run_test(
        "Single cell no match",
        [["A"]],
        "B",
        False,
    )

    run_test(
        "Reused cell not allowed",
        [["A", "A"]],
        "AAA",
        False,
    )
