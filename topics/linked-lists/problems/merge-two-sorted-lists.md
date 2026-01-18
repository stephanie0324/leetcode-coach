# Problem: Merge Two Sorted Lists

**Company**: Google, Meta, Amazon, Apple
**Difficulty**: Easy
**Time Limit**: 20 minutes
**Topic**: Linked Lists
**Pattern**: Merge Operations

## Task Description

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists in a way that the resulting linked list is also sorted. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

## Examples

**Example 1:**
```
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Visualization:
list1:  1 -> 2 -> 4 -> NULL
list2:  1 -> 3 -> 4 -> NULL
result: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> NULL
```

**Example 2:**
```
Input: list1 = [], list2 = []
Output: []
```

**Example 3:**
```
Input: list1 = [], list2 = [0]
Output: [0]
```

## Visual Step-by-Step

```
Initial state:
list1: [1] -> [2] -> [4] -> NULL
list2: [1] -> [3] -> [4] -> NULL
dummy: [0] -> NULL
current: points to dummy

Step 1: Compare 1 vs 1 (equal, take from list1)
dummy: [0] -> [1] -> NULL
current: points to [1]
list1: [2] -> [4] -> NULL
list2: [1] -> [3] -> [4] -> NULL

Step 2: Compare 2 vs 1 (1 is smaller, take from list2)
dummy: [0] -> [1] -> [1] -> NULL
current: points to second [1]
list1: [2] -> [4] -> NULL
list2: [3] -> [4] -> NULL

... continue until one list is exhausted ...

Final: dummy.next points to the merged list
```

## Constraints

- The number of nodes in both lists is in the range `[0, 50]`
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in **non-decreasing** order

## Expected Approach

**Iterative**: O(n+m) time, O(1) space - Use dummy node and merge pointers
**Recursive**: O(n+m) time, O(n+m) space - Elegant but uses call stack

**Key Insight**: Compare heads of both lists, take the smaller one, advance that pointer.

## Hints

1. **What simplifies edge cases?**: Using a dummy node as starting point
2. **How to choose which node to take?**: Compare values of current heads
3. **What happens when one list ends?**: Attach the remaining list
4. **What do you return?**: dummy.next (skip the dummy node)

## Function Signature

```python
# Definition for singly-linked list node
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Merge two sorted linked lists into one sorted list.

    Args:
        list1: Head of first sorted linked list
        list2: Head of second sorted linked list

    Returns:
        Head of the merged sorted linked list

    Time Complexity: O(n + m) where n, m are lengths of the lists
    Space Complexity: O(1) for iterative approach
    """
    # Your solution here
    pass
```

## Test Cases

```python
def list_to_array(head):
    """Helper function to convert linked list to array for testing"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

def array_to_list(arr):
    """Helper function to create linked list from array"""
    if not arr:
        return None

    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def test_merge_two_lists():
    # Test case 1: Normal merge
    list1 = array_to_list([1, 2, 4])
    list2 = array_to_list([1, 3, 4])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == [1, 1, 2, 3, 4, 4]

    # Test case 2: Both empty
    list1 = array_to_list([])
    list2 = array_to_list([])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == []

    # Test case 3: One empty
    list1 = array_to_list([])
    list2 = array_to_list([0])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == [0]

    # Test case 4: Different lengths
    list1 = array_to_list([1, 3, 5])
    list2 = array_to_list([2, 4, 6, 7, 8])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == [1, 2, 3, 4, 5, 6, 7, 8]

    # Test case 5: No overlap in values
    list1 = array_to_list([1, 2, 3])
    list2 = array_to_list([4, 5, 6])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == [1, 2, 3, 4, 5, 6]

    # Test case 6: Duplicate values
    list1 = array_to_list([1, 1, 1])
    list2 = array_to_list([2, 2, 2])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == [1, 1, 1, 2, 2, 2]

    # Test case 7: Negative numbers
    list1 = array_to_list([-3, -1, 0])
    list2 = array_to_list([-2, 1, 2])
    merged = merge_two_lists(list1, list2)
    assert list_to_array(merged) == [-3, -2, -1, 0, 1, 2]

    print("✅ All test cases passed!")

if __name__ == "__main__":
    test_merge_two_lists()
```

## Approach Analysis

### Iterative Approach with Dummy Node (Recommended)
```python
def merge_two_lists(list1, list2):
    # Create dummy node to simplify edge cases
    dummy = ListNode(0)
    current = dummy

    # While both lists have nodes
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Attach remaining nodes (at most one list is non-empty)
    current.next = list1 or list2

    return dummy.next  # Skip dummy node
```

**Pros:**
- O(1) space complexity
- Clear logic flow
- Handles all edge cases elegantly

**Cons:**
- Requires dummy node (minimal overhead)

### Recursive Approach
```python
def merge_two_lists_recursive(list1, list2):
    # Base cases
    if not list1:
        return list2
    if not list2:
        return list1

    # Recursive case
    if list1.val <= list2.val:
        list1.next = merge_two_lists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = merge_two_lists_recursive(list1, list2.next)
        return list2
```

**Pros:**
- Very clean and elegant
- No dummy node needed
- Natural recursive structure

**Cons:**
- O(n+m) space due to call stack
- May cause stack overflow for very long lists

## Related LeetCode Problems

- [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) - Original problem
- [23. Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) - Extension to k lists
- [88. Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) - Array version
- [148. Sort List](https://leetcode.com/problems/sort-list/) - Uses merge sort on linked list

## Company Interview Notes

- **Google**: May ask for both iterative and recursive solutions
- **Meta**: Focus on discussing space complexity trade-offs
- **Amazon**: Expect follow-up about merging k lists
- **Apple**: Often used as stepping stone to more complex merge problems

## Follow-up Questions

1. **How would you merge k sorted lists?** → Use priority queue or divide-and-conquer
2. **What if lists are not sorted?** → Need different approach, possibly sort first
3. **Can you merge in-place without creating new nodes?** → Yes, just rearrange pointers
4. **What if you want to remove duplicates during merge?** → Add duplicate checking logic
5. **How does this relate to merge sort?** → This is the merge step of merge sort

## Key Patterns to Remember

### Dummy Node Pattern
- **When to use**: Simplifies cases where head might change
- **How**: Create dummy, work with dummy.next, return dummy.next
- **Benefits**: Eliminates special cases for empty lists

### Two-Pointer Merge
- **Compare current elements** of both lists
- **Advance pointer** of the list whose element was chosen
- **Attach remaining** elements when one list is exhausted

### Edge Case Handling
- **Empty lists**: Return the other list
- **Equal values**: Consistent choice (take from first list)
- **Different lengths**: Remaining elements attached at end

---

**Practice Goal**: Master the merge pattern using dummy nodes. This technique is fundamental for many linked list manipulation problems!