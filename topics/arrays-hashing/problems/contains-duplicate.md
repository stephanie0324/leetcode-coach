# Problem: Contains Duplicate

**Company**: Meta, Amazon, Microsoft
**Difficulty**: Easy
**Time Limit**: 10 minutes
**Topic**: Arrays & Hashing
**Pattern**: Frequency Counting

## Task Description

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

This is a classic problem for demonstrating the trade-off between time and space complexity using different approaches.

## Examples

**Example 1:**
```
Input: nums = [1,2,3,1]
Output: true
Explanation: The element 1 appears at index 0 and 3.
```

**Example 2:**
```
Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct.
```

**Example 3:**
```
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
Explanation: Multiple elements appear more than once.
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Expected Approaches

### Approach 1: Hash Set (Optimal)
**Time**: O(n), **Space**: O(n)
**Key Insight**: Use a set to track seen elements

### Approach 2: Sorting
**Time**: O(n log n), **Space**: O(1)
**Key Insight**: Sort first, then check adjacent elements

### Approach 3: Brute Force
**Time**: O(n²), **Space**: O(1)
**Key Insight**: Check every pair - not recommended for large inputs

## Hints

1. **What do you need to remember?**: Elements you've already seen
2. **What data structure is perfect for membership testing?**: Hash set
3. **Alternative approach**: What if you sort the array first?
4. **Space vs Time**: Can you solve with O(1) space but worse time complexity?

## Function Signature

```python
def contains_duplicate(nums: List[int]) -> bool:
    """
    Check if array contains any duplicate values.

    Args:
        nums: List of integers to check

    Returns:
        True if any duplicates exist, False otherwise

    Time Complexity: O(n) with hash set
    Space Complexity: O(n) with hash set
    """
    # Your solution here
    pass
```

## Test Cases

```python
def test_contains_duplicate():
    # Test case 1: Has duplicates
    assert contains_duplicate([1,2,3,1]) == True

    # Test case 2: All distinct
    assert contains_duplicate([1,2,3,4]) == False

    # Test case 3: Multiple duplicates
    assert contains_duplicate([1,1,1,3,3,4,3,2,4,2]) == True

    # Test case 4: Single element (no duplicates possible)
    assert contains_duplicate([1]) == False

    # Test case 5: Two identical elements
    assert contains_duplicate([1,1]) == True

    # Test case 6: Negative numbers
    assert contains_duplicate([-1,-2,-3,-4,-1]) == True

    # Test case 7: Large numbers
    assert contains_duplicate([1000000000, 999999999, 1000000000]) == True

    # Test case 8: Empty constraint (minimum 1 element, so skip)

    print("✅ All test cases passed!")

if __name__ == "__main__":
    test_contains_duplicate()
```

## Approach Comparison

### Hash Set Solution (Recommended)
```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Or more Pythonic:
def contains_duplicate_pythonic(nums):
    return len(nums) != len(set(nums))
```

**Pros:** Fast O(n) time complexity
**Cons:** Uses O(n) extra space

### Sorting Solution
```python
def contains_duplicate_sort(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True
    return False
```

**Pros:** O(1) space if in-place sorting allowed
**Cons:** Slower O(n log n) time, modifies input array

### Brute Force (Not Recommended)
```python
def contains_duplicate_brute(nums):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
```

**Pros:** O(1) space, simple to understand
**Cons:** Very slow O(n²) time complexity

## Related LeetCode Problems

- [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) - Original problem
- [219. Contains Duplicate II](https://leetcode.com/problems/contains-duplicate-ii/) - Within k distance
- [220. Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/) - Value difference constraint
- [242. Valid Anagram](https://leetcode.com/problems/valid-anagram/) - Similar frequency counting

## Company Interview Notes

- **Meta**: May ask you to implement multiple approaches and discuss trade-offs
- **Amazon**: Focus on explaining time/space complexity differences
- **Microsoft**: Often combined with follow-up questions about constraints
- **Google**: May ask for the most memory-efficient solution

## Follow-up Questions

1. **What if you can't use extra space?** → Use sorting approach
2. **What if duplicates must be within k distance?** → Sliding window with set
3. **What if you need to return the duplicate value?** → Modify to return the value
4. **How would you handle very large arrays?** → External sorting, streaming algorithms
5. **What if the array is already sorted?** → Simple adjacent comparison

## Key Learning Points

### Pattern Recognition
- **"Find duplicates"** → Think hash set or frequency counting
- **"Any duplicates exist"** → Boolean return, early termination possible
- **Trade-offs** → Time vs Space complexity decisions

### Implementation Tips
- **Early return** when duplicate found (don't need to check all)
- **Set operations** are generally O(1) average case
- **Sorting approach** useful when space is constrained

### Common Variations
- Find the duplicate value (not just boolean)
- Count number of duplicates
- Find all duplicate values
- Remove duplicates from array

---

**Practice Goal**: Master the hash set pattern for duplicate detection. This is fundamental for many frequency-based problems!