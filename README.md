# LeetCode Coach CLI

<div align="center">

🤖 **Simple file-based LeetCode practice with AI feedback**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![UV](https://img.shields.io/badge/uv-package%20manager-green)](https://github.com/astral-sh/uv)

Generate Python files for LeetCode problems, code in your favorite editor, get instant AI feedback from Claude!

</div>

## ⚡ Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/leetcode-coach.git
cd leetcode-coach
```

2. **Install dependencies**:
```bash
uv sync
```

3. **Setup Claude AI (optional but recommended)**:
```bash
cp .env.example .env
# Edit .env and add your Claude API key
# Get your key from: https://console.anthropic.com
```

4. **Start coding**:
```bash
uv run coach new --random
```

## 🚀 Workflow

```bash
# 1. Generate a new problem file
uv run coach new --random
# ✨ Creates: problems/problem_001_two_sum.py

# 2. Code your solution in VS Code/vim/any editor
code problems/problem_001_two_sum.py

# 3. Test your solution
uv run coach test problems/problem_001_two_sum.py

# 4. Get AI feedback (requires Claude API key)
uv run coach judge problems/problem_001_two_sum.py

# 5. Need hints?
uv run coach hint problems/problem_001_two_sum.py
```

## 📁 Project Structure

When you generate problems, they'll be organized in the `problems/` directory:

```
leetcode-coach/
├── problems/                 # Your generated problem files go here
│   ├── problem_001_two_sum.py
│   ├── problem_020_valid_parentheses.py
│   └── ...
├── examples/                 # Sample files for reference
│   └── problem_001_two_sum.py
├── coach.py                  # Main application
└── README.md
```

## 📝 Example Generated File

Check out [`examples/problem_001_two_sum.py`](examples/problem_001_two_sum.py) to see what a generated file looks like!

```python
"""
LeetCode #1: Two Sum (Easy)

Given an array of integers nums and an integer target,
return indices of the two numbers that add up to target.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
"""

def two_sum(nums, target):
    """
    Your solution here
    """
    pass

# Test cases and runner automatically included
```

## 🎯 Commands

| Command | Description |
|---------|-------------|
| `coach list` | Show available problems |
| `coach new --id 1` | Generate specific problem |
| `coach new --random` | Generate random problem |
| `coach test <file>` | Run test cases |
| `coach judge <file>` | Get AI feedback on your solution |
| `coach hint <file>` | Add helpful hints to your file |

## 📚 Available Problems

Currently includes 5 curated LeetCode problems:

- **#1** Two Sum (Easy)
- **#20** Valid Parentheses (Easy)
- **#121** Best Time to Buy and Sell Stock (Easy)
- **#206** Reverse Linked List (Easy)
- **#217** Contains Duplicate (Easy)

Perfect for getting started with coding interviews!

## ✨ Features

- 🎯 **Real LeetCode Problems**: Curated set with detailed descriptions and examples
- 🤖 **AI Code Review**: Claude analyzes your solutions for bugs, edge cases, and optimizations
- 💡 **Smart Hints**: Context-aware hints added directly to your files
- 🧪 **Built-in Tests**: Automatic test cases for each problem
- 📁 **File-based**: Work directly in your favorite editor
- 🎨 **Beautiful CLI**: Colored output and clean interface
- ⚡ **Zero Database**: No setup required, just pure Python files

## 🛠️ Development

Want to add more problems? Edit the `PROBLEMS` dictionary in `coach.py`:

```python
PROBLEMS = {
    42: {
        "title": "Your Problem Title",
        "difficulty": "Medium",
        "description": "Problem description...",
        "function_name": "your_function",
        "signature": "def your_function(params):",
        "test_cases": ["(input, expected)"]
    }
}
```

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request. Areas for improvement:

- Add more LeetCode problems
- Improve AI feedback prompts
- Add different difficulty levels
- Better test case formatting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LeetCode](https://leetcode.com) for the problems
- [Anthropic](https://www.anthropic.com) for Claude AI
- [uv](https://github.com/astral-sh/uv) for fast Python package management

---

<div align="center">

**Happy Coding!** 🚀

Star ⭐ this repo if you find it helpful!

</div>