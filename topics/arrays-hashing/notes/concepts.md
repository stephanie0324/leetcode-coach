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