#!/usr/bin/env python3
import os
import random
import re
import subprocess
import sys
import threading
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
import click
from colorama import init, Fore, Style
import requests
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Initialize colorama and load environment variables
init(autoreset=True)
load_dotenv()
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL")
ANTHROPIC_AUTH_TOKEN = os.getenv("ANTHROPIC_AUTH_TOKEN")

# Interviewer Mode Configuration
TIMER_DEFAULTS = {
    "Easy": 10 * 60,    # 10 minutes in seconds
    "Medium": 30 * 60,  # 30 minutes in seconds
    "Hard": 60 * 60,    # 60 minutes in seconds
}

HELP_LEVELS = {
    "easy": {
        "check_interval": 120,  # Check every 2 minutes
        "hint_threshold": 180,  # Offer hint after 3 minutes
        "encouragement": True,
        "progress_reminders": True,
    },
    "medium": {
        "check_interval": 300,  # Check every 5 minutes
        "hint_threshold": 600,  # Offer hint after 10 minutes
        "encouragement": True,
        "progress_reminders": False,
    },
    "hard": {
        "check_interval": 600,  # Check every 10 minutes
        "hint_threshold": 1200, # Offer hint after 20 minutes
        "encouragement": False,
        "progress_reminders": False,
    }
}

# Global variables for interview state
interview_state = {
    "active": False,
    "problem_file": None,
    "start_time": None,
    "difficulty": None,
    "help_level": "medium",
    "timer_duration": None,
    "last_file_size": 0,
    "last_check_time": None,
    "hints_given": 0,
    "observer": None,
}

# LeetCode problems with descriptions
PROBLEMS = {
    1: {
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": """Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

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
- Only one valid answer exists.""",
        "function_name": "two_sum",
        "signature": "def two_sum(nums, target):",
        "test_cases": [
            "([2, 7, 11, 15], 9, [0, 1])",
            "([3, 2, 4], 6, [1, 2])",
            "([3, 3], 6, [0, 1])",
            "([-1, -2, -3, -4, -5], -8, [2, 4])",
        ]
    },
    20: {
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "description": """Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.""",
        "function_name": "is_valid",
        "signature": "def is_valid(s):",
        "test_cases": [
            '("()", True)',
            '("()[]{}", True)',
            '("(]", False)',
            '("([)]", False)',
            '("{[]}", True)',
        ]
    },
    121: {
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "description": """You are given an array prices where prices[i] is the price of a given stock on the ith day.

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
- 0 <= prices[i] <= 10^4""",
        "function_name": "max_profit",
        "signature": "def max_profit(prices):",
        "test_cases": [
            "([7,1,5,3,6,4], 5)",
            "([7,6,4,3,1], 0)",
            "([1,2,3,4,5], 4)",
            "([1], 0)",
        ]
    },
    206: {
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "description": """Given the head of a singly linked list, reverse the list, and return the reversed list.

Example 1:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Example 2:
Input: head = [1,2]
Output: [2,1]

Example 3:
Input: head = []
Output: []

Constraints:
- The number of nodes in the list is the range [0, 5000].
- -5000 <= Node.val <= 5000

Follow up: A linked list can be reversed either iteratively or recursively. Could you implement both?""",
        "function_name": "reverse_list",
        "signature": "def reverse_list(head):",
        "test_cases": [
            "(list_to_linked([1,2,3,4,5]), [5,4,3,2,1])",
            "(list_to_linked([1,2]), [2,1])",
            "(list_to_linked([]), [])",
        ]
    },
    217: {
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "description": """Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]
Output: true

Example 2:
Input: nums = [1,2,3,4]
Output: false

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9""",
        "function_name": "contains_duplicate",
        "signature": "def contains_duplicate(nums):",
        "test_cases": [
            "([1,2,3,1], True)",
            "([1,2,3,4], False)",
            "([1,1,1,3,3,4,3,2,4,2], True)",
        ]
    }
}

def generate_filename(problem_id, title):
    """Generate a filename from problem ID and title."""
    # Clean title for filename
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
    clean_title = '_'.join(clean_title.lower().split())

    # Ensure problems directory exists
    problems_dir = Path("problems")
    problems_dir.mkdir(exist_ok=True)

    return f"problems/problem_{problem_id:03d}_{clean_title}.py"

def claude_analyze(code, problem_description):
    """Send code to Claude for analysis."""
    if not ANTHROPIC_BASE_URL or not ANTHROPIC_AUTH_TOKEN:
        return "❌ Missing ANTHROPIC_BASE_URL or ANTHROPIC_AUTH_TOKEN in .env file"

    # Construct the full URL - append 'v1/messages' if not already included
    base_url = ANTHROPIC_BASE_URL.rstrip('/')
    if not base_url.endswith('v1/messages'):
        url = f"{base_url}/v1/messages"
    else:
        url = base_url

    headers = {
        "Authorization": f"Bearer {ANTHROPIC_AUTH_TOKEN}",
        "anthropic-version": "2023-12-15",
        "Content-Type": "application/json"
    }

    prompt = f"""Analyze this LeetCode solution as an expert coding interviewer. Provide structured feedback.

PROBLEM:
{problem_description}

SOLUTION:
{code}

Provide EXACTLY this format with specific, actionable feedback:

✅ What's working well:
[One specific thing that's implemented correctly]

⚠️ What could be improved:
[One specific issue with the current implementation - edge case, logic error, or inefficiency]

🚀 Optimization opportunity:
[One specific way to make the code better - performance, readability, or algorithm improvement]

Keep each point concise and actionable. Focus on practical improvements the developer can make.

Be specific and constructive. If the solution is incomplete, guide them on next steps."""

    data = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes

        response_data = response.json()

        # Check if response has the expected structure
        if "content" in response_data and len(response_data["content"]) > 0:
            return response_data["content"][0]["text"]
        else:
            # Handle unexpected response format
            return f"❌ Unexpected API response format: {response_data}"

    except requests.exceptions.RequestException as e:
        return f"❌ Network error getting AI feedback: {e}"
    except KeyError as e:
        return f"❌ API response missing expected field: {e}"
    except Exception as e:
        return f"❌ Error getting AI feedback: {e}"

# Note-taking and Progress Tracking Functions

def detect_problem_topic(filename):
    """Detect which topic a problem belongs to based on filename or content."""
    # Try to detect from new topic-based file structure
    if "topics/" in filename:
        parts = filename.split("/")
        for i, part in enumerate(parts):
            if part == "topics" and i + 1 < len(parts):
                return parts[i + 1]

    # Fallback: map old problem IDs to topics
    problem_topic_map = {
        1: "arrays-hashing",      # Two Sum
        20: "stacks-queues",      # Valid Parentheses
        121: "arrays-hashing",    # Best Time to Buy and Sell Stock
        206: "linked-lists",      # Reverse Linked List
        217: "arrays-hashing"     # Contains Duplicate
    }

    # Extract problem ID from old-style filename
    match = re.search(r'problem_(\d+)', filename)
    if match:
        problem_id = int(match.group(1))
        return problem_topic_map.get(problem_id, "unknown")

    return "unknown"

def load_progress():
    """Load progress data from JSON file."""
    try:
        with open("progress.json", 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default structure if file doesn't exist or is corrupted
        return {"problems": {}, "topics": {}, "session_history": []}

def save_progress(progress_data):
    """Save progress data to JSON file."""
    try:
        with open("progress.json", 'w') as f:
            json.dump(progress_data, f, indent=2)
    except Exception as e:
        click.echo(f"⚠️ Could not save progress: {e}")

def extract_solution_approach(code, ai_feedback):
    """Extract the approach used from code and AI feedback."""
    code_lower = code.lower()
    feedback_lower = ai_feedback.lower()

    # Define approach keywords
    approaches = {
        "hash_map": ["hash", "dict", "set()", "{}"],
        "two_pointers": ["two pointer", "left", "right", "slow", "fast"],
        "sliding_window": ["window", "sliding"],
        "recursion": ["def.*self", "return.*recursive", "recursiv"],
        "iteration": ["while", "for.*in"],
        "sorting": ["sort", "sorted"],
        "binary_search": ["binary", "mid", "left.*right"],
        "dynamic_programming": ["dp", "memo", "cache"],
    }

    detected_approaches = []
    for approach, keywords in approaches.items():
        for keyword in keywords:
            if keyword in code_lower or keyword in feedback_lower:
                detected_approaches.append(approach)
                break

    return detected_approaches or ["unknown"]

def generate_session_notes(filename, code, ai_feedback, problem_data, time_taken=None):
    """Generate and append session notes to the appropriate topic file."""
    topic = detect_problem_topic(filename)
    if topic == "unknown":
        return

    # Extract problem name from filename or problem data
    problem_name = Path(filename).stem.replace("problem_", "").replace("_", " ").title()
    if "title" in problem_data:
        problem_name = problem_data["title"]

    # Extract difficulty level
    difficulty = "Medium"  # Default
    if "difficulty" in problem_data:
        difficulty = problem_data["difficulty"]
    else:
        # Try to detect from file content or filename
        try:
            with open(filename, 'r') as f:
                content = f.read()
            if "(Easy)" in content or "easy" in filename.lower():
                difficulty = "Easy"
            elif "(Hard)" in content or "hard" in filename.lower():
                difficulty = "Hard"
        except:
            pass

    # Get current date and time
    from datetime import datetime
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = time_taken if time_taken else "Unknown"

    # Determine result based on AI feedback
    result = "✅ Solved" if any(word in ai_feedback.lower() for word in ["correct", "good", "works well"]) else "🔄 In Progress"

    # Extract approach
    approaches = extract_solution_approach(code, ai_feedback)
    approach_str = ", ".join(approaches).replace("_", " ").title()

    # Extract structured AI feedback (using new format)
    feedback_lines = ai_feedback.split('\n')
    # Extract structured feedback from new format
    working_well = ""
    improvements = ""
    optimization = ""

    for line in feedback_lines:
        line = line.strip()
        if line.startswith("✅") and "working well:" in line:
            # Get the next line after this header
            idx = feedback_lines.index(line)
            if idx + 1 < len(feedback_lines):
                working_well = feedback_lines[idx + 1].strip()
        elif line.startswith("⚠️") and "could be improved:" in line:
            # Get the next line after this header
            idx = feedback_lines.index(line)
            if idx + 1 < len(feedback_lines):
                improvements = feedback_lines[idx + 1].strip()
        elif line.startswith("🚀") and "Optimization opportunity:" in line:
            # Get the next line after this header
            idx = feedback_lines.index(line)
            if idx + 1 < len(feedback_lines):
                optimization = feedback_lines[idx + 1].strip()

    # Create session entry with difficulty level
    session_entry = f"""
### {date_str} - {problem_name} ({difficulty})
**Time**: {time_str} | **Result**: {result} | **Approach**: {approach_str}

#### Solution Summary
- Implemented using {approach_str.lower()} approach
- Code length: {len(code.split())} words, {len(code.splitlines())} lines
- Difficulty: {difficulty}

#### AI Feedback Highlights
- ✅ What's working: {working_well if working_well else 'Good implementation approach'}
- ⚠️ Could improve: {improvements if improvements else 'Consider edge cases and error handling'}
- 🚀 Optimization: {optimization if optimization else 'Look for opportunities to improve efficiency'}
"""

    session_entry += f"""
#### Personal Reflection
*Add your thoughts here: What was challenging? What did you learn?*

#### Related Concepts
- Patterns: {", ".join(approaches)}
- Topic: {topic.replace('-', ' & ').title()}

---
"""

    # Write to topic's session notes
    notes_file = f"topics/{topic}/notes/session-notes.md"
    try:
        # Read existing content
        try:
            with open(notes_file, 'r') as f:
                existing_content = f.read()
        except FileNotFoundError:
            existing_content = "# Session Notes\n\n*Practice sessions will be logged here*\n"

        # Insert new session after the header
        lines = existing_content.split('\n')
        header_end = 3  # After "# Session Notes" and description

        # Insert new session
        lines.insert(header_end, session_entry)

        with open(notes_file, 'w') as f:
            f.write('\n'.join(lines))

    except Exception as e:
        click.echo(f"⚠️ Could not update session notes: {e}")

def update_progress_tracking(filename, code, ai_feedback, approaches):
    """Update progress.json with session data."""
    progress = load_progress()

    topic = detect_problem_topic(filename)
    problem_key = Path(filename).stem.replace("problem_", "").replace("-", "_")

    # Update session history
    from datetime import datetime
    session_data = {
        "timestamp": datetime.now().isoformat(),
        "problem": problem_key,
        "topic": topic,
        "approaches": approaches,
        "result": "solved" if "✅" in ai_feedback else "attempted"
    }

    if "session_history" not in progress:
        progress["session_history"] = []
    progress["session_history"].append(session_data)

    # Update problem-specific data
    if "problems" not in progress:
        progress["problems"] = {}

    if problem_key not in progress["problems"]:
        progress["problems"][problem_key] = {
            "topic": topic,
            "attempts": 0,
            "solved": False,
            "approaches_tried": []
        }

    problem_progress = progress["problems"][problem_key]
    problem_progress["attempts"] += 1
    problem_progress["last_attempt"] = datetime.now().isoformat()

    # Add new approaches
    for approach in approaches:
        if approach not in problem_progress["approaches_tried"]:
            problem_progress["approaches_tried"].append(approach)

    # Check if solved
    if any(word in ai_feedback.lower() for word in ["correct", "optimal", "well done"]):
        problem_progress["solved"] = True

    # Update topic progress
    if "topics" not in progress:
        progress["topics"] = {}

    if topic not in progress["topics"]:
        progress["topics"][topic] = {
            "problems_attempted": 0,
            "problems_solved": 0,
            "practice_sessions": 0
        }

    topic_progress = progress["topics"][topic]
    topic_progress["practice_sessions"] += 1
    topic_progress["last_practiced"] = datetime.now().isoformat()

    # Count unique problems attempted/solved in this topic
    topic_problems = [p for p, data in progress["problems"].items() if data.get("topic") == topic]
    topic_progress["problems_attempted"] = len(topic_problems)
    topic_progress["problems_solved"] = len([p for p in topic_problems if progress["problems"][p]["solved"]])

    save_progress(progress)

    return progress

# File Watcher for Interview Mode
class CodeFileWatcher(FileSystemEventHandler):
    """Watches for changes in the problem file during interview mode."""

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def on_modified(self, event):
        if not event.is_directory and Path(event.src_path) == self.file_path:
            # Update file size tracking
            try:
                new_size = self.file_path.stat().st_size
                if new_size != interview_state["last_file_size"]:
                    interview_state["last_file_size"] = new_size
                    interview_state["last_check_time"] = time.time()
            except:
                pass

def format_time(seconds):
    """Format seconds into MM:SS format."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def show_progress_notification(elapsed, total, progress_made=False):
    """Show a progress notification to the user."""
    remaining = max(0, total - elapsed)
    elapsed_str = format_time(elapsed)
    remaining_str = format_time(remaining)

    if remaining <= 0:
        click.echo(f"\n{Fore.RED}⏰ TIME'S UP! {elapsed_str} elapsed{Style.RESET_ALL}")
        return True
    elif remaining <= 300:  # 5 minutes warning
        click.echo(f"\n{Fore.YELLOW}⚠️  Only {remaining_str} remaining! ({elapsed_str} elapsed){Style.RESET_ALL}")
    elif progress_made:
        click.echo(f"\n{Fore.GREEN}✍️  Progress detected! {elapsed_str} elapsed, {remaining_str} remaining{Style.RESET_ALL}")
    else:
        click.echo(f"\n{Fore.BLUE}⏰ {elapsed_str} elapsed, {remaining_str} remaining{Style.RESET_ALL}")

    return False

def check_progress_and_offer_help():
    """Check if user needs help and offer assistance."""
    if not interview_state["active"]:
        return

    elapsed = time.time() - interview_state["start_time"]
    help_config = HELP_LEVELS[interview_state["help_level"]]

    # Check if file has been modified recently
    recent_activity = (
        interview_state["last_check_time"] and
        (time.time() - interview_state["last_check_time"]) < 300  # 5 minutes
    )

    # Show time-based notifications
    time_up = show_progress_notification(elapsed, interview_state["timer_duration"], recent_activity)
    if time_up:
        click.echo(f"{Fore.RED}🔔 Interview time completed! Let's review your progress.{Style.RESET_ALL}")
        return

    # Offer help based on elapsed time and activity
    if elapsed > help_config["hint_threshold"] and interview_state["hints_given"] == 0:
        if not recent_activity:
            click.echo(f"\n{Fore.YELLOW}💭 Getting stuck? Would you like a hint?{Style.RESET_ALL}")
            if click.confirm("Would you like me to add some hints to your file?"):
                try:
                    hint_command(interview_state["problem_file"])
                    interview_state["hints_given"] += 1
                except:
                    pass
        else:
            click.echo(f"\n{Fore.GREEN}👍 Good progress! Keep going!{Style.RESET_ALL}")

    # Encouragement based on help level
    if help_config["encouragement"] and recent_activity:
        encouragements = [
            "🚀 You're making progress!",
            "💪 Keep it up!",
            "🎯 You're on the right track!",
            "✨ Looking good so far!"
        ]
        if elapsed > 300 and elapsed % 600 < help_config["check_interval"]:  # Every 10 min after 5 min
            click.echo(f"\n{Fore.GREEN}{random.choice(encouragements)}{Style.RESET_ALL}")

def interview_monitoring_thread():
    """Background thread for monitoring interview progress."""
    while interview_state["active"]:
        try:
            help_config = HELP_LEVELS[interview_state["help_level"]]
            time.sleep(help_config["check_interval"])
            check_progress_and_offer_help()
        except:
            break

def start_interview_mode(problem_file, difficulty):
    """Start interview mode with file watching and timing."""
    problem_path = Path(problem_file)
    if not problem_path.exists():
        click.echo(f"❌ Problem file {problem_file} not found")
        return False

    # Set up interview state
    interview_state.update({
        "active": True,
        "problem_file": str(problem_path),
        "start_time": time.time(),
        "difficulty": difficulty,
        "timer_duration": TIMER_DEFAULTS.get(difficulty, TIMER_DEFAULTS["Medium"]),
        "last_file_size": problem_path.stat().st_size,
        "last_check_time": time.time(),
        "hints_given": 0,
    })

    # Start file watcher
    event_handler = CodeFileWatcher(problem_path)
    observer = Observer()
    observer.schedule(event_handler, str(problem_path.parent), recursive=False)
    observer.start()
    interview_state["observer"] = observer

    # Start monitoring thread
    monitor_thread = threading.Thread(target=interview_monitoring_thread, daemon=True)
    monitor_thread.start()

    # Show interview start message
    duration_str = format_time(interview_state["timer_duration"])
    click.echo(f"\n{Fore.GREEN}🎬 INTERVIEW MODE STARTED{Style.RESET_ALL}")
    click.echo(f"📁 Problem: {problem_file}")
    click.echo(f"⏰ Time limit: {duration_str}")
    click.echo(f"🎯 Difficulty: {difficulty}")
    click.echo(f"🤖 Help level: {interview_state['help_level']}")
    click.echo(f"\n{Fore.YELLOW}💡 I'm watching your progress and will offer help when needed!{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}📝 Start coding in: code {problem_file}{Style.RESET_ALL}")

    return True

def stop_interview_mode():
    """Stop interview mode and cleanup."""
    if interview_state["active"]:
        interview_state["active"] = False
        if interview_state["observer"]:
            interview_state["observer"].stop()
            interview_state["observer"].join()

        elapsed = time.time() - interview_state["start_time"] if interview_state["start_time"] else 0
        click.echo(f"\n{Fore.GREEN}🏁 INTERVIEW MODE ENDED{Style.RESET_ALL}")
        click.echo(f"⏰ Total time: {format_time(elapsed)}")

        # Reset state
        interview_state.update({
            "active": False,
            "problem_file": None,
            "start_time": None,
            "difficulty": None,
            "observer": None,
        })

# Helper function for hint command to work with interview mode
def hint_command(filename):
    """Add hints to the specified file (used by interview mode)."""
    if not Path(filename).exists():
        click.echo(f"❌ File {filename} not found")
        return

    # Extract problem ID
    match = re.search(r'problem_(\d+)', filename)
    if not match:
        click.echo("❌ Invalid filename format")
        return

    problem_id = int(match.group(1))
    if problem_id not in PROBLEMS:
        click.echo(f"❌ Problem {problem_id} not found")
        return

    # Read current file
    with open(filename, 'r') as f:
        content = f.read()

    # Check if hints already exist
    if "# HINTS:" in content:
        click.echo("💡 Hints already added to this file!")
        return

    # Generate hints based on problem
    hints_map = {
        1: [
            "# HINTS:",
            "# 1. Try using a hash map to store numbers you've seen",
            "# 2. For each number, check if (target - number) exists in the map",
            "# 3. Don't forget to handle the case where the same element can't be used twice",
        ],
        20: [
            "# HINTS:",
            "# 1. Stack data structure is perfect for this problem",
            "# 2. Push opening brackets onto the stack",
            "# 3. When you see a closing bracket, check if it matches the top of stack",
            "# 4. Stack should be empty at the end for valid parentheses",
        ],
        121: [
            "# HINTS:",
            "# 1. Track the minimum price seen so far",
            "# 2. For each price, calculate profit if selling today",
            "# 3. Keep track of maximum profit seen so far",
            "# 4. Only one pass through the array needed",
        ],
        206: [
            "# HINTS:",
            "# 1. Think about what reversing means: each node should point to the previous one",
            "# 2. You'll need to track: previous node, current node, next node",
            "# 3. Be careful not to lose the reference to the rest of the list",
            "# 4. The new head will be the original tail",
        ],
        217: [
            "# HINTS:",
            "# 1. A set can help you track seen elements",
            "# 2. If you see an element that's already in your set, return True",
            "# 3. Alternative: sort the array and check adjacent elements",
        ]
    }

    hints = hints_map.get(problem_id, [
        "# HINTS:",
        "# 1. Break down the problem into smaller steps",
        "# 2. Consider edge cases (empty input, single element, etc.)",
        "# 3. Think about time and space complexity",
    ])

    # Insert hints before the function definition
    lines = content.split('\n')
    function_line = -1
    for i, line in enumerate(lines):
        if line.startswith('def '):
            function_line = i
            break

    if function_line != -1:
        # Insert hints before function
        for hint in reversed(hints):
            lines.insert(function_line, hint)
        lines.insert(function_line, "")  # Empty line

        # Write back to file
        with open(filename, 'w') as f:
            f.write('\n'.join(lines))

        click.echo(f"💡 Added hints to {Fore.GREEN}{filename}{Style.RESET_ALL}")
        click.echo("Check your file for helpful guidance!")
    else:
        click.echo("❌ Could not find function definition in file")

@click.group()
def cli():
    """🤖 LeetCode Coach - Simple file-based coding practice"""
    pass

@cli.command()
@click.option('--id', 'problem_id', type=int, help='Specific problem ID to generate')
@click.option('--random', 'use_random', is_flag=True, help='Generate random problem')
def new(problem_id, use_random):
    """Generate a new problem file for coding practice."""

    # Get available problem IDs safely
    available_problem_ids = [1, 20, 121, 206, 217]

    if problem_id and problem_id not in PROBLEMS:
        click.echo(f"❌ Problem {problem_id} not found. Available: {available_problem_ids}")
        return

    if use_random or not problem_id:
        problem_id = random.choice(available_problem_ids)

    problem = PROBLEMS[problem_id]
    filename = generate_filename(problem_id, problem['title'])

    # Check if file already exists
    if Path(filename).exists():
        if not click.confirm(f"File {filename} already exists. Overwrite?"):
            return

    file_content = f'''"""
LeetCode #{problem_id}: {problem['title']} ({problem['difficulty']})

{problem['description']}
"""

{problem['signature']}
    """
    Your solution here
    """
    pass

# Test cases
def run_tests():
    test_cases = [
        {', '.join(problem['test_cases'])}
    ]

    print("🧪 Running test cases...")
    for i, test_case in enumerate(test_cases):
        try:
            if len(test_case) == 3:
                inputs, expected = test_case[:-1], test_case[-1]
                result = {problem['function_name']}(*inputs)
                status = "✅" if result == expected else "❌"
                print(f"Test {{i+1}}: {{status}} {{result}} (expected: {{expected}})")
            else:
                print(f"Test {{i+1}}: ⚠️ Invalid test case format")
        except Exception as e:
            print(f"Test {{i+1}}: ❌ Error: {{e}}")

if __name__ == "__main__":
    run_tests()
'''

    with open(filename, 'w') as f:
        f.write(file_content)

    click.echo(f"✨ Generated: {Fore.GREEN}{filename}{Style.RESET_ALL}")
    click.echo(f"📝 Problem: {problem['title']} ({problem['difficulty']})")
    click.echo(f"🚀 Start coding! Then run: {Fore.CYAN}coach judge {filename}{Style.RESET_ALL}")

@cli.command()
@click.argument('filename')
@click.option('--no-notes', is_flag=True, help='Skip automatic note generation')
def judge(filename, no_notes):
    """Get AI feedback on your solution with automatic note-taking."""

    if not Path(filename).exists():
        click.echo(f"❌ File {filename} not found")
        return

    # Handle both old and new file formats
    problem_data = {}
    problem_desc = ""

    # Try old format first
    match = re.search(r'problem_(\d+)', filename)
    if match:
        problem_id = int(match.group(1))
        if problem_id in PROBLEMS:
            problem_data = PROBLEMS[problem_id]
            problem_desc = f"Problem #{problem_id}: {problem_data['title']}\n{problem_data['description']}"

    # If not old format, try to extract from new topic-based files
    if not problem_desc:
        if "topics/" in filename and filename.endswith('.md'):
            # For new Codility-style markdown problems, extract title from filename
            problem_name = Path(filename).stem.replace('-', ' ').title()
            problem_data = {"title": problem_name}
            problem_desc = f"Problem: {problem_name}"
        else:
            click.echo("❌ Unable to identify problem format. Use old 'coach new' or new topic structure.")
            return

    # Read the solution code
    with open(filename, 'r') as f:
        code = f.read()

    # Check if there's actual solution code (not just template)
    if "pass" in code and len(code.strip().split('\n')) < 10:
        click.echo("⚠️  Looks like you haven't written much code yet. Write your solution first!")
        return

    click.echo(f"🤖 Analyzing your solution...")
    feedback = claude_analyze(code, problem_desc)

    click.echo(f"\n{Fore.BLUE}📋 AI Feedback:{Style.RESET_ALL}")
    click.echo(feedback)

    # Generate automatic notes (unless disabled)
    if not no_notes:
        try:
            click.echo(f"\n{Fore.YELLOW}📝 Updating your learning notes...{Style.RESET_ALL}")

            # Extract solution approaches
            approaches = extract_solution_approach(code, feedback)

            # Generate session notes
            generate_session_notes(filename, code, feedback, problem_data)

            # Update progress tracking
            progress = update_progress_tracking(filename, code, feedback, approaches)

            # Show progress summary
            topic = detect_problem_topic(filename)
            if topic != "unknown" and "topics" in progress:
                topic_stats = progress["topics"].get(topic, {})
                sessions = topic_stats.get("practice_sessions", 0)
                solved = topic_stats.get("problems_solved", 0)
                attempted = topic_stats.get("problems_attempted", 0)

                click.echo(f"✅ Notes updated! {Fore.GREEN}{topic.replace('-', ' & ').title()}{Style.RESET_ALL} progress: {solved}/{attempted} solved, {sessions} sessions")
                click.echo(f"📂 Check: topics/{topic}/notes/session-notes.md")

        except Exception as e:
            click.echo(f"⚠️ Could not update notes: {e}")
    else:
        click.echo(f"\n{Fore.YELLOW}📝 Note-taking skipped (--no-notes flag used){Style.RESET_ALL}")

@cli.command()
@click.argument('filename')
def test(filename):
    """Run test cases for your solution."""

    if not Path(filename).exists():
        click.echo(f"❌ File {filename} not found")
        return

    try:
        click.echo(f"🧪 Running tests for {filename}...")
        result = subprocess.run([sys.executable, filename],
                              capture_output=True, text=True, timeout=10)

        if result.stdout:
            click.echo(result.stdout)
        if result.stderr:
            click.echo(f"{Fore.RED}Errors:{Style.RESET_ALL}")
            click.echo(result.stderr)

    except subprocess.TimeoutExpired:
        click.echo("❌ Test execution timed out (10s limit)")
    except Exception as e:
        click.echo(f"❌ Error running tests: {e}")

@cli.command()
@click.argument('filename')
def hint(filename):
    """Add hints to your solution file."""

    if not Path(filename).exists():
        click.echo(f"❌ File {filename} not found")
        return

    # Extract problem ID
    match = re.search(r'problem_(\d+)', filename)
    if not match:
        click.echo("❌ Invalid filename format")
        return

    problem_id = int(match.group(1))
    if problem_id not in PROBLEMS:
        click.echo(f"❌ Problem {problem_id} not found")
        return

    # Read current file
    with open(filename, 'r') as f:
        content = f.read()

    # Check if hints already exist
    if "# HINTS:" in content:
        click.echo("💡 Hints already added to this file!")
        return

    problem = PROBLEMS[problem_id]

    # Generate hints based on problem
    hints_map = {
        1: [
            "# HINTS:",
            "# 1. Try using a hash map to store numbers you've seen",
            "# 2. For each number, check if (target - number) exists in the map",
            "# 3. Don't forget to handle the case where the same element can't be used twice",
        ],
        20: [
            "# HINTS:",
            "# 1. Stack data structure is perfect for this problem",
            "# 2. Push opening brackets onto the stack",
            "# 3. When you see a closing bracket, check if it matches the top of stack",
            "# 4. Stack should be empty at the end for valid parentheses",
        ],
        121: [
            "# HINTS:",
            "# 1. Track the minimum price seen so far",
            "# 2. For each price, calculate profit if selling today",
            "# 3. Keep track of maximum profit seen so far",
            "# 4. Only one pass through the array needed",
        ],
        206: [
            "# HINTS:",
            "# 1. Think about what reversing means: each node should point to the previous one",
            "# 2. You'll need to track: previous node, current node, next node",
            "# 3. Be careful not to lose the reference to the rest of the list",
            "# 4. The new head will be the original tail",
        ],
        217: [
            "# HINTS:",
            "# 1. A set can help you track seen elements",
            "# 2. If you see an element that's already in your set, return True",
            "# 3. Alternative: sort the array and check adjacent elements",
        ]
    }

    hints = hints_map.get(problem_id, [
        "# HINTS:",
        "# 1. Break down the problem into smaller steps",
        "# 2. Consider edge cases (empty input, single element, etc.)",
        "# 3. Think about time and space complexity",
    ])

    # Insert hints before the function definition
    lines = content.split('\n')
    function_line = -1
    for i, line in enumerate(lines):
        if line.startswith('def '):
            function_line = i
            break

    if function_line != -1:
        # Insert hints before function
        for hint in reversed(hints):
            lines.insert(function_line, hint)
        lines.insert(function_line, "")  # Empty line

        # Write back to file
        with open(filename, 'w') as f:
            f.write('\n'.join(lines))

        click.echo(f"💡 Added hints to {Fore.GREEN}{filename}{Style.RESET_ALL}")
        click.echo("Check your file for helpful guidance!")
    else:
        click.echo("❌ Could not find function definition in file")

@cli.command()
def list():
    """List available problems."""
    click.echo(f"\n{Fore.BLUE}📚 Available Problems:{Style.RESET_ALL}")

    for problem_id, problem in PROBLEMS.items():
        difficulty_color = Fore.GREEN if problem['difficulty'] == 'Easy' else Fore.YELLOW
        click.echo(f"  {problem_id:3d}: {problem['title']} ({difficulty_color}{problem['difficulty']}{Style.RESET_ALL})")

    click.echo(f"\n{Fore.YELLOW}Usage:{Style.RESET_ALL}")
    click.echo("  coach new --id 1        # Generate specific problem")
    click.echo("  coach new --random      # Generate random problem")

# New Topic-Based Learning Commands
@cli.command()
def topics():
    """📚 List available topics and your progress."""
    progress = load_progress()

    click.echo(f"\n{Fore.BLUE}📚 Available Learning Topics:{Style.RESET_ALL}")

    topics_info = {
        "arrays-hashing": {"name": "Arrays & Hashing", "emoji": "🧮"},
        "linked-lists": {"name": "Linked Lists", "emoji": "🔗"},
        "stacks-queues": {"name": "Stacks & Queues", "emoji": "📚"},
        "trees-graphs": {"name": "Trees & Graphs", "emoji": "🌳"},
        "dynamic-programming": {"name": "Dynamic Programming", "emoji": "💫"},
        "sorting-searching": {"name": "Sorting & Searching", "emoji": "🔍"},
        "greedy-algorithms": {"name": "Greedy Algorithms", "emoji": "💰"},
        "backtracking": {"name": "Backtracking", "emoji": "🔙"}
    }

    for topic_key, info in topics_info.items():
        topic_stats = progress.get("topics", {}).get(topic_key, {})
        solved = topic_stats.get("problems_solved", 0)
        attempted = topic_stats.get("problems_attempted", 0)
        sessions = topic_stats.get("practice_sessions", 0)

        # Check if topic directory exists
        topic_path = Path(f"topics/{topic_key}")
        status = "✅" if topic_path.exists() else "🚧"

        # Progress bar
        if attempted > 0:
            progress_pct = (solved / attempted) * 100
            progress_bar = "█" * int(progress_pct // 10) + "░" * (10 - int(progress_pct // 10))
            progress_text = f"[{progress_bar}] {solved}/{attempted} solved ({progress_pct:.0f}%)"
        else:
            progress_text = "Not started yet"

        click.echo(f"  {status} {info['emoji']} {info['name']:<20} {progress_text}")
        if sessions > 0:
            click.echo(f"      └─ {sessions} practice sessions")

    click.echo(f"\n{Fore.YELLOW}💡 Commands:{Style.RESET_ALL}")
    click.echo("  coach practice arrays-hashing    # Start focused practice")
    click.echo("  coach notes arrays-hashing       # View topic notes")
    click.echo("  coach stats                      # Detailed progress")

@cli.command()
@click.argument('topic', required=False)
def practice(topic):
    """🎯 Start focused practice session for a topic."""
    if not topic:
        click.echo("❌ Please specify a topic. Use 'coach topics' to see available topics.")
        return

    topic_path = Path(f"topics/{topic}")
    if not topic_path.exists():
        click.echo(f"❌ Topic '{topic}' not found. Use 'coach topics' to see available topics.")
        return

    problems_path = topic_path / "problems"
    if not problems_path.exists():
        click.echo(f"❌ No problems found for topic '{topic}'")
        return

    # List available problems
    try:
        problem_files = [f for f in problems_path.iterdir() if f.suffix == '.md']
    except OSError:
        problem_files = []
    if not problem_files:
        click.echo(f"❌ No problems found in {problems_path}")
        return

    click.echo(f"\n{Fore.BLUE}🎯 {topic.replace('-', ' & ').title()} Practice Session{Style.RESET_ALL}")
    click.echo(f"📂 Available problems:")

    for i, problem_file in enumerate(problem_files, 1):
        problem_name = problem_file.stem.replace('-', ' ').title()
        click.echo(f"  {i}. {problem_name}")

    click.echo(f"\n{Fore.YELLOW}📝 How to practice:{Style.RESET_ALL}")
    click.echo(f"1. Read the topic guide: {Fore.CYAN}topics/{topic}/README.md{Style.RESET_ALL}")
    click.echo(f"2. Pick a problem and create your solution")
    click.echo(f"3. Use: {Fore.CYAN}coach judge <your-solution-file>{Style.RESET_ALL}")
    click.echo(f"4. Check your notes: {Fore.CYAN}topics/{topic}/notes/session-notes.md{Style.RESET_ALL}")

@cli.command()
@click.argument('topic', required=False)
def notes(topic):
    """📝 View or manage your topic notes."""
    if not topic:
        click.echo("❌ Please specify a topic. Use 'coach topics' to see available topics.")
        return

    topic_path = Path(f"topics/{topic}")
    if not topic_path.exists():
        click.echo(f"❌ Topic '{topic}' not found. Use 'coach topics' to see available topics.")
        return

    notes_path = topic_path / "notes"
    session_notes = notes_path / "session-notes.md"
    concepts_notes = notes_path / "concepts.md"

    topic_name = topic.replace('-', ' & ').title()
    click.echo(f"\n{Fore.BLUE}📝 {topic_name} Notes{Style.RESET_ALL}")

    # Show recent sessions
    if session_notes.exists():
        try:
            with open(session_notes, 'r') as f:
                content = f.read()

            # Extract recent sessions (look for date headers)
            recent_sessions = []
            lines = content.split('\n')
            for line in lines:
                if line.startswith('### 2026-') or line.startswith('### 202'):  # Date headers
                    recent_sessions.append(line.replace('### ', ''))

            if recent_sessions:
                click.echo(f"📅 Recent practice sessions:")
                for session in recent_sessions[-3:]:  # Show last 3
                    click.echo(f"  • {session}")
            else:
                click.echo(f"📅 No practice sessions yet")

        except Exception as e:
            click.echo(f"⚠️ Could not read session notes: {e}")

    # Show available note files
    click.echo(f"\n{Fore.YELLOW}📂 Available notes:{Style.RESET_ALL}")
    if session_notes.exists():
        click.echo(f"  📝 {session_notes} - Your practice sessions")
    if concepts_notes.exists():
        click.echo(f"  🧠 {concepts_notes} - Key concepts and patterns")
    if (topic_path / "README.md").exists():
        click.echo(f"  📖 {topic_path / 'README.md'} - Topic guide")

    click.echo(f"\n{Fore.CYAN}💡 Open in editor: code topics/{topic}/notes/{Style.RESET_ALL}")

@cli.command()
def review():
    """🔄 Show problems due for review (spaced repetition)."""
    progress = load_progress()

    # For now, show basic review suggestions based on recent activity
    click.echo(f"\n{Fore.BLUE}🔄 Review Recommendations{Style.RESET_ALL}")

    session_history = progress.get("session_history", [])
    if not session_history:
        click.echo("📭 No practice history yet. Start with 'coach practice <topic>'!")
        return

    # Group sessions by topic
    from collections import defaultdict
    topic_sessions = defaultdict(list)
    for session in session_history[-10:]:  # Last 10 sessions
        topic_sessions[session.get("topic", "unknown")].append(session)

    for topic, sessions in topic_sessions.items():
        if topic == "unknown":
            continue

        topic_name = topic.replace('-', ' & ').title()
        click.echo(f"\n📚 {topic_name}:")

        # Show problems that were attempted but not solved
        for session in sessions:
            if session.get("result") == "attempted":
                problem = session.get("problem", "Unknown")
                timestamp = session.get("timestamp", "")
                if timestamp:
                    date = timestamp.split('T')[0]
                    click.echo(f"  🔄 {problem.replace('_', ' ').title()} (attempted {date})")

    click.echo(f"\n{Fore.YELLOW}💡 Tip: Focus on problems you attempted but haven't solved yet!{Style.RESET_ALL}")

@cli.command()
def stats():
    """📊 Show comprehensive learning statistics."""
    progress = load_progress()

    click.echo(f"\n{Fore.BLUE}📊 Your Learning Dashboard{Style.RESET_ALL}")

    # Overall stats
    profile = progress.get("profile", {})
    total_sessions = len(progress.get("session_history", []))
    total_problems = len(progress.get("problems", {}))
    solved_problems = len([p for p in progress.get("problems", {}).values() if p.get("solved", False)])

    click.echo(f"\n🎯 {Fore.GREEN}Overall Progress{Style.RESET_ALL}")
    click.echo(f"  • Total practice sessions: {total_sessions}")
    click.echo(f"  • Problems attempted: {total_problems}")
    click.echo(f"  • Problems solved: {solved_problems}")

    if total_problems > 0:
        success_rate = (solved_problems / total_problems) * 100
        click.echo(f"  • Success rate: {success_rate:.1f}%")

    # Topic breakdown
    topics_data = progress.get("topics", {})
    if topics_data:
        click.echo(f"\n📚 {Fore.GREEN}Topic Progress{Style.RESET_ALL}")
        for topic, data in topics_data.items():
            if data.get("practice_sessions", 0) > 0:
                topic_name = topic.replace('-', ' & ').title()
                solved = data.get("problems_solved", 0)
                attempted = data.get("problems_attempted", 0)
                sessions = data.get("practice_sessions", 0)

                if attempted > 0:
                    topic_success = (solved / attempted) * 100
                    click.echo(f"  • {topic_name}: {solved}/{attempted} solved ({topic_success:.0f}%) - {sessions} sessions")

    # Recent activity
    session_history = progress.get("session_history", [])
    if session_history:
        click.echo(f"\n🕐 {Fore.GREEN}Recent Activity{Style.RESET_ALL}")
        for session in session_history[-5:]:  # Last 5 sessions
            timestamp = session.get("timestamp", "")
            problem = session.get("problem", "Unknown")
            result = session.get("result", "unknown")
            topic = session.get("topic", "unknown")

            if timestamp:
                date = timestamp.split('T')[0]
                result_emoji = "✅" if result == "solved" else "🔄"
                click.echo(f"  {result_emoji} {date}: {problem.replace('_', ' ').title()} ({topic.replace('-', ' & ')})")

    click.echo(f"\n{Fore.YELLOW}🚀 Keep up the great work! Use 'coach practice <topic>' to continue learning.{Style.RESET_ALL}")

# Interview Mode CLI Commands
@cli.group()
def interview():
    """🎬 Interview mode with timing and monitoring."""
    pass

@interview.command()
@click.argument('filename')
@click.option('--difficulty', type=click.Choice(['Easy', 'Medium', 'Hard']), default='Medium',
              help='Problem difficulty (affects timer duration)')
@click.option('--help-level', type=click.Choice(['easy', 'medium', 'hard']), default='medium',
              help='How much help to provide (easy=frequent, hard=minimal)')
def start(filename, difficulty, help_level):
    """Start interview mode with file monitoring and timer."""

    # Check if interview is already active
    if interview_state["active"]:
        click.echo(f"❌ Interview mode already active for {interview_state['problem_file']}")
        click.echo("Use 'coach interview stop' to end current session")
        return

    # Check if file exists
    if not Path(filename).exists():
        click.echo(f"❌ File {filename} not found")
        click.echo("Use 'coach new --random' to generate a problem first")
        return

    # Set help level
    interview_state["help_level"] = help_level

    # Start interview mode
    if start_interview_mode(filename, difficulty):
        click.echo(f"\n{Fore.CYAN}🎯 Commands (run in a new terminal):{Style.RESET_ALL}")
        click.echo(f"  coach interview status  # Check progress")
        click.echo(f"  coach interview stop    # End interview")
        click.echo(f"  coach test {filename}   # Run tests")
        click.echo(f"  coach judge {filename}  # Get AI feedback")
        click.echo(f"\n{Fore.YELLOW}📟 Monitoring active... Press Ctrl+C to stop{Style.RESET_ALL}\n")

        # Keep the command running for continuous monitoring
        try:
            while interview_state["active"]:
                time.sleep(1)  # Check every second

                # Check if time is up
                elapsed = time.time() - interview_state["start_time"]
                if elapsed >= interview_state["timer_duration"]:
                    click.echo(f"\n{Fore.RED}⏰ TIME'S UP! Interview session ended.{Style.RESET_ALL}")
                    break

        except KeyboardInterrupt:
            click.echo(f"\n\n{Fore.YELLOW}🛑 Interview monitoring stopped by user{Style.RESET_ALL}")
        finally:
            stop_interview_mode()

@interview.command()
def stop():
    """Stop interview mode."""

    if not interview_state["active"]:
        click.echo("❌ No interview mode currently active")
        return

    stop_interview_mode()
    click.echo(f"{Fore.GREEN}✨ Interview session complete!{Style.RESET_ALL}")
    click.echo("\n💡 Ready to review your solution? Try:")
    click.echo(f"   coach test {interview_state.get('problem_file', '<your-file>')}")
    click.echo(f"   coach judge {interview_state.get('problem_file', '<your-file>')}")

@interview.command()
def status():
    """Show current interview status."""

    if not interview_state["active"]:
        click.echo("❌ No interview mode currently active")
        click.echo("\n🚀 Start a new interview session:")
        click.echo("   coach new --random")
        click.echo("   coach interview start problems/problem_XXX_name.py")
        return

    elapsed = time.time() - interview_state["start_time"]
    remaining = max(0, interview_state["timer_duration"] - elapsed)

    click.echo(f"\n{Fore.GREEN}🎬 INTERVIEW MODE ACTIVE{Style.RESET_ALL}")
    click.echo(f"📁 Problem: {interview_state['problem_file']}")
    click.echo(f"⏰ Elapsed: {format_time(elapsed)}")
    click.echo(f"⏱️  Remaining: {format_time(remaining)}")
    click.echo(f"🎯 Difficulty: {interview_state['difficulty']}")
    click.echo(f"🤖 Help level: {interview_state['help_level']}")
    click.echo(f"💡 Hints given: {interview_state['hints_given']}")

    # Show progress indicator
    progress = min(100, (elapsed / interview_state["timer_duration"]) * 100)
    progress_bar = "█" * int(progress // 5) + "░" * (20 - int(progress // 5))
    click.echo(f"📊 Progress: [{progress_bar}] {progress:.1f}%")

    if remaining <= 0:
        click.echo(f"\n{Fore.RED}⏰ TIME'S UP!{Style.RESET_ALL}")
    elif remaining <= 300:  # 5 minutes warning
        click.echo(f"\n{Fore.YELLOW}⚠️  Only {format_time(remaining)} remaining!{Style.RESET_ALL}")

@interview.command()
@click.argument('filename')
def quick(filename):
    """Quick interview mode - start with optimal settings."""

    # Check if file exists
    if not Path(filename).exists():
        click.echo(f"❌ File {filename} not found")
        click.echo("Use 'coach new --random' to generate a problem first")
        return

    # Detect problem difficulty from filename
    try:
        with open(filename, 'r') as f:
            content = f.read()

        if "(Easy)" in content:
            difficulty = "Easy"
        elif "(Hard)" in content:
            difficulty = "Hard"
        else:
            difficulty = "Medium"
    except:
        difficulty = "Medium"

    # Set help level to medium (as requested in requirements)
    interview_state["help_level"] = "medium"

    if start_interview_mode(filename, difficulty):
        click.echo(f"{Fore.GREEN}⚡ Quick start successful! Good luck!{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}📟 Monitoring active... Press Ctrl+C to stop{Style.RESET_ALL}\n")

        # Keep the command running for continuous monitoring
        try:
            while interview_state["active"]:
                time.sleep(1)  # Check every second

                # Check if time is up
                elapsed = time.time() - interview_state["start_time"]
                if elapsed >= interview_state["timer_duration"]:
                    click.echo(f"\n{Fore.RED}⏰ TIME'S UP! Interview session ended.{Style.RESET_ALL}")
                    break

        except KeyboardInterrupt:
            click.echo(f"\n\n{Fore.YELLOW}🛑 Interview monitoring stopped by user{Style.RESET_ALL}")
        finally:
            stop_interview_mode()

if __name__ == "__main__":
    cli()