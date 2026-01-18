"""
LeetCode #217: Contains Duplicate (Easy)

Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]
Output: true

Example 2:
Input: nums = [1,2,3,4]
Output: false

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""

def contains_duplicate(nums):
    """
    Your solution here
    """
    pass

# Test cases
def run_tests():
    test_cases = [
        ([1,2,3,1], True), ([1,2,3,4], False), ([1,1,1,3,3,4,3,2,4,2], True)
    ]

    print("🧪 Running test cases...")
    for i, test_case in enumerate(test_cases):
        try:
            if len(test_case) == 3:
                inputs, expected = test_case[:-1], test_case[-1]
                result = contains_duplicate(*inputs)
                status = "✅" if result == expected else "❌"
                print(f"Test {i+1}: {status} {result} (expected: {expected})")
            else:
                print(f"Test {i+1}: ⚠️ Invalid test case format")
        except Exception as e:
            print(f"Test {i+1}: ❌ Error: {e}")

if __name__ == "__main__":
    run_tests()
