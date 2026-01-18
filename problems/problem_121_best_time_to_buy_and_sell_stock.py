"""
LeetCode #121: Best Time to Buy and Sell Stock (Easy)

You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4
"""

def max_profit(prices):
    """
    Your solution here
    """
    max_profit, min_price = 0, float('inf')
    
    for price in prices:
        if price < min_price:
            min_price = price
        else:
            max_profit = max(max_profit, price - min_price)
    return max_profit

# Test cases
def run_tests():
    test_cases = [
        ([7,1,5,3,6,4], 5), ([7,6,4,3,1], 0), ([1,2,3,4,5], 4), ([1], 0)
    ]

    print("🧪 Running test cases...")
    for i, test_case in enumerate(test_cases):
        try:
            if len(test_case) == 3:
                inputs, expected = test_case[:-1], test_case[-1]
                result = max_profit(*inputs)
                status = "✅" if result == expected else "❌"
                print(f"Test {i+1}: {status} {result} (expected: {expected})")
            else:
                print(f"Test {i+1}: ⚠️ Invalid test case format")
        except Exception as e:
            print(f"Test {i+1}: ❌ Error: {e}")

if __name__ == "__main__":
    run_tests()
