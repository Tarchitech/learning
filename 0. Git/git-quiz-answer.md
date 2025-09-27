# Git Learning Quiz - Self-Assessment

Based on the learning-git README, test your understanding of the most common Git commands and workflows.

---

## Question 1: Daily Workflow Commands 🔥

**Scenario:** You've just finished coding a new feature and want to save your work to the repository.

**Question:** What is the correct sequence of commands to add your changes, commit them, and push to the remote repository?

**A)** `git commit -m "message" .` → `git add .` → `git push`<br>
**B)** `git add .` → `git commit -m "message" .` → `git push`<br>
**C)** `git push` → `git add .` → `git commit -m "message" .`<br>
**D)** `git status` → `git push` → `git commit -m "message" .`<br>

<details>
<summary>Click to see answer</summary>

**Answer: B)** `git add .` → `git commit -m "message" .` → `git push`

**Visual Representation:**
```
Working Directory → Staging Area → Local Repository → Remote Repository
     (modified)        (staged)        (committed)        (pushed)
         ↓                ↓                ↓                ↓
    git add .      git commit -m        git push
```

**Explanation:** This is the correct Git workflow sequence:
1. `git add .` - Stages all modified files for commit
2. `git commit -m "message" .` - Creates a commit with your changes
3. `git push` - Uploads your commits to the remote repository

This sequence represents the "Top 5 Core Commands" mentioned in the README and handles 90% of daily Git work.
</details>

---

## Question 2: Branch Management 🌿

**Scenario:** You need to create a new feature branch called "user-login" and switch to it immediately.

**Visual Representation:**
```
Before: main branch (current)
        *
        |
        |
After:  main branch
        |
        * user-login branch (current)
```

**Question:** Which command accomplishes this task in one step?

**A)** `git branch user-login && git checkout user-login`<br>
**B)** `git checkout -b user-login`<br>
**C)** `git create user-login`<br>
**D)** `git new-branch user-login`<br>

<details>
<summary>Click to see answer</summary>

**Answer: B)** `git checkout -b user-login`

**Explanation:** The `git checkout -b` command creates a new branch and switches to it in one step. This is much more efficient than creating the branch first and then checking it out separately. This command is listed in the "Frequently Used (70% of the time)" section of the README.
</details>

---

## Question 3: Status Checking 📊

**Scenario:** You want to see what files have been modified, staged, or are untracked in your repository.

**Visual Representation:**
```
git status output example:

On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/app.js

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   src/utils.js

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        new-file.txt
```

**Question:** Which command should you use to check the current status of your working directory?

**A)** `git log`<br>
**B)** `git status`<br>
**C)** `git diff`<br>
**D)** `git show`<br>

<details>
<summary>Click to see answer</summary>

**Answer: B)** `git status`

**Explanation:** `git status` is the most frequently used command (mentioned as "most frequently used" in the README) and shows you:
- Which files are modified but not staged
- Which files are staged for commit
- Which files are untracked
- Current branch information
- Whether your branch is ahead/behind the remote

This command is essential for understanding what changes you have before committing.
</details>

---

## Question 4: Undo Operations ↩️

**Scenario:** You accidentally added a file to the staging area but haven't committed yet. You want to unstage it.

**Visual Representation:**
```
Git Areas:
┌───────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Working Directory │    │ Staging Area    │    │ Local Repository│
│                   │    │                 │    │                 │
│ file.txt          │───▶│ file.txt        │    │                 │
│ (modified)        │    │ (staged)        │    │                 │
└───────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       │
         │                       │
         └───────────────────────┘
             unstages the file
```

**Question:** Which command will remove the file from the staging area while keeping your changes in the working directory?

**A)** `git checkout -- filename`<br>
**B)** `git reset HEAD filename`<br>
**C)** `git reset --hard HEAD filename`<br>
**D)** `git delete filename`<br>

<details>
<summary>Click to see answer</summary>

**Answer: B)** `git reset HEAD filename`

**Explanation:** `git reset HEAD filename` unstages the file from the staging area but keeps your changes in the working directory. This is useful when you've added a file with `git add` but want to unstage it before committing.

- `git checkout -- filename` would discard changes entirely
- `git reset --hard HEAD filename` would also discard changes
- `git delete filename` is not a valid Git command

This command is listed in the "Undo and Fix Commands" section of the README.
</details>

---

## Question 5: Practical Workflow 🚀

**Scenario:** You're working on a feature branch and need to get the latest changes from the main branch before continuing your work.

**Question:** What is the complete workflow to update your feature branch with the latest main branch changes?

**A)** `git checkout main` → `git pull` → `git checkout feature-branch` → `git merge main`<br>
**B)** `git pull main` → `git merge main`<br>
**C)** `git checkout main` → `git merge feature-branch`<br>
**D)** `git fetch` → `git merge origin/main`<br>

<details>
<summary>Click to see answer</summary>

**Answer: A)** `git checkout main` → `git pull` → `git checkout feature-branch` → `git merge main`

**Visual Representation:**
```
Step 1: git checkout main
main branch (current) ←── You are here
        |
        * feature-branch

Step 2: git pull
main branch (updated with latest changes) ←── You are here
        |
        * feature-branch

Step 3: git checkout feature-branch
main branch
        |
        * feature-branch (current) ←── You are here

Step 4: git merge main
main branch
        |
        * feature-branch (now has latest main changes) ←── You are here
```


**Explanation:** This is the complete workflow to update your feature branch:
1. `git checkout main` - Switch to main branch
2. `git pull` - Get latest changes from remote main branch
3. `git checkout feature-branch` - Switch back to your feature branch
4. `git merge main` - Merge the updated main branch into your feature branch

This workflow is demonstrated in "Scenario 1: Start New Feature" in the README and ensures your feature branch has the latest changes from main before you continue working.
</details>

---

## Bonus Question: Command Combination 💡

**Scenario:** You want to quickly commit and push your changes in one command chain.

**Question:** Which command combination accomplishes this efficiently?

**A)** `git add . && git commit -m "fix: fix login issue" . && git push`<br>
**B)** `git commit -m "fix: fix login issue" . && git push`<br>
**C)** `git add . && git push`<br>
**D)** `git commit && git push`<br>

<details>
<summary>Click to see answer</summary>

**Answer: A)** `git add . && git commit -m "fix: fix login issue" . && git push`

**Explanation:** This is the "Quick Commit Workflow" mentioned in the README's "Practical Command Combinations" section. The `&&` operator ensures each command only runs if the previous one succeeds, making it a safe and efficient way to:
1. Stage all changes
2. Commit with a descriptive message
3. Push to remote repository

This combination is perfect for quick commits when you're confident about your changes.
</details>

---

## Scoring Guide 📈

- **5/5 Correct:** Git Master! You understand the core workflows perfectly.
- **4/5 Correct:** Excellent! You have a solid understanding of Git basics.
- **3/5 Correct:** Good foundation! Review the incorrect answers and practice more.
- **2/5 or less:** Keep studying! Focus on the "Top 5 Core Commands" from the README.

## Key Takeaways 🎯

Remember the **Top 5 Core Commands** that handle 90% of daily Git work:
1. `git status` - Check status
2. `git add .` - Add all changed files  
3. `git commit -m "..." .` - Commit all files
4. `git push` - Push commits to remote
5. `git pull` - Pull from remote

Master these commands first, then gradually learn the advanced features as needed!
