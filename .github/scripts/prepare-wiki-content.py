#!/usr/bin/env python3
"""
Prepare LeetCode Coach content for GitHub Wiki synchronization - SIMPLIFIED STRUCTURE.

This script transforms the structured learning content into a clean, user-friendly wiki:
- Home dashboard with overview
- One consolidated page per topic (not scattered files)
- Problems, concepts, and progress all in one place per topic
- Easy navigation and reduced information overload
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import re


class WikiContentProcessor:
    def __init__(self, source_dir=".", target_dir="wiki-content"):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.progress_data = self.load_progress()

    def load_progress(self):
        """Load progress.json for learning analytics."""
        try:
            with open(self.source_dir / "progress.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def clean_target_directory(self):
        """Clean and create fresh wiki content directory."""
        if self.target_dir.exists():
            shutil.rmtree(self.target_dir)
        self.target_dir.mkdir(parents=True)

    def create_home_dashboard(self):
        """Create a clean, focused learning dashboard."""
        dashboard_content = f"""# 🎯 LeetCode Coach - Learning Dashboard

*Your personal coding interview preparation wiki*

**Last Updated:** {datetime.now().strftime("%B %d, %Y")}

---

## 📊 Your Progress

{self.format_overall_progress()}

---

## 📚 Learning Topics

{self.format_topics_overview()}

---

## 🚀 Quick Start

1. **Pick a topic** from the list above
2. **Click the topic** to see overview, problems, and your progress
3. **Practice with CLI:** `coach practice <topic>`
4. **Get feedback:** `coach judge <problem-file>`
5. **Watch your progress** update automatically!

---

*This dashboard updates automatically when you practice problems*
"""

        with open(self.target_dir / "Home.md", 'w') as f:
            f.write(dashboard_content)

        print("✅ Created dashboard: Home.md")

    def create_consolidated_topic_page(self, topic_name):
        """Create ONE comprehensive page per topic with everything."""
        topic_path = self.source_dir / "topics" / topic_name
        if not topic_path.exists():
            return

        print(f"📁 Processing topic: {topic_name}")

        # Read all content for this topic
        overview_content = self.get_topic_overview(topic_path)
        concepts_content = self.get_topic_concepts(topic_path)
        session_notes = self.get_session_notes(topic_path)
        problems_content = self.get_problems_content(topic_path)
        progress_stats = self.get_topic_stats(topic_name)

        # Build consolidated page
        topic_display = topic_name.replace('-', ' & ').title()

        consolidated_content = f"""# {topic_display}

*Complete guide with problems, concepts, and your progress*

{self.create_topic_navigation()}

---

## 📊 Your Progress

{self.format_topic_progress(topic_name, progress_stats)}

---

## 📖 Overview & Key Concepts

{overview_content}

{concepts_content}

---

## 💡 Problems in This Topic

{problems_content}

---

## 📝 Your Practice Sessions

{session_notes}

---

## 🎯 Next Steps

{self.generate_topic_recommendations(topic_name, progress_stats)}

---

*This page updates automatically when you practice problems in this topic*
"""

        # Save consolidated topic page
        safe_name = self.wiki_safe_filename(topic_display)
        topic_file = self.target_dir / f"{safe_name}.md"

        with open(topic_file, 'w') as f:
            f.write(consolidated_content)

        print(f"✅ Created topic page: {topic_file.name}")

    def create_topic_navigation(self):
        """Create simple navigation back to dashboard."""
        return """[🏠 Back to Dashboard](Home) | [📊 All Topics](#)

"""

    def get_topic_overview(self, topic_path):
        """Extract overview content from topic README."""
        readme_path = topic_path / "README.md"
        if not readme_path.exists():
            return "*No overview available yet.*"

        with open(readme_path, 'r') as f:
            content = f.read()

        # Remove the title (first line) since we'll have our own
        lines = content.split('\n')
        if lines and lines[0].startswith('# '):
            content = '\n'.join(lines[1:])

        return content.strip()

    def get_topic_concepts(self, topic_path):
        """Extract key concepts, but streamlined."""
        concepts_path = topic_path / "notes" / "concepts.md"
        if not concepts_path.exists():
            return ""

        with open(concepts_path, 'r') as f:
            content = f.read()

        # Take only the first few key patterns, not the entire file
        lines = content.split('\n')
        result_lines = []
        pattern_count = 0

        for line in lines:
            if line.startswith('## ') and 'Pattern' in line:
                pattern_count += 1
                if pattern_count > 3:  # Only show first 3 patterns
                    break
            result_lines.append(line)

        return '\n'.join(result_lines[:100])  # Limit length

    def get_session_notes(self, topic_path):
        """Get recent practice sessions."""
        sessions_path = topic_path / "notes" / "session-notes.md"
        if not sessions_path.exists():
            return "*No practice sessions yet. Use `coach judge <problem-file>` to start!*"

        with open(sessions_path, 'r') as f:
            content = f.read()

        # Extract only recent sessions (first few entries)
        lines = content.split('\n')
        session_lines = []
        session_count = 0

        for line in lines:
            if line.startswith('### ') and any(month in line for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
                session_count += 1
                if session_count > 5:  # Only show 5 most recent sessions
                    break
            session_lines.append(line)

        if not session_lines:
            return "*No practice sessions yet. Use `coach judge <problem-file>` to start!*"

        return '\n'.join(session_lines[:50])  # Limit to ~50 lines

    def get_problems_content(self, topic_path):
        """Create a clean problems section."""
        problems_path = topic_path / "problems"
        if not problems_path.exists():
            return "*No problems available yet.*"

        problems_list = []
        for problem_file in problems_path.glob("*.md"):
            problem_name = problem_file.stem.replace('-', ' ').title()

            # Read first few lines to get description
            with open(problem_file, 'r') as f:
                content = f.read()

            lines = content.split('\n')
            description = "Practice problem"
            for line in lines[:10]:
                if line.strip() and not line.startswith('#') and not line.startswith('*') and len(line.strip()) > 20:
                    description = line.strip()[:100] + "..."
                    break

            problems_list.append(f"### {problem_name}\n{description}\n")

        if not problems_list:
            return "*No problems available yet.*"

        return '\n'.join(problems_list)

    def wiki_safe_filename(self, name):
        """Convert filename to wiki-safe format."""
        name = re.sub(r'[^a-zA-Z0-9-_\s]', '', name)
        name = name.replace(' ', '-').replace('_', '-')
        return re.sub(r'-+', '-', name).strip('-')

    def format_overall_progress(self):
        """Format overall learning statistics."""
        profile = self.progress_data.get("profile", {})

        total_attempted = profile.get("total_problems_attempted", 0)
        solved = profile.get("total_problems_solved", 0)
        sessions = profile.get("total_sessions", 0)
        streak = profile.get("current_streak", 0)

        return f"""| Metric | Value |
|--------|--------|
| **Problems Attempted** | {total_attempted} |
| **Problems Solved** | {solved} |
| **Practice Sessions** | {sessions} |
| **Current Streak** | {streak} days |"""

    def format_topics_overview(self):
        """Create clean topics overview with progress."""
        topics = self.progress_data.get("topics", {})

        if not topics:
            return """| Topic | Status |
|-------|--------|
| **[Arrays & Hashing](Arrays-Hashing)** | Ready to start! |
| **[Linked Lists](Linked-Lists)** | Ready to start! |
| **[Dynamic Programming](Dynamic-Programming)** | Unlock by practicing basics |

*Click any topic above to see detailed guides and problems*"""

        topic_rows = []
        for topic_name, stats in topics.items():
            topic_display = topic_name.replace('-', ' & ').title()
            topic_link = self.wiki_safe_filename(topic_display)

            solved = stats.get("problems_solved", 0)
            total = stats.get("total_problems", 0)
            mastery = stats.get("mastery_level", 0) * 100

            if solved == 0:
                status = "Ready to start!"
            elif mastery < 50:
                status = f"In progress ({solved}/{total} solved)"
            else:
                status = f"Great progress! ({solved}/{total} solved)"

            topic_rows.append(f"| **[{topic_display}]({topic_link})** | {status} |")

        header = """| Topic | Status |
|-------|--------|"""

        return header + "\n" + "\n".join(topic_rows)

    def format_topic_progress(self, topic_name, stats):
        """Format progress for individual topic page."""
        mastery = stats.get("mastery_level", 0) * 100
        solved = stats.get("problems_solved", 0)
        total = stats.get("total_problems", 0)
        sessions = stats.get("practice_sessions", 0)

        last_practiced = stats.get("last_practiced")
        if last_practiced:
            try:
                last_date = datetime.fromisoformat(last_practiced.replace('Z', '+00:00'))
                last_practiced_str = last_date.strftime("%B %d, %Y")
            except:
                last_practiced_str = "Recently"
        else:
            last_practiced_str = "Not yet practiced"

        progress_bar = self.create_progress_bar(mastery)

        return f"""| Metric | Value |
|--------|--------|
| **Mastery Level** | {mastery:.0f}% {progress_bar} |
| **Problems Solved** | {solved} / {total} |
| **Practice Sessions** | {sessions} |
| **Last Practiced** | {last_practiced_str} |"""

    def create_progress_bar(self, percentage):
        """Create visual progress bar."""
        filled = int(percentage / 10)
        empty = 10 - filled
        return "🟩" * filled + "⬜" * empty

    def get_topic_stats(self, topic_name):
        """Extract statistics for a topic."""
        topics = self.progress_data.get("topics", {})
        return topics.get(topic_name, {})

    def generate_topic_recommendations(self, topic_name, stats):
        """Generate personalized recommendations for the topic."""
        mastery = stats.get("mastery_level", 0) * 100
        solved = stats.get("problems_solved", 0)

        if solved == 0:
            return "🎯 **Start practicing!** Use `coach practice " + topic_name + "` to begin with your first problem."
        elif mastery < 30:
            return f"📚 **Keep practicing basics** - Focus on understanding core patterns. You're making progress!"
        elif mastery < 70:
            return f"🚀 **Try harder problems** - You've got the basics down, challenge yourself with medium difficulty!"
        else:
            return f"⭐ **Excellent mastery!** Consider exploring advanced problems or moving to a new topic."

    def process_all_content(self):
        """Main processing function."""
        print("🚀 Preparing LeetCode Coach content for GitHub Wiki (SIMPLIFIED)...")

        # Clean and setup
        self.clean_target_directory()

        # Create main dashboard
        self.create_home_dashboard()

        # Create one consolidated page per topic
        topics_dir = self.source_dir / "topics"
        if topics_dir.exists():
            for topic_dir in topics_dir.iterdir():
                if topic_dir.is_dir() and not topic_dir.name.startswith('.'):
                    self.create_consolidated_topic_page(topic_dir.name)

        print(f"\n✅ Wiki content prepared in: {self.target_dir}")
        print("📄 Generated pages:")
        for wiki_file in sorted(self.target_dir.glob("*.md")):
            print(f"   - {wiki_file.name}")
        print("\n🎯 Much cleaner structure - one page per topic!")


if __name__ == "__main__":
    processor = WikiContentProcessor()
    processor.process_all_content()