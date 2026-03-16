#!/bin/bash

# GitHub Push Script for Docling Factory
# This script initializes a git repository and pushes to GitHub

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if git is installed
if ! command_exists git; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi

print_info "Docling Factory - GitHub Push Script"
echo ""

# Get the project root directory (parent of scripts/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

print_info "Working directory: $PROJECT_ROOT"
echo ""

# Check if already a git repository
if [ -d ".git" ]; then
    print_warning "Git repository already exists."
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted."
        exit 0
    fi
else
    # Initialize git repository
    print_info "Initializing git repository..."
    git init
    print_success "Git repository initialized"
    echo ""
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_info "Creating .gitignore file..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Application specific
output/*.md
output/*.html
output/*.json
!output/.gitkeep

# Temporary files
*.tmp
.cache/

# Environment variables
.env
.env.local
EOF
    print_success ".gitignore created"
    echo ""
fi

# Create .gitkeep files for empty directories
print_info "Creating .gitkeep files for empty directories..."
touch input/.gitkeep
touch output/.gitkeep
touch logs/.gitkeep
print_success ".gitkeep files created"
echo ""

# Get user information
print_info "Git Configuration"
echo ""

# Check if git user is configured
if ! git config user.name >/dev/null 2>&1; then
    read -p "Enter your name: " git_name
    git config user.name "$git_name"
fi

if ! git config user.email >/dev/null 2>&1; then
    read -p "Enter your email: " git_email
    git config user.email "$git_email"
fi

print_success "Git user configured: $(git config user.name) <$(git config user.email)>"
echo ""

# Add all files
print_info "Adding files to git..."
git add .
print_success "Files added"
echo ""

# Check if there are changes to commit
if git diff --cached --quiet; then
    print_warning "No changes to commit"
else
    # Commit changes
    read -p "Enter commit message (default: 'Initial commit - Docling Factory'): " commit_msg
    commit_msg=${commit_msg:-"Initial commit - Docling Factory"}
    
    print_info "Committing changes..."
    git commit -m "$commit_msg"
    print_success "Changes committed"
    echo ""
fi

# Check if remote exists
if git remote | grep -q "origin"; then
    print_warning "Remote 'origin' already exists"
    git remote -v
    echo ""
    read -p "Do you want to update the remote URL? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter GitHub repository URL (e.g., https://github.com/username/docling-factory.git): " repo_url
        git remote set-url origin "$repo_url"
        print_success "Remote URL updated"
    fi
else
    # Add remote
    read -p "Enter GitHub repository URL (e.g., https://github.com/username/docling-factory.git): " repo_url
    
    if [ -z "$repo_url" ]; then
        print_warning "No repository URL provided. Skipping remote setup."
        print_info "You can add a remote later with: git remote add origin <URL>"
        exit 0
    fi
    
    print_info "Adding remote repository..."
    git remote add origin "$repo_url"
    print_success "Remote repository added"
    echo ""
fi

# Get current branch name
current_branch=$(git branch --show-current)
if [ -z "$current_branch" ]; then
    current_branch="main"
    git branch -M main
fi

# Push to GitHub
print_info "Pushing to GitHub..."
echo ""
read -p "Push to branch '$current_branch'? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if branch exists on remote
    if git ls-remote --heads origin "$current_branch" | grep -q "$current_branch"; then
        print_info "Pushing to existing branch '$current_branch'..."
        git push origin "$current_branch"
    else
        print_info "Creating and pushing new branch '$current_branch'..."
        git push -u origin "$current_branch"
    fi
    print_success "Successfully pushed to GitHub!"
    echo ""
    print_info "Repository URL: $(git remote get-url origin)"
else
    print_info "Push cancelled. You can push later with: git push origin $current_branch"
fi

echo ""
print_success "Git setup complete!"
print_info "Next steps:"
echo "  1. Visit your GitHub repository"
echo "  2. Add a description and topics"
echo "  3. Configure branch protection rules (optional)"
echo "  4. Set up GitHub Actions (optional)"

# Made with Bob
