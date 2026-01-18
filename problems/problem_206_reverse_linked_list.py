"""
LeetCode #206: Reverse Linked List (Easy)

Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []

Constraints:
- The number of nodes in the list is the range [0, 5000].
- -5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?
"""

# Helper classes and functions for linked lists
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list_to_linked(arr):
    """Convert a list to a linked list."""
    if not arr:
        return None

    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def linked_to_list(head):
    """Convert a linked list to a list."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result

def reverse_list(head):
    """

    """
    prev = None  # Initialize prev to None
    while head is not None:
        now = head
        head = head.next
        now.next = prev
        prev = now
    return prev

# Test cases
def run_tests():
    test_cases = [
        (list_to_linked([1,2,3,4,5]), [5,4,3,2,1]),
        (list_to_linked([1,2]), [2,1]),
        (list_to_linked([]), [])
    ]

    print("🧪 Running test cases...")
    for i, (input_list, expected) in enumerate(test_cases):
        try:
            result = reverse_list(input_list)
            result_as_list = linked_to_list(result)
            status = "✅" if result_as_list == expected else "❌"
            print(f"Test {i+1}: {status} {result_as_list} (expected: {expected})")
        except Exception as e:
            print(f"Test {i+1}: ❌ Error: {e}")

if __name__ == "__main__":
    run_tests()
