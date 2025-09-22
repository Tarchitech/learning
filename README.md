# learning-git

## Most Important Git Commands for Daily Work

### Essential Workflow Commands (Must Know)

#### 1. Check Status and Logs
```bash
# Check current status (most frequently used)
git status

# View commit history
git log --oneline

# View file differences
git diff
```

#### 2. Basic Operations Workflow
```bash
# Clone a repository
git clone https://github.com/Tarchitech/learning-git.git

# Add files to staging area
git add .

# Commit changes
git commit -m "Describe your changes"

# Push to remote repository
git push

# Pull remote updates
git pull
```

### Branch Management Commands (Important)

#### 3. Branch Operations
```bash
# View all branches
git branch -a

# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge latest change in main branch to current branch
git merge main

# Rebase based on main branch
git rebase main

# Delete branch
git branch -d feature/new-feature
```

#### 4. Remote Operations
```bash
# View remote repositories
git remote -v

# Add remote repository
git remote add origin <url>

# Push new branch to remote
git push -u origin feature/new-feature
```

### Undo and Fix Commands (Emergency Use)

#### 5. Undo Operations
```bash
# Undo working directory changes
git checkout -- filename

# Unstage files from staging area
git reset HEAD filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

#### 6. Modify Commits
```bash
# Modify last commit message
git commit --amend

# Modify last commit content
git add .
git commit --amend --no-edit
```

### Advanced but Practical Commands

#### 7. View and Compare
```bash
# View file modification history
git log --follow filename

# Compare two branches
git diff branch1..branch2

# View specific commit changes
git show commit-hash
```

#### 8. Stash and Restore
```bash
# Stash current changes
git stash

# View stash list
git stash list

# Restore stashed changes
git stash pop

# Apply stashed changes without removing
git stash apply
```

### Daily Usage Frequency Ranking

#### 🔥 Used Daily (90% of the time)
```bash
git status          # Check status
git add .           # Add files
git commit -m "..."  # Commit
git push            # Push
git pull            # Pull
```

#### 🔥 Frequently Used (70% of the time)
```bash
git log --oneline   # View history
git checkout -b ... # Create branch
git merge ...       # Merge branch
git diff            # View differences
```

#### 🔥 Occasionally Used (30% of the time)
```bash
git stash           # Stash changes
git reset ...       # Undo operations
git branch -d ...   # Delete branch
git remote -v       # View remotes
```

### Practical Command Combinations

#### 1. Quick Commit Workflow
```bash
git add . && git commit -m "fix: fix login issue" && git push
```

#### 2. Save Work Before Switching Branches
```bash
git stash && git checkout other-branch && git stash pop
```

#### 3. View Recent Commits
```bash
git log --oneline -10
```

#### 4. Quick Feature Branch Creation
```bash
git checkout -b feature/$(date +%Y%m%d)-feature-name
```

### Configuration Commands (One-time Setup)

#### 5. Basic Configuration
```bash
# Set username and email
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Set default editor
git config --global core.editor "code --wait"

# Set default branch name
git config --global init.defaultBranch main
```

### Common Alias Setup

```bash
# Set common aliases
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'
```

### Real Work Scenario Examples

#### Scenario 1: Start New Feature
```bash
git checkout main
git pull
git checkout -b feature/user-authentication
# Start coding...
git add .
git commit -m "feat: add user authentication feature"
git push -u origin feature/user-authentication
```

#### Scenario 2: Fix Urgent Bug
```bash
git checkout main
git pull
git checkout -b hotfix/critical-bug
# Fix bug...
git add .
git commit -m "fix: fix critical bug"
git push
git checkout main
git merge hotfix/critical-bug
git push
```

#### Scenario 3: Handle Conflicts
```bash
git pull
# Resolve conflicts...
git add .
git commit -m "resolve: resolve merge conflicts"
git push
```

### Summary

**Top 5 Core Commands:**
1. `git status` - Check status
2. `git add .` - Add all changed files
3. `git commit -m "..."` - Commit all files
4. `git push` - Push commits to remote
5. `git pull` - Pull from remote

Mastering these 5 commands will handle 90% of daily Git work. Other commands can be learned gradually as needed.

## Recommended Tools

### Enhanced Git Prompt: bash-git-prompt

**Repository:** https://github.com/magicmonty/bash-git-prompt

**Why it's recommended:**

The bash-git-prompt is an excellent tool that significantly enhances your Git workflow by providing:

- **Visual Git Status**: Shows current branch, commit status, and repository state directly in your terminal prompt
- **Color-coded Information**: Uses colors to quickly identify:
  - Current branch name
  - Modified, staged, and untracked files
  - Ahead/behind status with remote
  - Stash count
  - Merge/rebase status
- **Real-time Feedback**: No need to constantly run `git status` - the information is always visible
- **Customizable Themes**: Multiple built-in themes and easy customization options
- **Performance Optimized**: Fast and lightweight, won't slow down your terminal

**Installation:**
```bash
# Clone the repository
git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt

# Add to your ~/.bashrc or ~/.bash_profile
echo "source ~/.bash-git-prompt/gitprompt.sh" >> ~/.bashrc
```

This tool is particularly valuable for beginners as it provides constant visual feedback about your Git repository state, helping you understand Git concepts better and reducing the need to remember complex command combinations.