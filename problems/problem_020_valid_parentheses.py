"""
LeetCode #20: Valid Parentheses (Easy)

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.
"""

def is_valid(s):
    """
    Your solution here
    """
    pass

# Test cases
def run_tests():
    test_cases = [
        ("()", True), ("()[]{}", True), ("(]", False), ("([)]", False), ("{[]}", True)
    ]

    print("🧪 Running test cases...")
    for i, test_case in enumerate(test_cases):
        try:
            if len(test_case) == 3:
                inputs, expected = test_case[:-1], test_case[-1]
                result = is_valid(*inputs)
                status = "✅" if result == expected else "❌"
                print(f"Test {i+1}: {status} {result} (expected: {expected})")
            else:
                print(f"Test {i+1}: ⚠️ Invalid test case format")
        except Exception as e:
            print(f"Test {i+1}: ❌ Error: {e}")

if __name__ == "__main__":
    run_tests()
