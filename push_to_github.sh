#!/bin/bash

echo "=========================================="
echo "Push to GitHub"
echo "=========================================="
echo ""

# Check if remote is already set
if git remote get-url origin > /dev/null 2>&1; then
    echo "Remote 'origin' is already set to:"
    git remote get-url origin
    echo ""
    read -p "Do you want to push to this remote? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push -u origin main
        echo ""
        echo "✓ Successfully pushed to GitHub!"
        exit 0
    fi
fi

echo "To push to GitHub, you need to:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name it (e.g., 'tyc-islamic-finance-advisor')"
echo "   - Choose Public or Private"
echo "   - DO NOT initialize with README, .gitignore, or license"
echo "   - Click 'Create repository'"
echo ""
echo "2. Copy the repository URL (it will look like):"
echo "   https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
echo ""
echo "3. Run this command with your URL:"
echo "   git remote add origin YOUR_REPO_URL"
echo "   git push -u origin main"
echo ""
echo "Or, if you already have the URL, paste it below:"
echo ""

read -p "GitHub repository URL: " repo_url

if [ -z "$repo_url" ]; then
    echo "No URL provided. Exiting."
    exit 1
fi

# Add remote
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"

# Push
echo ""
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Successfully pushed to GitHub!"
    echo "=========================================="
    echo ""
    echo "Your repository is now at: $repo_url"
    echo ""
    echo "Next step: Deploy to Render (see DEPLOY.md)"
else
    echo ""
    echo "⚠ Error pushing to GitHub. Please check:"
    echo "   - Your repository URL is correct"
    echo "   - You have access to the repository"
    echo "   - You're authenticated with GitHub"
fi

