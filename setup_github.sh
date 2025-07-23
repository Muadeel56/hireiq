#!/bin/bash

# One-Click GitHub Setup for HireIQ
# This script will set up everything on GitHub automatically

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🚀 HireIQ GitHub One-Click Setup${NC}"
echo "====================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI is not installed.${NC}"
    echo ""
    echo -e "${YELLOW}📦 Installing GitHub CLI...${NC}"
    echo ""
    
    # Install GitHub CLI on Ubuntu/Debian
    if command -v apt &> /dev/null; then
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh -y
    else
        echo -e "${RED}❌ Please install GitHub CLI manually:${NC}"
        echo "Visit: https://cli.github.com/"
        exit 1
    fi
    
    echo -e "${GREEN}✅ GitHub CLI installed successfully!${NC}"
    echo ""
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}🔐 GitHub authentication required.${NC}"
    echo ""
    echo -e "${BLUE}Please authenticate with GitHub:${NC}"
    echo "1. A browser window will open"
    echo "2. Follow the authentication process"
    echo "3. Return to this terminal when done"
    echo ""
    read -p "Press Enter to continue with authentication..."
    
    gh auth login
fi

# Check if jq is installed (required for JSON parsing)
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}📦 Installing jq (JSON processor)...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt install jq -y
    else
        echo -e "${RED}❌ Please install jq manually:${NC}"
        echo "Visit: https://stedolan.github.io/jq/download/"
        exit 1
    fi
fi

echo -e "${GREEN}✅ All prerequisites are ready!${NC}"
echo ""

# Get repository info
REPO_OWNER=$(gh repo view --json owner -q .owner.login)
REPO_NAME=$(gh repo view --json name -q .name)

echo -e "${BLUE}📋 Repository: $REPO_OWNER/$REPO_NAME${NC}"
echo ""

# Confirm before proceeding
echo -e "${YELLOW}⚠️  This will create:${NC}"
echo "- 25 GitHub labels"
echo "- 5 GitHub milestones"
echo "- 25 GitHub issues"
echo "- 1 project board with 8 columns"
echo ""
read -p "Do you want to proceed? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Setup cancelled.${NC}"
    exit 1
fi

echo ""
echo -e "${PURPLE}🚀 Starting GitHub setup...${NC}"
echo ""

# Run the main setup script
./scripts/setup_github_project.sh

echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📋 What was created:${NC}"
echo "✅ 25 GitHub labels for organization"
echo "✅ 5 GitHub milestones with due dates"
echo "✅ 25 GitHub issues with detailed descriptions"
echo "✅ 1 project board with 8 workflow columns"
echo ""
echo -e "${YELLOW}🔗 Next Steps:${NC}"
echo "1. Visit your GitHub repository to see all items"
echo "2. Review and adjust any issues or labels"
echo "3. Set up automation rules in the project board"
echo "4. Start working on Milestone 1 issues"
echo "5. Configure team access and permissions"
echo ""
echo -e "${CYAN}📋 Useful Commands:${NC}"
echo "- View all issues: gh issue list"
echo "- View project board: gh project list"
echo "- Add team members: gh repo edit --add-collaborator username"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}" 