from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode()
        dummy.next = head

        fast = dummy
        slow = dummy

        # Phase A: move fast forward n+1 steps, creating a gap of n nodes
        for _ in range(n + 1):
            fast = fast.next

        # Phase B: move both forward together until fast falls off the end
        while fast is not None:
            fast = fast.next
            slow = slow.next

        # slow is now sitting right before the target node — splice it out
        slow.next = slow.next.next

        return dummy.next


# ---------- Helpers for local testing ----------

def build_linked_list(values):
    """Convert a Python list into a linked list, return the head."""
    dummy = ListNode()
    curr = dummy
    for v in values:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next


def linked_list_to_list(head):
    """Convert a linked list back into a Python list, for easy comparing/printing."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


# ---------- Test cases ----------

if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),  # remove 4
        ([1], 1, []),                        # remove the only node
        ([1, 2], 1, [1]),                    # remove tail
        ([1, 2], 2, [2]),                    # remove head
    ]

    for values, n, expected in test_cases:
        head = build_linked_list(values)
        result_head = sol.removeNthFromEnd(head, n)
        result = linked_list_to_list(result_head)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: input={values}, n={n} -> got={result}, expected={expected}")