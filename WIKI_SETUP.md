# 📖 GitHub Wiki Auto-Sync Setup Guide

Transform your LeetCode Coach into an automatically-updating GitHub Wiki! This guide walks you through setting up the auto-sync pipeline.

## 🎯 What This Does

Your learning content will automatically sync to a beautiful GitHub Wiki whenever you:
- Complete a practice session with `coach judge [problem]`
- Update your notes or topic guides
- Make progress in your learning journey

**Wiki Features:**
- 🏠 **Learning Dashboard** - Overview of your progress and topics
- 📚 **Topic Pages** - Comprehensive guides with navigation
- 📝 **Session Notes** - Auto-logged practice sessions with AI feedback
- 🧠 **Concept Guides** - Evolving knowledge base from your practice
- 📊 **Progress Tracking** - Visual progress bars and statistics
- 🔗 **Smart Navigation** - Cross-linked topics and concepts

## ⚡ Quick Setup (5 minutes)

### Step 1: Enable Wiki for Your Repository

1. Go to your GitHub repository
2. Click **Settings** tab
3. Scroll down to **Features** section
4. Check the **Wikis** checkbox
5. Click **Save changes**

### Step 2: Create GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/personal-access-tokens/tokens)
2. Click **Generate new token (classic)**
3. Give it a descriptive name: `LeetCode Coach Wiki Sync`
4. Select expiration: **No expiration** (recommended) or your preferred duration
5. Select these scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (Access public repositories) - if your repo is public

6. Click **Generate token**
7. **Copy the token immediately** - you won't see it again!

### Step 3: Add Token to Repository Secrets

1. Go to your repository **Settings > Secrets and variables > Actions**
2. Click **New repository secret**
3. Name: `WIKI_TOKEN`
4. Value: Paste the personal access token you just copied
5. Click **Add secret**

### Step 4: Test the Setup

1. Push these new files to your repository:
   ```bash
   git add .github/
   git add WIKI_SETUP.md
   git commit -m "Add GitHub Wiki auto-sync pipeline

   Co-Authored-By: Claude <noreply@anthropic.com>"
   git push
   ```

2. The GitHub Action should trigger automatically and sync your content

3. Check your repository's **Wiki** tab to see your learning dashboard!

## 🧪 Manual Testing

You can also manually trigger the wiki sync:

1. Go to your repository's **Actions** tab
2. Find the "Auto-Sync Learning Content to GitHub Wiki" workflow
3. Click **Run workflow** button
4. Click the green **Run workflow** button

## 🎯 What Gets Synced

The pipeline transforms your content structure:

```
topics/
├── linked-lists/
│   ├── README.md           → Linked Lists.md
│   ├── notes/
│   │   ├── session-notes.md → Linked Lists Sessions.md
│   │   └── concepts.md      → Linked Lists Concepts.md
│   └── problems/
│       └── reverse-list.md  → Linked Lists Reverse List.md
└── arrays-hashing/
    ├── README.md           → Arrays Hashing.md
    ├── notes/              → Arrays Hashing Sessions.md & Concepts.md
    └── problems/           → Individual problem pages

progress.json               → Powers dashboard statistics and progress bars
```

**Generated Wiki Pages:**
- `Home.md` - Main learning dashboard
- `Learning-Progress.md` - Detailed progress analytics
- `[Topic].md` - Topic overview pages
- `[Topic] Sessions.md` - Practice session logs
- `[Topic] Concepts.md` - Pattern guides and knowledge base

## 🔧 Customization Options

### Modify Sync Triggers

Edit `.github/workflows/wiki-sync.yml` to change when sync happens:

```yaml
on:
  push:
    branches: [ main, master ]
    paths:
      - 'topics/**/*.md'      # Topic content changes
      - 'progress.json'       # Progress updates
      # Add more paths as needed
```

### Customize Wiki Content

Modify `.github/scripts/prepare-wiki-content.py` to:
- Change page naming conventions
- Add custom navigation elements
- Include additional metadata
- Modify progress visualization

### Add Custom Wiki Pages

Create additional markdown files that will be included in the sync:

1. Add files to a `wiki-pages/` directory
2. Modify the script to copy them to the wiki
3. Link them from your dashboard or navigation

## 🎨 Example Wiki Output

Once set up, your wiki will look like:

### Home Page (Learning Dashboard)
```markdown
# 🎯 LeetCode Coach Learning Dashboard

## 📈 Overall Progress
| Problems Attempted | Problems Solved | Current Streak |
|--------------------|-----------------|----------------|
| 15                 | 12              | 3 days         |

## 📚 Learning Topics
| Topic | Solved | Mastery | Progress |
|-------|---------|---------|----------|
| [Linked Lists](Linked-Lists) | 3/5 | 60% | 🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜ |
| [Arrays & Hashing](Arrays-Hashing) | 2/8 | 25% | 🟩🟩⬜⬜⬜⬜⬜⬜⬜⬜ |
```

### Topic Pages with Navigation
```markdown
[🏠 Home](Home) | [📚 All Topics](Learning-Dashboard) | [📊 Progress](Learning-Progress)

**Linked Lists:** **📖 Overview** | [📝 Sessions](Linked-Lists-Sessions) | [🧠 Concepts](Linked-Lists-Concepts)

# Linked Lists
*Your comprehensive topic guide with patterns, examples, and strategies*
```

## 🚨 Troubleshooting

### Wiki sync fails?
1. Check that the `WIKI_TOKEN` secret is correctly set
2. Verify your repository has Wiki enabled
3. Check the Actions tab for error logs

### Content not appearing?
1. Make sure your file paths match the trigger paths in the workflow
2. Check that your markdown files are valid
3. Review the action logs for processing errors

### Permission errors?
1. Verify the personal access token has `repo` scope
2. Make sure the token hasn't expired
3. Check that you're the repository owner or have admin access

## 🎉 You're All Set!

Once configured, your LeetCode Coach will automatically:

1. ✅ **Track your practice** with `coach judge [problem]`
2. ✅ **Generate session notes** with AI feedback
3. ✅ **Update topic progress** and statistics
4. ✅ **Sync to GitHub Wiki** automatically
5. ✅ **Provide searchable** learning knowledge base
6. ✅ **Show visual progress** with charts and metrics

Your learning journey is now documented and searchable as a beautiful GitHub Wiki that grows with every practice session!

---

## 🔗 Useful Links

- [GitHub Wiki Documentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)
- [Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

*Happy learning! 🚀*