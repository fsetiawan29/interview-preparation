# Linked List

## What is this pattern?

A **linked list** is a chain of nodes where each node holds a value and a
pointer (`next`, and for doubly linked lists, `prev`) to another node,
instead of living at a contiguous, indexable memory offset like an array.
That trade-off is the whole story: no random access (`O(n)` to reach the
`k`-th node), but `O(1)` insertion/removal once you're holding the right
node — no shifting elements like an array requires.

Use this pattern when the problem is about:
- Traversing or rewiring a chain of nodes (`ListNode`, `head`/`next`)
- Detecting a **cycle**, finding the **middle**, or finding the
  **k-th-from-end** node without knowing the length up front
- **Reversing** all or part of a list, or merging/splitting lists
- Keywords like "linked list", "head", "reverse", "cycle", "merge k
  sorted lists", "LRU cache", "doubly linked", "circular"

## The general shape

**Traversal** — walk the chain until `None`:
```python
def solve(head):
    curr = head
    while curr:
        # process curr
        curr = curr.next
```

**Dummy node** — sidesteps special-casing the head when it might be
removed/replaced; return `dummy.next` at the end:
```python
def solve(head):
    dummy = ListNode(0, head)
    prev, curr = dummy, head
    while curr:
        # decide whether to unlink curr, or advance prev
        curr = curr.next
    return dummy.next
```

**Fast & slow pointers** — `slow` moves one step, `fast` moves two; when
`fast` reaches the end, `slow` is at the middle. If the list has a cycle,
`fast` and `slow` are guaranteed to meet inside it:
```python
def solve(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True  # cycle detected
    return False
```

**In-place reversal** — rewire `next` pointers one at a time, keeping a
`prev` trailer:
```python
def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev  # new head
```

## Common sub-patterns

**Fixed-distance two pointers** (k-th from end: advance one pointer `k`
steps first, then move both together)
*(no solutions yet)*
```python
fast = slow = dummy = ListNode(0, head)
for _ in range(k):
    fast = fast.next
while fast.next:
    fast = fast.next
    slow = slow.next
# slow.next is the k-th node from the end
```

**Merge two sorted lists** (splice nodes onto a dummy tail, no new nodes
allocated)
*(no solutions yet)*
```python
dummy = tail = ListNode()
while l1 and l2:
    if l1.val <= l2.val:
        tail.next, l1 = l1, l1.next
    else:
        tail.next, l2 = l2, l2.next
    tail = tail.next
tail.next = l1 or l2
return dummy.next
```

**Cycle entry point** (Floyd's algorithm, part 2: after slow/fast meet,
reset one pointer to `head` and advance both one step at a time — they
meet again exactly at the cycle's start)
*(no solutions yet)*
```python
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
    if slow is fast:
        ptr = head
        while ptr is not slow:
            ptr, slow = ptr.next, slow.next
        return ptr  # cycle start
return None
```

**HashMap + node mapping** (copy list with random pointer / detect
intersection: use identity, not value, as the map key)
*(no solutions yet)*
```python
old_to_new = {}
curr = head
while curr:
    old_to_new[curr] = Node(curr.val)
    curr = curr.next
curr = head
while curr:
    old_to_new[curr].next = old_to_new.get(curr.next)
    old_to_new[curr].random = old_to_new.get(curr.random)
    curr = curr.next
```

## Complexity

- **Time:** `O(n)` for a single traversal-based pass; `O(n log n)` for
  merge-sort-based problems (Sort List, Merge K Sorted Lists via
  divide & conquer); `O(1)` per operation for LRU Cache once the
  HashMap + doubly linked list is set up.
- **Space:** `O(1)` for pure pointer rewiring (reversal, cycle detection,
  merging in place); `O(n)` when a HashMap is needed to map old nodes to
  new ones (Copy List with Random Pointer) or to track visited nodes.

## Common pitfalls

- **Losing the rest of the list** — overwriting `curr.next` before saving
  it to a temp variable (`nxt = curr.next`) during reversal orphans
  everything after `curr`.
- **Forgetting the dummy node** — without it, removing/inserting at the
  head needs special-case branches instead of falling out of the same
  loop as every other node.
- **Off-by-one on fast/slow start** — whether `slow = fast = head` or
  `slow = head, fast = head.next` changes which node "middle" lands on
  for even-length lists; pick one convention and check it against the
  problem's expected output.
- **`fast.next.next` on a `None`** — the loop guard must check both
  `fast` and `fast.next` before advancing `fast` two steps, or it
  crashes on odd/even length edge cases.
- **Mutating while iterating** — reading `curr.next` *after* rewiring
  `curr.next` gives the new pointer, not the original next node; capture
  what you need before mutating.
- **Cycle checks needing identity, not value equality** — `slow is fast`
  (not `==`), since node values can repeat legitimately.

## Problems in this folder

No solutions yet — see [PROGRESS.md](./PROGRESS.md) for the full problem
queue, difficulty levels, and recommended learning order (fundamentals →
fast/slow pointers → pointer manipulation → multiple lists/HashMap →
sorting → doubly/circular lists).
