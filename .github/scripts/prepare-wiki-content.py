#!/usr/bin/env python3
"""
Prepare LeetCode Coach content for GitHub Wiki synchronization.

This script transforms the structured learning content into wiki-ready format:
- Organizes topic content with proper wiki naming
- Creates navigation and index pages
- Processes cross-references and links
- Generates learning progress visualization
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

    def wiki_safe_filename(self, name):
        """Convert filename to wiki-safe format."""
        # GitHub wiki pages use specific naming conventions
        name = re.sub(r'[^a-zA-Z0-9-_\s]', '', name)
        name = name.replace(' ', '-').replace('_', '-')
        return re.sub(r'-+', '-', name).strip('-')

    def process_topic_content(self, topic_name):
        """Process all content for a specific topic."""
        topic_path = self.source_dir / "topics" / topic_name
        if not topic_path.exists():
            return

        print(f"Processing topic: {topic_name}")

        # Create wiki pages for topic
        self.create_topic_overview(topic_name, topic_path)
        self.create_topic_session_notes(topic_name, topic_path)
        self.create_topic_concepts(topic_name, topic_path)
        self.process_topic_problems(topic_name, topic_path)

    def create_topic_overview(self, topic_name, topic_path):
        """Create main overview page for topic."""
        readme_path = topic_path / "README.md"
        if not readme_path.exists():
            return

        # Read original README content
        with open(readme_path, 'r') as f:
            content = f.read()

        # Add wiki-specific navigation and metadata
        wiki_content = self.add_wiki_navigation(topic_name, content, "overview")

        # Write to wiki format
        safe_name = self.wiki_safe_filename(topic_name.replace('-', ' ').title())
        wiki_file = self.target_dir / f"{safe_name}.md"

        with open(wiki_file, 'w') as f:
            f.write(wiki_content)

        print(f"  Created overview: {wiki_file.name}")

    def create_topic_session_notes(self, topic_name, topic_path):
        """Create session notes page for topic."""
        notes_path = topic_path / "notes" / "session-notes.md"
        if not notes_path.exists():
            return

        with open(notes_path, 'r') as f:
            content = f.read()

        # Add topic statistics and progress info
        stats = self.get_topic_stats(topic_name)
        stats_content = self.format_topic_stats(topic_name, stats)

        wiki_content = self.add_wiki_navigation(topic_name, content, "sessions")
        wiki_content = stats_content + "\n\n" + wiki_content

        safe_name = self.wiki_safe_filename(f"{topic_name.replace('-', ' ')} Sessions")
        wiki_file = self.target_dir / f"{safe_name}.md"

        with open(wiki_file, 'w') as f:
            f.write(wiki_content)

        print(f"  Created sessions: {wiki_file.name}")

    def create_topic_concepts(self, topic_name, topic_path):
        """Create concepts reference page for topic."""
        concepts_path = topic_path / "notes" / "concepts.md"
        if not concepts_path.exists():
            return

        with open(concepts_path, 'r') as f:
            content = f.read()

        wiki_content = self.add_wiki_navigation(topic_name, content, "concepts")

        safe_name = self.wiki_safe_filename(f"{topic_name.replace('-', ' ')} Concepts")
        wiki_file = self.target_dir / f"{safe_name}.md"

        with open(wiki_file, 'w') as f:
            f.write(wiki_content)

        print(f"  Created concepts: {wiki_file.name}")

    def process_topic_problems(self, topic_name, topic_path):
        """Process individual problem files for topic."""
        problems_path = topic_path / "problems"
        if not problems_path.exists():
            return

        for problem_file in problems_path.glob("*.md"):
            with open(problem_file, 'r') as f:
                content = f.read()

            wiki_content = self.add_wiki_navigation(topic_name, content, "problem")

            safe_name = self.wiki_safe_filename(f"{topic_name.replace('-', ' ')} {problem_file.stem}")
            wiki_file = self.target_dir / f"{safe_name}.md"

            with open(wiki_file, 'w') as f:
                f.write(wiki_content)

            print(f"  Created problem: {wiki_file.name}")

    def add_wiki_navigation(self, topic_name, content, page_type):
        """Add navigation breadcrumbs and cross-links."""
        topic_display = topic_name.replace('-', ' & ').title()

        # Navigation header
        nav_header = f"""<!-- Wiki Navigation -->
[🏠 Home](Home) | [📚 All Topics](Learning-Dashboard) | [📊 Progress](Learning-Progress)

**Current Topic:** {topic_display}

---

"""

        # Add topic navigation menu
        topic_nav = self.create_topic_navigation(topic_name, page_type)

        return nav_header + topic_nav + "\n\n" + content

    def create_topic_navigation(self, topic_name, current_page):
        """Create navigation menu for topic pages."""
        topic_display = topic_name.replace('-', ' ').title()
        topic_safe = self.wiki_safe_filename(topic_display)

        nav_items = [
            ("📖 Overview", f"{topic_safe}", "overview"),
            ("📝 Sessions", f"{topic_safe.replace(' ', '-')}-Sessions", "sessions"),
            ("🧠 Concepts", f"{topic_safe.replace(' ', '-')}-Concepts", "concepts")
        ]

        nav_links = []
        for label, page, page_type in nav_items:
            if page_type == current_page:
                nav_links.append(f"**{label}**")  # Bold for current page
            else:
                nav_links.append(f"[{label}]({page})")

        return f"**{topic_display}:** {' | '.join(nav_links)}\n"

    def get_topic_stats(self, topic_name):
        """Extract statistics for a topic from progress data."""
        topics = self.progress_data.get("topics", {})
        return topics.get(topic_name, {})

    def format_topic_stats(self, topic_name, stats):
        """Format topic statistics for wiki display."""
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
            last_practiced_str = "Not yet"

        stats_content = f"""## 📊 {topic_name.replace('-', ' & ').title()} Progress

| Metric | Value |
|--------|--------|
| **Mastery Level** | {mastery:.1f}% |
| **Problems Solved** | {solved}/{total} |
| **Practice Sessions** | {sessions} |
| **Last Practiced** | {last_practiced_str} |

---"""

        return stats_content

    def create_learning_dashboard(self):
        """Create main learning dashboard/home page."""
        dashboard_content = f"""# 🎯 LeetCode Coach Learning Dashboard

*Your personal learning wiki - auto-generated from practice sessions*

**Last Updated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## 📈 Overall Progress

{self.format_overall_progress()}

---

## 📚 Learning Topics

{self.format_topics_overview()}

---

## 🎯 Quick Navigation

### By Difficulty
- [🟢 Easy Problems](Learning-Progress#easy)
- [🟡 Medium Problems](Learning-Progress#medium)
- [🔴 Hard Problems](Learning-Progress#hard)

### By Pattern
- [🔄 Two Pointers](Two-Pointers-Pattern)
- [📊 Sliding Window](Sliding-Window-Pattern)
- [🌳 Tree Traversal](Tree-Traversal-Pattern)
- [⚡ Dynamic Programming](Dynamic-Programming-Pattern)

---

## 📖 How to Use This Wiki

1. **Start with a topic overview** to understand key concepts
2. **Review session notes** to see your progress and AI feedback
3. **Study concept guides** for in-depth pattern explanations
4. **Track your progress** on the [Learning Progress](Learning-Progress) page

---

*This wiki is automatically updated when you practice with `coach judge [problem]`*
"""

        with open(self.target_dir / "Home.md", 'w') as f:
            f.write(dashboard_content)

        print("Created learning dashboard: Home.md")

    def format_overall_progress(self):
        """Format overall learning statistics."""
        profile = self.progress_data.get("profile", {})

        total_problems = profile.get("total_problems_attempted", 0)
        solved = profile.get("total_problems_solved", 0)
        sessions = profile.get("total_sessions", 0)
        streak = profile.get("current_streak", 0)

        return f"""| Metric | Value |
|--------|--------|
| **Problems Attempted** | {total_problems} |
| **Problems Solved** | {solved} |
| **Practice Sessions** | {sessions} |
| **Current Streak** | {streak} days |"""

    def format_topics_overview(self):
        """Format overview of all topics."""
        topics = self.progress_data.get("topics", {})
        topic_rows = []

        for topic_name, stats in topics.items():
            topic_display = topic_name.replace('-', ' & ').title()
            topic_safe = self.wiki_safe_filename(topic_display)

            mastery = stats.get("mastery_level", 0) * 100
            solved = stats.get("problems_solved", 0)
            total = stats.get("total_problems", 0)

            progress_bar = self.create_progress_bar(mastery)

            topic_rows.append(
                f"| [{topic_display}]({topic_safe}) | {solved}/{total} | {mastery:.0f}% | {progress_bar} |"
            )

        if not topic_rows:
            return "*No topics practiced yet. Start with `coach practice <topic>` to begin!*"

        header = """| Topic | Solved | Mastery | Progress |
|-------|---------|---------|----------|"""

        return header + "\n" + "\n".join(topic_rows)

    def create_progress_bar(self, percentage):
        """Create visual progress bar for wiki."""
        filled = int(percentage / 10)  # 10 blocks for 100%
        empty = 10 - filled
        return "🟩" * filled + "⬜" * empty

    def create_learning_progress_page(self):
        """Create detailed progress tracking page."""
        progress_content = f"""# 📊 Learning Progress

*Detailed analytics and progress tracking*

---

{self.format_session_history()}

---

{self.format_topic_mastery_details()}

---

## 🎯 Next Recommended Actions

{self.generate_recommendations()}
"""

        with open(self.target_dir / "Learning-Progress.md", 'w') as f:
            f.write(progress_content)

        print("Created learning progress page: Learning-Progress.md")

    def format_session_history(self):
        """Format recent session history."""
        sessions = self.progress_data.get("session_history", [])

        if not sessions:
            return "## 📅 Recent Sessions\n\n*No practice sessions yet.*"

        content = "## 📅 Recent Sessions\n\n"

        # Show last 10 sessions
        for session in sessions[-10:]:
            timestamp = session.get("timestamp", "")
            problem = session.get("problem", "Unknown")
            topic = session.get("topic", "unknown")
            result = session.get("result", "attempted")

            try:
                date_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                date_str = date_obj.strftime("%m/%d/%Y")
            except:
                date_str = "Recent"

            result_emoji = "✅" if result == "solved" else "🔄"
            topic_display = topic.replace('-', ' & ').title()
            problem_display = problem.replace('_', ' ').title()

            content += f"- {result_emoji} **{date_str}**: {problem_display} ({topic_display})\n"

        return content

    def format_topic_mastery_details(self):
        """Format detailed topic mastery breakdown."""
        topics = self.progress_data.get("topics", {})

        content = "## 🧠 Topic Mastery Breakdown\n\n"

        for topic_name, stats in topics.items():
            topic_display = topic_name.replace('-', ' & ').title()
            mastery = stats.get("mastery_level", 0) * 100

            content += f"### {topic_display}\n"
            content += f"- **Mastery Level**: {mastery:.1f}%\n"
            content += f"- **Problems Solved**: {stats.get('problems_solved', 0)}/{stats.get('total_problems', 0)}\n"
            content += f"- **Practice Sessions**: {stats.get('practice_sessions', 0)}\n"

            weak_concepts = stats.get("weak_concepts", [])
            if weak_concepts:
                content += f"- **Areas to Focus**: {', '.join(weak_concepts)}\n"

            content += "\n"

        return content

    def generate_recommendations(self):
        """Generate personalized learning recommendations."""
        topics = self.progress_data.get("topics", {})

        # Find topics that need attention
        weak_topics = []
        strong_topics = []

        for topic_name, stats in topics.items():
            mastery = stats.get("mastery_level", 0) * 100
            if mastery < 50:
                weak_topics.append((topic_name, mastery))
            elif mastery > 80:
                strong_topics.append((topic_name, mastery))

        recommendations = []

        if weak_topics:
            # Sort by lowest mastery first
            weak_topics.sort(key=lambda x: x[1])
            topic_name = weak_topics[0][0]
            topic_display = topic_name.replace('-', ' & ').title()
            recommendations.append(f"🎯 **Focus on {topic_display}** - your weakest area ({weak_topics[0][1]:.0f}% mastery)")

        if strong_topics:
            topic_name = strong_topics[0][0]
            topic_display = topic_name.replace('-', ' & ').title()
            recommendations.append(f"🚀 **Advance from {topic_display}** - you're doing great ({strong_topics[0][1]:.0f}% mastery)")

        if not recommendations:
            recommendations.append("🌟 **Start practicing!** Use `coach practice <topic>` to begin your learning journey")

        return "\n".join(f"- {rec}" for rec in recommendations)

    def process_all_content(self):
        """Main processing function - orchestrates all content preparation."""
        print("🚀 Preparing LeetCode Coach content for GitHub Wiki...")

        # Clean and setup target directory
        self.clean_target_directory()

        # Create main dashboard and progress pages
        self.create_learning_dashboard()
        self.create_learning_progress_page()

        # Process all topic directories
        topics_dir = self.source_dir / "topics"
        if topics_dir.exists():
            for topic_dir in topics_dir.iterdir():
                if topic_dir.is_dir():
                    self.process_topic_content(topic_dir.name)

        print(f"\n✅ Wiki content prepared in: {self.target_dir}")
        print("📁 Generated pages:")
        for wiki_file in sorted(self.target_dir.glob("*.md")):
            print(f"   - {wiki_file.name}")


if __name__ == "__main__":
    processor = WikiContentProcessor()
    processor.process_all_content()