---
name: github_push_code
description: A skill to securely push code to a specified GitHub repository, verify authentication, check remote branch existence, and prevent direct pushing to the main branch.
when_to_use: Use this skill when the user wants to push local commits to a GitHub repository, push code to a specific feature branch, or invokes the `/github_push_code` command.
---

# GitHub Push Code Skill

## Objective
Your goal is to securely push local code changes to a specified GitHub repository. You must verify authentication, confirm the target repository, check if a relevant remote branch exists, and ensure that you push to a specific feature branch rather than directly to the default `main`/`master` branch.

## Core Directives

### 1. Authentication Verification
Before pushing any code:
- Ensure the `gh` CLI is installed.
- Check authentication status using `gh auth status`.
- If authentication is missing, prompt the user to log in by running `gh auth login` in their terminal.

### 2. Repository and Branch Target Identification
- Ask the user for the target repository URL or `owner/repo` path if not already provided or if it cannot be determined via `git remote get-url origin`.
- Determine the current active local branch:
  ```bash
  git branch --show-current
  ```
- **Avoid Main Branch Push:** If the current branch is `main`, `master`, or the remote's default branch, DO NOT push to it directly. Prompt the user to specify or create a dedicated feature branch.

### 3. Branch Verification and Push Flow

#### Step 1: Check Remote Branch Existence
Check if the corresponding branch already exists on the remote repository:
```bash
git ls-remote --heads origin <branch-name>
```
- If the branch exists, inform the user and proceed with pushing the code to that specific branch.
- If the branch does not exist on remote, confirm if a new remote branch should be created.

#### Step 2: Push Code to the Specific Branch
Push the local branch commits to the remote repository, setting the tracking reference:
```bash
git push -u origin <branch-name>
```
*Never force-push (`git push -f`) unless explicitly requested by the user after confirming they understand the risk of overwriting remote changes.*

## Output Formatting Requirements
Provide a clear status report after the push operation:
1. **Repository & Branch Info:** Specify the target repository and the exact branch pushed to.
2. **Push Status:** Summary of git push output (e.g., new branch created, or commits updated).
3. **Link to Branch/PR:** Provide a clickable link to the branch on GitHub, and optionally suggest creating a Pull Request if the branch is new.
