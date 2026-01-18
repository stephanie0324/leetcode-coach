# Linked Lists

**Topic Category**: Linear Data Structures
**Prerequisites**: Understanding of pointers/references

## Overview

Linked List problems focus on manipulating nodes connected through pointers. These problems are fundamental for understanding pointer manipulation and form the basis for more complex data structures.

**Key Focus Areas:**
- Pointer manipulation and traversal
- Two-pointer techniques (fast/slow, distance)
- Recursive vs iterative approaches
- In-place modifications

## Essential Patterns

### Node Structure
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Reversal Pattern
```python
def reverse_list(head):
    prev = None
    current = head
    while current:
        next_temp = current.next  # Save next
        current.next = prev       # Reverse pointer
        prev = current           # Move prev forward
        current = next_temp      # Move current forward
    return prev  # New head
```

### Two Pointers (Floyd's Algorithm)
```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
    return slow  # Slow is at middle
```

## Quick Reference

**Basic Traversal:**
```python
current = head
while current:
    # Process current node
    current = current.next
```

**Cycle Detection:**
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # Cycle found
return False
```