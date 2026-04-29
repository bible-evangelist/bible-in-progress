# Setup Guide

Steps for publishing this project on GitHub.

## Prerequisites

- An anonymous GitHub account
- `git` installed locally
- (If you plan to run the AI branch) an Anthropic or OpenAI API key

## Step 1: Initialize the local repository

```bash
cd bible-in-progress
git init

# Repository-local settings (to prevent leaking your real identity)
git config user.name "bible-in-progress"
git config user.email "[ID]+[username]@users.noreply.github.com"

# First commit on main
git checkout -b main
git add .
git commit -m "Initial commit: the bible begins, in progress"
```

## Step 2: Create a remote on GitHub and push

On GitHub, create an empty repository named `bible-in-progress` (do not add a README, etc.).

```bash
git remote add origin https://github.com/[anonymous-username]/bible-in-progress.git
git push -u origin main
```

## Step 3: Create the three branches

```bash
# human branch
git checkout -b human main
git push -u origin human

# ai branch
git checkout -b ai main
git push -u origin ai

# Back to main
git checkout main
```

You now have `main`, `human`, and `ai`.

## Step 4: Set branch protection rules (GitHub Web UI)

In Settings → Branches → Add branch protection rule:

### `main`
- Require a pull request before merging: ON
- Require approvals: 1
- This forbids direct pushes to `main`.

### `human`
- Require a pull request before merging: ON
- Direct pushes only by maintainers.

### `ai`
- No protection (Actions need to push directly).
- By convention, do not push from anywhere other than the workflow.

## Step 5: Make `main` the default branch

In Settings → General → Default branch, set it to `main` (it should already be the default).

## Step 6: (Optional) Enable the AI update workflow

Only if you want to run the AI branch's automatic updates.

### 6-1. Register the API key as a secret

Settings → Secrets and variables → Actions → New repository secret

- Name: `ANTHROPIC_API_KEY`
- Value: your API key

### 6-2. Configure workflow permissions

Settings → Actions → General → Workflow permissions

- Select "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### 6-3. Smoke test

From the Actions tab, run the "AI Branch Monthly Update" workflow manually (workflow_dispatch).
On success, a new commit will appear on the `ai` branch.

## Step 7: Verify README links

Confirm that links in `README.md` (e.g., `../../tree/main`) work correctly in your repository.
Check on the GitHub repository page.

## Step 8: Prepare for launch

After publishing, prepare at minimum:

- An introductory blurb (within 280 characters, for X)
- The repository URL
- A "call for contributors" issue (a way to recruit early maintainers)
- (Optional) Posts for Hacker News, Reddit r/programming

Example blurb:
> A secular scripture for the twenty-first century, written democratically.
> No founder. No revelation. No god put into words.
> Humans and AI write it on separate branches.
> Sources required. Refutations welcome. Forever in progress.
> github.com/[anonymous-username]/bible-in-progress

## Troubleshooting

### My real name or main email leaked into a push

```bash
# Rewrite history (force push required; recommended only during initial setup)
git filter-branch --env-filter '
OLD_EMAIL="real-name@example.com"
NEW_NAME="bible-in-progress"
NEW_EMAIL="[ID]+[username]@users.noreply.github.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]; then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]; then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

git push --force --all
```

Note: if there are collaborators, force-pushing causes confusion. Use this only during initial setup.

### Actions are not running

- A private repository has limited free Actions minutes (2,000/month). Public repositories are unlimited.
- Re-check workflow permissions.
- Confirm the secret name (`ANTHROPIC_API_KEY`) is exact.

---

Once setup is done, a good first issue is "Call for contributors."
It helps you get through the quiet early period.
