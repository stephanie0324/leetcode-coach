# Problem: Reverse Linked List

**Company**: Google, Meta, Amazon, Microsoft
**Difficulty**: Easy
**Time Limit**: 15 minutes
**Topic**: Linked Lists
**Pattern**: Reversal

## Task Description

Given the `head` of a singly linked list, reverse the list, and return the reversed list.

The reversal should be done **in-place** without using extra space for storing the list elements.

## Examples

**Example 1:**
```
Input:  1 -> 2 -> 3 -> 4 -> 5 -> NULL
Output: 5 -> 4 -> 3 -> 2 -> 1 -> NULL
```

**Example 2:**
```
Input:  1 -> 2 -> NULL
Output: 2 -> 1 -> NULL
```

**Example 3:**
```
Input:  1 -> NULL
Output: 1 -> NULL
```

**Example 4:**
```
Input:  NULL
Output: NULL
```

## Visual Representation

```
Before: [1] -> [2] -> [3] -> [4] -> [5] -> NULL

Step-by-step reversal:
Step 1: NULL <- [1]    [2] -> [3] -> [4] -> [5] -> NULL
                ↑       ↑
              prev    current

Step 2: NULL <- [1] <- [2]    [3] -> [4] -> [5] -> NULL
                       ↑       ↑
                     prev    current

... continue until current is NULL

Final:  NULL <- [1] <- [2] <- [3] <- [4] <- [5]
                                              ↑
                                            prev (new head)
```

## Constraints

- The number of nodes in the list is the range `[0, 5000]`
- `-5000 <= Node.val <= 5000`

## Expected Approach

**Iterative**: O(n) time, O(1) space - Three pointers technique
**Recursive**: O(n) time, O(n) space - Function call stack

**Key Insight**: To reverse links, you need to keep track of three pointers: previous, current, and next.

## Hints

1. **What needs to change?**: The direction of the `next` pointers
2. **What do you risk losing?**: The reference to the rest of the list
3. **How many pointers do you need?**: Three - prev, current, next
4. **What's the new head?**: The last node becomes the first node

## Function Signature

```python
# Definition for singly-linked list node
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    """
    Reverse a singly linked list in-place.

    Args:
        head: The head node of the linked list

    Returns:
        The head node of the reversed linked list

    Time Complexity: O(n) where n is the number of nodes
    Space Complexity: O(1) for iterative, O(n) for recursive
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

def test_reverse_list():
    # Test case 1: Normal list
    head1 = array_to_list([1, 2, 3, 4, 5])
    reversed1 = reverse_list(head1)
    assert list_to_array(reversed1) == [5, 4, 3, 2, 1]

    # Test case 2: Two nodes
    head2 = array_to_list([1, 2])
    reversed2 = reverse_list(head2)
    assert list_to_array(reversed2) == [2, 1]

    # Test case 3: Single node
    head3 = array_to_list([1])
    reversed3 = reverse_list(head3)
    assert list_to_array(reversed3) == [1]

    # Test case 4: Empty list
    head4 = array_to_list([])
    reversed4 = reverse_list(head4)
    assert list_to_array(reversed4) == []

    # Test case 5: Negative numbers
    head5 = array_to_list([-1, -2, -3])
    reversed5 = reverse_list(head5)
    assert list_to_array(reversed5) == [-3, -2, -1]

    print("✅ All test cases passed!")

if __name__ == "__main__":
    test_reverse_list()
```

## Approach Analysis

### Iterative Approach (Recommended)
**Pros:**
- O(1) space complexity
- Easier to understand and debug
- No risk of stack overflow

**Cons:**
- Requires careful pointer manipulation

### Recursive Approach
**Pros:**
- Clean, elegant code
- Good for understanding recursion

**Cons:**
- O(n) space due to call stack
- Can cause stack overflow for large lists

## Related LeetCode Problems

- [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) - Original problem
- [92. Reverse Linked List II](https://leetcode.com/problems/reverse-linked-list-ii/) - Reverse portion of list
- [25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) - Reverse in groups
- [24. Swap Nodes in Pairs](https://leetcode.com/problems/swap-nodes-in-pairs/) - Swap adjacent nodes

## Company Interview Notes

- **Google**: May ask for both iterative and recursive solutions
- **Meta**: Expect follow-up about reversing in groups or portions
- **Amazon**: Focus on handling edge cases and explaining pointer movements
- **Microsoft**: Common for demonstrating pointer manipulation skills

## Follow-up Questions

1. **Can you solve it recursively?** → Use recursion to reach end, then reverse on way back
2. **What if you only reverse nodes at even positions?** → Selective reversal with tracking
3. **How would you reverse nodes in groups of k?** → Extend reversal to work on k-node segments
4. **Can you reverse without changing node values?** → Yes, change pointers only
5. **What if the list has cycles?** → Need cycle detection first

## Common Mistakes

- **Losing reference to remaining list**: Always save `next` before changing `current.next`
- **Wrong return value**: Return `prev`, not `current` (which will be NULL)
- **Not handling empty list**: Check if `head` is None
- **Off-by-one errors**: Make sure loop condition is correct

---

**Practice Goal**: Master the three-pointer technique for linked list reversal. This pattern appears in many advanced linked list problems!