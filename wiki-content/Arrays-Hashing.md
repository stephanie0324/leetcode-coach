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
**Prerequisites**: Basic programming concepts, iteration

## Overview

Arrays and Hashing problems form the foundation of algorithmic problem solving. These problems typically involve manipulating data stored in arrays or hash tables to find patterns and optimize data access.

**Key Focus Areas:**
- Array traversal and manipulation
- Hash table operations for fast lookups
- Two-pointer techniques
- Sliding window patterns

## Essential Patterns

### Hash Tables (O(1) lookups)
- Perfect for "seen before" or "complement search" problems
- Trade space for time complexity improvements

### Two-Pointer Technique
- Use when array is sorted or finding pairs/triplets
- Reduces O(n²) brute force to O(n)

### Sliding Window
- Finding subarrays with specific properties
- Maintain window properties while sliding

## Quick Reference

**Hash Map Approach:**
```python
seen = {}
for i, num in enumerate(arr):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

**Two Pointers:**
```python
left, right = 0, len(arr) - 1
while left < right:
    if condition_met:
        left += 1
        right -= 1
    elif need_larger:
        left += 1
    else:
        right -= 1
```

---

## 📝 Your Practice Sessions

# Arrays & Hashing - Learning Journal

*Your practice journey with consolidated notes*

## Learning Path
**Beginner Path:** Two Sum → Contains Duplicate → Valid Anagram
**Intermediate Path:** Longest Substring → Product of Array → Top K Frequent
**Advanced Path:** Sliding Window Maximum → Subarray Sum Equals K

---

<details>
<summary><strong>2026-01-18 - Best Time to Buy and Sell Stock</strong> | Time: Unknown | Result: Solved | Approach: Two Pointers, Iteration | Difficulty: Easy</summary>

### AI Feedback Analysis

**What's working well:**
The solution correctly implements the one-pass approach, keeping track of the **minimum price** seen so far and updating the maximum profit. This is an **efficient O(n) time complexity** solution.

**Areas for improvement:**
The current implementation may miss the optimal solution in some cases. The **right pointer (r) starts from the end** and moves left, which can lead to **overlooking better buy-sell opportunities** earlier in the array.

**Optimization opportunities:**
Implement a **single-pass solution** that moves from left to right, keeping track of the minimum price seen so far and updating the max profit at each step. This approach would be more efficient and **simpler to understand**.

### Personal Learning Notes
- Using two pointers to solve, may miss the optimal solution in some cases
- The right pointer (r) starts from the end and moves left, which can lead to overlooking better buy-sell opportunities earlier in the array

</details>

---

<details>
<summary><strong>2026-01-18 - Two Sum</strong> | Time: Unknown | Result: Solved | Approach: Hash Map, Two Pointers, Iteration, Sorting | Difficulty: Easy</summary>

### AI Feedback Analysis

**What's working well:**
Hash map approach provides **efficient O(n) time complexity** for finding the complement.

**Areas for improvement:**
Consider **edge cases** like duplicate values and empty arrays.

**Optimization opportunities:**
The **hash map approach is already optimal** for this problem.

### Personal Learning Notes
- Since I need to return the indices, sorting will create new index
- When sorting is not allowed, hash map is a good way to approach

</details>

---

---

## 🎯 Next Steps

📚 **Keep practicing basics** - Focus on understanding core patterns. You're making progress!

---

*This page updates automatically when you practice problems in this topic*
