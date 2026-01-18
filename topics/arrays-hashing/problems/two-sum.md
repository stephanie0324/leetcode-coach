# Problem: Two Sum

**Company**: Google, Meta, Amazon
**Difficulty**: Easy
**Time Limit**: 15 minutes
**Topic**: Arrays & Hashing
**Pattern**: Complement Search

## Task Description

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

## Examples

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
Explanation: nums[1] + nums[2] == 6, so return [1, 2]
```

**Example 3:**
```
Input: nums = [3,3], target = 6
Output: [0,1]
Explanation: nums[0] + nums[1] == 6
```

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- Only one valid answer exists

## Expected Approach

**Brute Force**: O(n²) time, O(1) space - Check all pairs
**Optimal**: O(n) time, O(n) space - Hash map for complement lookup

**Key Insight**: For each number `x`, check if `target - x` exists in the array.

## Hints

1. **Think about what you need to find**: For each number, you need its complement
2. **What data structure gives fast lookups?**: Hash map/dictionary
3. **How to avoid using same element twice?**: Store index in hash map
4. **When to add to hash map?**: After checking for complement

## Function Signature

```python
def two_sum(nums: List[int], target: int) -> List[int]:
    """
    Find indices of two numbers that add up to target.

    Args:
        nums: List of integers
        target: Target sum

    Returns:
        List containing indices of the two numbers

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # Your solution here
    pass
```

## Test Cases

```python
def test_two_sum():
    # Test case 1: Basic example
    assert two_sum([2,7,11,15], 9) == [0,1]

    # Test case 2: Different order
    assert two_sum([3,2,4], 6) == [1,2]

    # Test case 3: Duplicate numbers
    assert two_sum([3,3], 6) == [0,1]

    # Test case 4: Negative numbers
    assert two_sum([-1,-2,-3,-4,-5], -8) == [2,4]

    # Test case 5: Mixed positive/negative
    assert two_sum([-3,4,3,90], 0) == [0,2]

    print("✅ All test cases passed!")

if __name__ == "__main__":
    test_two_sum()
```

## Related LeetCode Problems

- [1. Two Sum](https://leetcode.com/problems/two-sum/) - Original problem
- [167. Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
- [15. 3Sum](https://leetcode.com/problems/3sum/) - Extension to three numbers
- [18. 4Sum](https://leetcode.com/problems/4sum/) - Extension to four numbers

## Company Interview Notes

- **Google**: Often asks as warm-up, expect follow-up questions about extensions
- **Meta**: May ask to implement multiple approaches and compare trade-offs
- **Amazon**: Focus on handling edge cases and explaining time complexity
- **Microsoft**: Common phone screening question, clear explanation expected

## Follow-up Questions

1. **What if the array is sorted?** → Use two pointers approach
2. **What if we need all pairs that sum to target?** → Modified hash map approach
3. **What if we can't use extra space?** → Two pointers on sorted array
4. **What if there are multiple solutions?** → Return any one or all solutions
5. **How would you extend this to 3Sum?** → Fix one element, apply 2Sum on rest

---

**Practice Goal**: Master the complement search pattern using hash maps. This is a fundamental technique used in many other problems!