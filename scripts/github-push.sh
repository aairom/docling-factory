#!/bin/bash

# 1. Ask for the Repository URL
echo "Enter the GitHub Repository URL:"
read repo_url

# 2. Initialize if .git doesn't exist
if [ ! -d ".git" ]; then
    echo "Initializing new Git repository..."
    git init
    git branch -M main
else
    echo "Existing Git repository detected."
fi

# 3. Check for nested .git folders (to prevent the 'link' error)
find . -mindepth 2 -name ".git" -type d -exec rm -rf {} + 2>/dev/null
echo "Cleaned up any nested .git folders to prevent subfolder linking."

# 4. Add Remote if it doesn't exist
if ! git remote | grep -q "origin"; then
    git remote add origin "$repo_url"
    echo "Remote 'origin' added."
else
    # Update the URL in case it changed
    git remote set-url origin "$repo_url"
fi

# 5. Add, Commit, and Push
echo "Enter commit message (default: 'update'):"
read commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="update"
fi

git add .
git commit -m "$commit_msg"

echo "Pushing to GitHub..."
git push -u origin main

echo "Done! Check your GitHub repo."