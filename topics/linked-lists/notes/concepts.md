# Linked Lists - Key Concepts & Patterns

*Dynamic knowledge base updated from practice sessions*

---

## Reversal Pattern
*Last Updated: Not yet practiced*

### Iterative Reversal
**When to Use:**
- Need to reverse entire list or portion of list
- Prefer O(1) space complexity

**Three-Pointer Technique:**
```python
def reverse_list(head):
    prev = None
    current = head

    while current:
        next_temp = current.next  # Save next
        current.next = prev       # Reverse pointer
        prev = current           # Move prev forward
        current = next_temp      # Move current forward

    return prev  # prev is new head
```

**Key Points:**
- Always save the next pointer before breaking the link
- prev becomes the new head after traversal
- Handle empty list (return None) and single node (return head) cases

**Problems Practiced:**
- *None yet - start practicing to build this list*

**Common Mistakes to Watch:**
- *Insights will be added from practice sessions*

---

## Two Pointers Pattern
*Last Updated: Not yet practiced*

### Fast/Slow Pointers (Floyd's Algorithm)
**When to Use:**
- Find middle of linked list
- Detect cycles
- Find nth node from end (with some modification)

**Standard Implementation:**
```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
    return slow  # slow points to middle
```

**Cycle Detection:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Problems Practiced:**
- *None yet*

**Key Insights:**
- *Insights will be added from practice sessions*

---

## Distance Pointers Pattern
*Last Updated: Not yet practiced*

### N-Distance Technique
**When to Use:**
- Find nth node from end
- Remove nth node from end
- Check if two pointers are at specific distance

**Implementation:**
```python
def find_nth_from_end(head, n):
    first = second = head

    # Move first pointer n steps ahead
    for _ in range(n):
        if not first:  # List shorter than n
            return None
        first = first.next

    # Move both until first reaches end
    while first:
        first = first.next
        second = second.next

    return second
```

**Problems Practiced:**
- *None yet*

---

## Merge Pattern
*Last Updated: Not yet practiced*

### Two-List Merge
**When to Use:**
- Merge two sorted linked lists
- Combine multiple data streams
- Part of divide-and-conquer algorithms

**Implementation:**
```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Attach remaining nodes
    current.next = l1 or l2
    return dummy.next
```

**Problems Practiced:**
- *None yet*

---

## In-Place Modification
*Last Updated: Not yet practiced*

### Dummy Node Technique
**When to Use:**
- Removing nodes based on value
- Modifying list structure
- Simplifying edge case handling

**Why Use Dummy Node:**
- Handles edge case where head node needs to be removed
- Provides consistent starting point for traversal
- Simplifies pointer manipulation logic

**Template:**
```python
def modify_list(head):
    dummy = ListNode(0)
    dummy.next = head
    current = dummy

    while current.next:
        if condition_to_modify:
            current.next = current.next.next  # Remove/skip
        else:
            current = current.next

    return dummy.next
```

**Problems Practiced:**
- *None yet*

---

## Common Edge Cases Checklist

### Always Check:
- [ ] Empty list (head is None)
- [ ] Single node list
- [ ] Two node list (minimum for many algorithms)
- [ ] All nodes have same value
- [ ] List with cycle (if applicable)

### Pointer Safety:
- [ ] Check if node exists before accessing .next
- [ ] Save next pointer before modifying current.next
- [ ] Proper null termination (last node.next = None)

### Return Value:
- [ ] Return correct head (may change after operations)
- [ ] Handle when entire list is removed
- [ ] Verify modified list structure

---

*This knowledge base will grow and evolve as you practice more linked list problems. Each session will add insights and strengthen your pointer manipulation skills.*