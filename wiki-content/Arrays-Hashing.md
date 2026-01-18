# Arrays & Hashing

*Complete guide with problems, concepts, and your progress*

[🏠 Back to Dashboard](Home) | [📊 All Topics](#)



---

## 📊 Your Progress

| Metric | Value |
|--------|--------|
| **Mastery Level** | 0% ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ |
| **Problems Solved** | 2 / 1 |
| **Practice Sessions** | 4 |
| **Last Practiced** | January 18, 2026 |

---

## 📖 Overview & Key Concepts

**Topic Category**: Fundamental Data Structures
**Difficulty Range**: Easy to Hard
**Prerequisites**: Basic programming concepts, iteration

## Overview

Arrays and Hashing problems form the foundation of algorithmic problem solving. These problems typically involve manipulating data stored in arrays or hash tables (dictionaries/maps) to find patterns, solve search problems, or optimize data access.

**Key Focus Areas:**
- Array traversal and manipulation
- Hash table operations for fast lookups
- Two-pointer techniques
- Sliding window patterns
- Prefix sum calculations

## Key Concepts

### 1. Hash Tables (Dictionaries/Maps)
- **O(1) average time** for insert, delete, and lookup
- Perfect for "seen before" or "complement search" problems
- Trade space for time complexity improvements

### 2. Two-Pointer Technique
- **Use when**: Array is sorted or you need to find pairs/triplets
- **Common patterns**: Opposite ends converging, fast/slow pointers
- **Benefit**: Reduces O(n²) brute force to O(n)

### 3. Sliding Window
- **Use when**: Finding subarrays with specific properties
- **Types**: Fixed-size windows, variable-size windows
- **Key insight**: Maintain window properties while sliding

### 4. Prefix Sums
- **Use when**: Need to calculate range sums efficiently
- **Preprocessing**: O(n) time, then O(1) range queries
- **Variations**: 2D prefix sums, difference arrays

## Common Problem Patterns

### 🔍 **Complement Search Pattern**
*"Find two elements that sum to target"*

**When to recognize:**
- Looking for pairs/combinations with specific sum
- "Two Sum", "Two Pointers" problems

**Approach:**
```python
# Hash map approach
seen = {}
for i, num in enumerate(arr):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

**Time**: O(n), **Space**: O(n)

### 📊 **Frequency Counting Pattern**
*"Count occurrences and find patterns"*

**When to recognize:**
- Finding duplicates, most frequent elements
- Anagram detection, character counting

**Approach:**
```python
from collections import Counter
freq = Counter(arr)
# or manually:
freq = {}
for item in arr:
    freq[item] = freq.get(item, 0) + 1
```

### ⬅️➡️ **Two Pointers Pattern**
*"Process array from both ends or with fast/slow pointers"*

**When to recognize:**
- Array is sorted
- Looking for pairs with specific properties
- Palindrome checks

**Approach:**
```python
left, right = 0, len(arr) - 1
while left < right:
    # Process current pair
    if condition_met:
        # Found answer or move both pointers
        left += 1
        right -= 1
    elif need_larger_sum:
        left += 1
    else:
        right -= 1
```

### 🪟 **Sliding Window Pattern**
*"Find optimal subarray with specific properties"*

**When to recognize:**
- "Maximum/minimum subarray"
- "Longest substring with..."
- Fixed or variable window size

**Fixed Window:**
```python
window_sum = sum(arr[:k])  # Initialize
max_sum = window_sum

for i in range(k, len(arr)):
    window_sum = window_sum - arr[i-k] + arr[i]
    max_sum = max(max_sum, window_sum)
```

**Variable Window:**
```python
left = 0
for right in range(len(arr)):
    # Expand window
    add arr[right] to window

    # Contract window while invalid
    while window_invalid():
        remove arr[left] from window
        left += 1

    # Update answer with current window
    update_result()
```

## Approach Strategy

### Step 1: Identify the Pattern
**Ask yourself:**
1. Do I need to find pairs/combinations? → Hash map or Two Pointers
2. Am I counting frequencies? → Hash map with counters
3. Is the array sorted? → Consider Two Pointers
4. Am I looking for subarrays? → Sliding Window or Prefix Sums
5. Do I need range queries? → Prefix Sums

### Step 2: Choose Data Structure
- **Hash Map**: When you need fast lookups, counting, or "seen before" checks
- **Array**: When working with indices, sorted data, or space is critical
- **Two variables**: When tracking simple state (min/max, counts)

### Step 3: Consider Edge Cases
- Empty array: `[]`
- Single element: `[1]`
- All same elements: `[5, 5, 5]`
- Negative numbers: `[-1, -2, 3]`
- Large inputs: Performance considerations

### Step 4: Optimize
- Can you reduce space complexity?
- Is there a mathematical insight to avoid extra passes?
- Can you use sorting to simplify the problem?

## Time & Space Complexity Guide

### Common Patterns:

| Pattern | Time Complexity | Space Complexity | When to Use |
|---------|-----------------|------------------|-------------|
| Hash Map Lookup | O(n) | O(n) | Fast searches, counting |
| Two Pointers | O(n) | O(1) | Sorted arrays, pairs |
| Sliding Window | O(n) | O(1) | Subarrays, optimization |
| Prefix Sums | O(n) + O(1) queries | O(n) | Range sum queries |
| Sorting First | O(n log n) | O(1) | When order matters |

### Optimization Goals:
- **Brute Force**: O(n²) → Look for O(n) solution
- **Multiple Passes**: O(kn) → Try to solve in single pass O(n)
- **Extra Space**: O(n) → See if O(1) space is possible

## Prerequisites

**Must Know Before Starting:**
- ✅ Array indexing and iteration
- ✅ Basic hash table operations (dict in Python)
- ✅ Understanding of time/space complexity

**Helpful Background:**
- Sorting algorithms (for optimization insights)
- Mathematical properties (sum formulas, modular arithmetic)

## Related Topics

**Natural Progressions:**
- **Strings** → Many string problems use array/hashing techniques
- **Two Pointers** → Advanced pointer manipulation
- **Sliding Window** → Dynamic programming foundations

**Advanced Applications:**
- **Dynamic Programming** → State storage and optimization
- **Graph Algorithms** → Adjacency lists, visited sets
- **Backtracking** → State management and pruning

## Quick Reference

### Essential Python Hash Operations:
```python
# Dictionary operations
d = {}
d[key] = value           # O(1) average
value = d[key]           # O(1) average, KeyError if missing
value = d.get(key, 0)    # O(1) average, returns default if missing
if key in d:             # O(1) average membership test
del d[key]               # O(1) average removal

# Counter for frequency counting
from collections import Counter
freq = Counter([1,2,2,3])  # {1: 1, 2: 2, 3: 1}
```

### Array Manipulation Tips:
```python
# Two pointers setup
left, right = 0, len(arr) - 1

# Sliding window setup
window_start = 0
for window_end in range(len(arr)):
    # expand window logic
    pass

# Prefix sum calculation
prefix = [0]
for num in arr:
    prefix.append(prefix[-1] + num)
```

---

## 🚀 Ready to Practice?

**Beginner Path:** Two Sum → Contains Duplicate → Valid Anagram
**Intermediate Path:** Longest Substring → Product of Array → Top K Frequent
**Advanced Path:** Sliding Window Maximum → Subarray Sum Equals K

Use `coach practice arrays-hashing` to start your focused practice session!

# Arrays & Hashing - Key Concepts & Patterns

*Dynamic knowledge base updated from practice sessions*

---

## Hash Map Patterns
*Last Updated: Not yet practiced*

### Complement Search Pattern
**When to Use:**
- Finding pairs that sum to target
- "Two Sum" style problems
- Need to check if specific value exists

**Implementation Template:**
```python
seen = {}
for i, value in enumerate(arr):
    complement = target - value
    if complement in seen:
        return [seen[complement], i]  # Found pair
    seen[value] = i
```

**Problems Practiced:**
- *None yet - start practicing to build this list*

**Key Insights:**
- *Insights will be added from practice sessions*

---

## Two Pointers Pattern
*Last Updated: Not yet practiced*

### Convergent Pointers
**When to Use:**
- Array is sorted
- Looking for pairs with specific sum
- Palindrome checking

**Implementation Template:**
```python
left, right = 0, len(arr) - 1
while left < right:
    current_sum = arr[left] + arr[right]
    if current_sum == target:
        return [left, right]
    elif current_sum < target:
        left += 1
    else:
        right -= 1
```

**Problems Practiced:**
- *None yet*

---

## Sliding Window Pattern
*Last Updated: Not yet practiced*

### Fixed Window
**When to Use:**
- Fixed subarray size problems
- "Maximum sum of k elements"

**Variable Window:**
**When to Use:**
- "Longest substring with..."
- Dynamic subarray problems

**Problems Practiced:**
- *None yet*

---

## Frequency Counting
*Last Updated: Not yet practiced*

### Counter Pattern
**When to Use:**
- Finding duplicates
- Most/least frequent elements
- Anagram detection

**Problems Practiced:**
- *None yet*

---

*This knowledge base will grow and evolve as you practice more problems. Each session will add insights and strengthen your pattern recognition.*

---

## 💡 Problems in This Topic

### Contains Duplicate
Practice problem

### Two Sum
Practice problem


---

## 📝 Your Practice Sessions

# Arrays & Hashing - Practice Session Notes

*Auto-generated practice log. Personal insights and AI feedback from each session.*

### 2026-01-18 - Best Time to Buy and Sell Stock (Easy)
**Time**: Unknown | **Result**: ✅ Solved | **Approach**: Iteration

#### Solution Summary
- Implemented using iteration approach
- Code length: 248 words, 58 lines
- Difficulty: Easy

#### AI Feedback Highlights
- ✅ What's working: The solution correctly implements the one-pass approach, keeping track of the minimum price seen so far and updating the maximum profit. This is an efficient O(n) time complexity solution.
- ⚠️ Could improve: The function lacks type hints for input and return values. Adding these would improve code readability and make it easier to understand the expected input and output types.
- 🚀 Optimization: While the current implementation is already optimal in terms of time complexity, you could consider using a more descriptive variable name instead of `price`. For example, `current_price` would make the code slightly more self-documenting.

#### Personal Reflection
*Using two pointers to solve, may miss the optimal solution in some cases. The right pointer (r) starts from the end and moves left, which can lead to overlooking better buy-sell opportunities earlier in the array.*

#### Related Concepts
- Patterns: iteration
- Topic: Arrays & Hashing

---


### 2026-01-18 - Best Time to Buy and Sell Stock (Easy)
**Time**: Unknown | **Result**: ✅ Solved | **Approach**: Two Pointers, Iteration

#### Solution Summary
- Implemented using two pointers, iteration approach
- Code length: 261 words, 60 lines
- Difficulty: Easy

#### AI Feedback Highlights
- ✅ What's working: The solution correctly uses two pointers (l and r) to traverse the array, which is a good approach for this problem. It also maintains a max_profit variable to keep track of the best profit found so far.
- ⚠️ Could improve: The current implementation may miss the optimal solution in some cases. The right pointer (r) starts from the end and moves left, which can lead to overlooking better buy-sell opportunities earlier in the array.
- 🚀 Optimization: Implement a single-pass solution that moves from left to right, keeping track of the minimum price seen so far and updating the max profit at each step. This approach would be more efficient (O(n) time complexity) and simpler to understand. Here's a sketch of the improved algorithm:

#### Personal Reflection
*Add your thoughts here: What was challenging? What did you learn?*

#### Related Concepts
- Patterns: two_pointers, iteration
- Topic: Arrays & Hashing

---



---

## 🎯 Next Steps

📚 **Keep practicing basics** - Focus on understanding core patterns. You're making progress!

---

*This page updates automatically when you practice problems in this topic*
