# Arrays & Hashing

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