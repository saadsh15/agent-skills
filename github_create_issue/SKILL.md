---
name: github_create_issue
description: A skill to create a GitHub issue for a specified repository and automatically create a corresponding local/remote git branch using the `gh` CLI.
when_to_use: Use this skill when the user wants to create a GitHub issue, track a task or bug on GitHub, create a feature branch for an issue, or invokes the `/github_create_issue` command.
---

# GitHub Create Issue & Branch Skill

## Objective
Your goal is to automate the creation of a GitHub issue for a specified repository and create a corresponding Git branch for that issue. This workflow must use the `gh` CLI for all GitHub operations and standard `git` commands for branch creation.

## Core Directives

### 1. Authentication and CLI Verification
Before attempting any GitHub actions:
- Verify that the `gh` CLI is installed and configured on the system.
- Run `gh auth status` to check if the user is authenticated. 
- If the user is not authenticated, prompt them clearly to authenticate by running `gh auth login` in their terminal. Do not attempt to proceed with issue creation without successful authentication.

### 2. Repository and Issue Information Gathering
- If the user has not specified a repository, attempt to auto-detect it by querying the current git repository remote URL:
  ```bash
  git remote get-url origin
  ```
- Parse the remote URL to extract the `owner/repo` path (e.g., `saadsh15/agent-skills`).
- If no repository can be detected, ask the user to provide the repository name or URL.
- Retrieve or generate the issue title and body description. If details are missing, ask the user for clarification or formulate a descriptive title and body based on the task context.

### 3. Step-by-Step Execution Guide

#### Step 1: Create the Issue on GitHub
Use the `gh` CLI to create the issue. Capture the issue number and URL from the command output.
```bash
gh issue create --repo <owner/repo> --title "<title>" --body "<body>"
```
*Note: Make sure to wrap title and body in quotes and properly escape any internal quotes if executing via shell.*

#### Step 2: Format the Branch Name
Construct a clean, lowercase branch name from the issue number and slugified title:
- format: `<issue-number>-<slugified-title>`
- Remove special characters, replace spaces with hyphens, and convert to lowercase. E.g., for issue `#42` titled "Fix login redirect bug!", the branch name should be `42-fix-login-redirect-bug`.

#### Step 3: Create and Push the Branch
Create the branch locally and push it to the remote repository, setting the upstream tracking:
```bash
git checkout -b <branch-name>
git push -u origin <branch-name>
```

## Output Formatting Requirements
Once the issue and branch are successfully created, provide a clear, concise report containing:
1. **GitHub Issue Details:** The issue number, title, and a clickable link to the issue on GitHub.
2. **Branch Details:** The name of the created Git branch and confirmation that it has been pushed and set up with upstream tracking.
