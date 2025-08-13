#!/bin/bash

# Add All Issues to Project Board for HireIQ
# This script adds all 25 issues to the project board

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Adding All Issues to Project Board for HireIQ${NC}"
echo "======================================================"

# Project details
PROJECT_NUMBER=5
PROJECT_OWNER="Muadeel56"

echo -e "${GREEN}✅ Using project board: $PROJECT_OWNER/projects/$PROJECT_NUMBER${NC}"
echo ""

# Get all issue numbers
echo -e "${YELLOW}Getting all issue numbers...${NC}"
ISSUE_NUMBERS=$(gh issue list --json number --jq '.[].number')

echo -e "${GREEN}✅ Found $(echo $ISSUE_NUMBERS | wc -w) issues${NC}"
echo ""

# Add all issues to the project board
echo -e "${YELLOW}Adding issues to project board...${NC}"

for issue_num in $ISSUE_NUMBERS; do
    echo -e "${YELLOW}Adding issue #$issue_num to project board${NC}"
    
    # Add issue to project board using URL
    gh project item-add $PROJECT_NUMBER --url "https://github.com/Muadeel56/hireiq/issues/$issue_num" --owner $PROJECT_OWNER
    
    echo -e "${GREEN}✅ Added issue #$issue_num to project board${NC}"
done

echo ""
echo -e "${GREEN}🎉 All issues added to project board successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Project Board Details:${NC}"
echo "- Name: HireIQ Development Board"
echo "- Project Number: $PROJECT_NUMBER"
echo "- Owner: $PROJECT_OWNER"
echo "- Issues Added: $(echo $ISSUE_NUMBERS | wc -w) issues"
echo ""
echo -e "${PURPLE}📋 What was completed:${NC}"
echo "✅ Added all issues to the project board"
echo "✅ Issues are now visible in the project board"
echo "✅ Ready for workflow management"
echo ""
echo -e "${YELLOW}🔗 Next Steps:${NC}"
echo "1. Visit: https://github.com/users/Muadeel56/projects/5"
echo "2. Move issues between columns as needed"
echo "3. Set up automation rules in the project board"
echo "4. Assign issues to team members"
echo "5. Start development with Milestone 1 issues"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}" 