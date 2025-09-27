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

---

## Question 5: Practical Workflow 🚀

**Scenario:** You're working on a feature branch and need to get the latest changes from the main branch before continuing your work.

**Question:** What is the complete workflow to update your feature branch with the latest main branch changes?

**A)** `git checkout main` → `git pull` → `git checkout feature-branch` → `git merge main`<br>
**B)** `git pull main` → `git merge main`<br>
**C)** `git checkout main` → `git merge feature-branch`<br>
**D)** `git fetch` → `git merge origin/main`<br>

---

## Bonus Question: Command Combination 💡

**Scenario:** You want to quickly commit and push your changes in one command chain.

**Question:** Which command combination accomplishes this efficiently?

**A)** `git add . && git commit -m "fix: fix login issue" . && git push`<br>
**B)** `git commit -m "fix: fix login issue" . && git push`<br>
**C)** `git add . && git push`<br>
**D)** `git commit && git push`<br>

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
