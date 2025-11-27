#!/bin/bash

echo "=========================================="
echo "TYC Islamic Finance Advisor - Deployment Prep"
echo "=========================================="
echo ""

# Check if .env exists
if [ -f .env ]; then
    echo "✓ .env file found"
    # Check if it's in .gitignore
    if grep -q "^\.env$" .gitignore 2>/dev/null; then
        echo "✓ .env is in .gitignore (good!)"
    else
        echo "⚠ Warning: .env should be in .gitignore"
    fi
else
    echo "⚠ Warning: .env file not found"
fi

# Check if git is initialized
if [ -d .git ]; then
    echo "✓ Git repository initialized"
    
    # Check if files are committed
    if git diff --quiet && git diff --cached --quiet; then
        echo "✓ All changes committed"
    else
        echo "⚠ You have uncommitted changes"
        echo "  Run: git add . && git commit -m 'Prepare for deployment'"
    fi
else
    echo "⚠ Git not initialized"
    echo "  Run: git init"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create a GitHub repository"
echo "2. Push your code:"
echo "   git remote add origin YOUR_REPO_URL"
echo "   git push -u origin main"
echo ""
echo "3. Go to https://render.com and:"
echo "   - Sign up/login"
echo "   - Create new Web Service"
echo "   - Connect your GitHub repo"
echo "   - Add OPENAI_API_KEY in Environment tab"
echo "   - Deploy!"
echo ""
echo "For detailed instructions, see DEPLOY.md"
echo ""

