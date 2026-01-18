# Arrays & Hashing - Learning Journal

*Your practice journey with consolidated notes*

---

### 2026-01-18 - Best Time to Buy and Sell Stock
**Time**: Unknown | **Result**: ✅ Solved | **Approach**: Two Pointers, Iteration | **Difficulty**: 🟢 Easy

<details>
<summary><strong>📋 Latest AI Feedback</strong></summary>

- ✅ **What's working:** The solution correctly implements the one-pass approach, keeping track of the minimum price seen so far and updating the maximum profit. This is an efficient O(n) time complexity solution.
- ⚠️ **Could improve:** The current implementation may miss the optimal solution in some cases. The right pointer (r) starts from the end and moves left, which can lead to overlooking better buy-sell opportunities earlier in the array.
- 🚀 **Optimization:** Implement a single-pass solution that moves from left to right, keeping track of the minimum price seen so far and updating the max profit at each step. This approach would be more efficient (O(n) time complexity) and simpler to understand.

</details>

#### Personal Notes
*Using two pointers to solve, may miss the optimal solution in some cases. The right pointer (r) starts from the end and moves left, which can lead to overlooking better buy-sell opportunities earlier in the array.*

---

### 2026-01-18 - Two Sum
**Time**: Unknown | **Result**: ✅ Solved | **Approach**: Hash Map, Two Pointers, Iteration, Sorting | **Difficulty**: 🟢 Easy

<details>
<summary><strong>📋 Latest AI Feedback</strong></summary>

- ✅ **What's working:** Hash map approach provides efficient O(n) time complexity for finding the complement.
- ⚠️ **Could improve:** Consider edge cases like duplicate values and empty arrays.
- 🚀 **Optimization:** The hash map approach is already optimal for this problem.

</details>

#### Personal Notes
*Since I need to return the indices, sorting will create new index, when sorting is not allowed, hash map is a good way to approach*

---