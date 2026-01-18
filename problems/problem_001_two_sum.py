"""
LeetCode #1: Two Sum (Easy)

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.
"""


# HINTS:
# 1. Try using a hash map to store numbers you've seen
# 2. For each number, check if (target - number) exists in the map
# 3. Don't forget to handle the case where the same element can't be used twice
def two_sum(nums, target):
    """
    Your solution here
    """
    pass

# Test cases
def run_tests():
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]), ([3, 2, 4], 6, [1, 2]), ([3, 3], 6, [0, 1]), ([-1, -2, -3, -4, -5], -8, [2, 4])
    ]

    print("🧪 Running test cases...")
    for i, test_case in enumerate(test_cases):
        try:
            if len(test_case) == 3:
                inputs, expected = test_case[:-1], test_case[-1]
                result = two_sum(*inputs)
                status = "✅" if result == expected else "❌"
                print(f"Test {i+1}: {status} {result} (expected: {expected})")
            else:
                print(f"Test {i+1}: ⚠️ Invalid test case format")
        except Exception as e:
            print(f"Test {i+1}: ❌ Error: {e}")

if __name__ == "__main__":
    run_tests()
