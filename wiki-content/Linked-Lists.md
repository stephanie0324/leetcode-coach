# Linked & Lists

*Complete guide with problems, concepts, and your progress*

[🏠 Back to Dashboard](Home) | [📊 All Topics](#)



---

## 📊 Your Progress

| Metric | Value |
|--------|--------|
| **Mastery Level** | 0% ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ |
| **Problems Solved** | 1 / 1 |
| **Practice Sessions** | 1 |
| **Last Practiced** | January 18, 2026 |

---

## 📖 Overview & Key Concepts

**Topic Category**: Linear Data Structures
**Difficulty Range**: Easy to Hard
**Prerequisites**: Understanding of pointers/references, basic recursion

## Overview

Linked List problems focus on manipulating nodes connected through pointers. Unlike arrays, linked lists offer dynamic size and efficient insertion/deletion, but lack random access. These problems are fundamental for understanding pointer manipulation and form the basis for more complex data structures.

**Key Focus Areas:**
- Pointer manipulation and traversal
- Two-pointer techniques (fast/slow, distance)
- Recursive vs iterative approaches
- In-place modifications
- Cycle detection and handling

## Key Concepts

### 1. Node Structure
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```
- **Value**: Data stored in the node
- **Next**: Reference to the next node (None for tail)
- **Head**: Reference to the first node

### 2. Traversal Patterns
```python
# Basic traversal
current = head
while current:
    # Process current node
    current = current.next

# Traversal with index
current, index = head, 0
while current:
    # Process current node at index
    current = current.next
    index += 1
```

### 3. Two Pointer Techniques
- **Fast/Slow (Tortoise and Hare)**: Detect cycles, find middle
- **Distance Pointers**: Find nth from end, remove nth node
- **Parallel Traversal**: Compare two lists simultaneously

## Common Problem Patterns

### 🔄 **Reversal Pattern**
*"Reverse the order of nodes in a linked list"*

**When to recognize:**
- "Reverse", "backward", "opposite order"
- Need to change direction of pointers

**Iterative Approach:**
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

**Recursive Approach:**
```python
def reverse_list_recursive(head):
    if not head or not head.next:
        return head

    new_head = reverse_list_recursive(head.next)
    head.next.next = head  # Reverse the pointer
    head.next = None       # Break old connection

    return new_head
```

**Time**: O(n), **Space**: O(1) iterative, O(n) recursive

### 🐢🐰 **Two Pointers Pattern**
*"Use fast and slow pointers for efficient traversal"*

**When to recognize:**
- Find middle element
- Detect cycles
- Find nth from end
- Check for palindrome

**Fast/Slow (Floyd's Algorithm):**
```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
    return slow  # Slow is at middle when fast reaches end
```

**Cycle Detection:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:  # Pointers meet
            return True
    return False
```

**Nth from End:**
```python
def find_nth_from_end(head, n):
    first = second = head

    # Move first pointer n steps ahead
    for _ in range(n):
        first = first.next

    # Move both pointers until first reaches end
    while first:
        first = first.next
        second = second.next

    return second  # nth from end
```

### 🔗 **Merge Pattern**
*"Combine two or more sorted linked lists"*

**When to recognize:**
- "Merge sorted lists"
- Combine multiple data streams
- K-way merge problems

**Two List Merge:**
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

### ✂️ **In-Place Modification Pattern**
*"Modify the list structure without extra space"*

**When to recognize:**
- Remove nodes with specific conditions
- Rearrange nodes (odd/even positions)
- Partition lists

**Remove Elements:**
```python
def remove_elements(head, val):
    # Handle removing head nodes
    while head and head.val == val:
        head = head.next

    if not head:
        return head

    current = head
    while current.next:
        if current.next.val == val:
            current.next = current.next.next  # Skip node
        else:
            current = current.next

    return head
```

**Dummy Node Technique:**
```python
def remove_elements_with_dummy(head, val):
    dummy = ListNode(0)
    dummy.next = head
    current = dummy

    while current.next:
        if current.next.val == val:
            current.next = current.next.next
        else:
            current = current.next

    return dummy.next
```

## Approach Strategy

### Step 1: Understand the Structure
**Ask yourself:**
1. Is it a singly or doubly linked list?
2. Do I need to modify in-place or can I create new nodes?
3. Are there any cycles or special properties?
4. What's the expected relationship between input and output?

### Step 2: Choose Your Technique
- **Single Pass**: Simple traversal problems
- **Two Pointers**: Cycle detection, finding middle/nth element
- **Recursion**: Tree-like problems, elegant reversal
- **Dummy Node**: Simplifies edge cases in modifications

### Step 3: Handle Edge Cases
- **Empty list**: `head = None`
- **Single node**: `head.next = None`
- **Two nodes**: Minimum for most two-pointer techniques
- **Cycles**: Infinite loops in traversal

### Step 4: Trace Through Example
- Draw the linked list visually
- Step through your algorithm pointer by pointer
- Verify edge cases work correctly

## Time & Space Complexity Guide

### Common Operations:

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Traversal | O(n) | O(1) | Visit each node once |
| Search | O(n) | O(1) | No random access |
| Insert/Delete at head | O(1) | O(1) | Direct pointer manipulation |
| Insert/Delete at position | O(n) | O(1) | Need traversal to position |
| Reverse (iterative) | O(n) | O(1) | Three pointers |
| Reverse (recursive) | O(n) | O(n) | Call stack space |
| Merge two lists | O(n+m) | O(1) | Compare and link |
| Cycle detection | O(n) | O(1) | Floyd's algorithm |

### Space Optimization Tips:
- **Use iteration over recursion** when possible (O(1) vs O(n) space)
- **Reuse existing nodes** instead of creating new ones
- **Dummy nodes** can simplify logic without significant space cost

## Prerequisites

**Must Know Before Starting:**
- ✅ Understanding of pointers/references
- ✅ Basic iteration and conditionals
- ✅ Concept of null/None values

**Helpful Background:**
- Recursion fundamentals
- Basic understanding of memory allocation
- Familiarity with drawing data structures

## Related Topics

**Natural Progressions:**
- **Stacks & Queues** → Can be implemented with linked lists
- **Trees** → Similar pointer manipulation concepts
- **Graph Traversal** → Generalization of linked list traversal

**Advanced Applications:**
- **Design Problems** → LRU Cache, data structure implementation
- **Dynamic Programming** → Some DP problems use linked structures
- **System Design** → Understanding of memory-efficient data structures

## Common Pitfalls

### 🚨 **Memory Management Issues**
- **Lost References**: Save `next` pointer before modifying `current.next`
- **Null Pointer Dereference**: Always check if node exists before accessing `.next`
- **Memory Leaks**: In languages with manual memory management

### 🚨 **Off-by-One Errors**
- **Loop Conditions**: `while current` vs `while current.next`
- **Pointer Movement**: Moving pointers correct number of times
- **Edge Cases**: Empty list, single node scenarios

### 🚨 **Cycle Handling**
- **Infinite Loops**: Not detecting cycles in traversal
- **Modified Cycles**: Changes made during traversal affecting cycle structure

## Quick Reference

### Essential Operations:
```python
# Check if list is empty
if not head:
    return None

# Traverse list
current = head
while current:
    # Process node
    current = current.next

# Find length
length = 0
current = head
while current:
    length += 1
    current = current.next

# Two pointers setup
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next

# Dummy node pattern
dummy = ListNode(0)
dummy.next = head
current = dummy
# ... modify current.next as needed
return dummy.next
```

### Node Creation:
```python
# Create new node
new_node = ListNode(value)

# Insert after current
new_node.next = current.next
current.next = new_node

# Delete next node
if current.next:
    current.next = current.next.next
```

---

## 🚀 Ready to Practice?

**Beginner Path:** Reverse Linked List → Remove Duplicates → Merge Two Lists
**Intermediate Path:** Remove Nth from End → Cycle Detection → Intersection of Lists
**Advanced Path:** Reverse Nodes in k-Group → Copy List with Random Pointer

Use `coach practice linked-lists` to start your focused practice session!

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

---

## 💡 Problems in This Topic

### Merge Two Sorted Lists
Practice problem

### Reverse Linked List
Practice problem


---

## 📝 Your Practice Sessions

# Linked Lists - Practice Session Notes

*Auto-generated practice log. Personal insights and AI feedback from each session.*

### 2026-01-18 - Reverse Linked List
**Time**: Unknown | **Result**: ✅ Solved | **Approach**: Recursion, Iteration

#### Solution Summary
- Implemented using recursion, iteration approach
- Code length: 251 words, 83 lines

#### AI Feedback Highlights
- 1. ✅ What's correct about this solution:
- 2. ⚠️ Edge cases or issues:
- 3. 🚀 Optimization suggestions:

#### Personal Reflection
*Add your thoughts here: What was challenging? What did you learn?*

#### Related Concepts
- Patterns: recursion, iteration
- Topic: Linked & Lists

---


---

## Session Template
*This template will be used for each practice session*

### [Date] - [Problem Name]
**Time**: X minutes | **Result**: ✅ Solved / ❌ Need Review | **Approach**: [Iterative/Recursive/Two-Pointer]

#### Solution Summary
- Approach used (iterative vs recursive)
- Key pointer manipulation techniques
- Edge cases handled
- Time/space complexity achieved

#### AI Feedback Highlights
- ✅ What worked well in pointer manipulation
- ⚠️ Potential null pointer issues or edge cases missed
- 🚀 More elegant or efficient approaches

#### Personal Reflection
- Which part of pointer manipulation was tricky?
- Did I remember to handle edge cases (empty list, single node)?
- How did I visualize the problem?
- What pattern did this problem follow?

---

## 🎯 Next Steps

📚 **Keep practicing basics** - Focus on understanding core patterns. You're making progress!

---

*This page updates automatically when you practice problems in this topic*
