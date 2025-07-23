#!/bin/bash

# Remove Due Dates from GitHub Milestones for HireIQ
# This script removes all milestone due dates to prevent overdue status

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Removing Due Dates from GitHub Milestones for HireIQ${NC}"
echo "========================================================"

# Function to remove milestone due date
remove_milestone_due_date() {
    local milestone_name="$1"
    
    echo -e "${YELLOW}Removing due date from milestone: $milestone_name${NC}"
    
    # Get milestone ID
    local milestone_id=$(gh api repos/Muadeel56/hireiq/milestones --jq ".[] | select(.title == \"$milestone_name\") | .number")
    
    if [ -z "$milestone_id" ]; then
        echo -e "${YELLOW}⚠️  Milestone not found: $milestone_name${NC}"
        return 1
    fi
    
    # Remove milestone due date by setting it to null
    gh api --method PATCH repos/Muadeel56/hireiq/milestones/$milestone_id \
        --field due_on=null
    
    echo -e "${GREEN}✅ Removed due date from milestone: $milestone_name${NC}"
}

# Remove due dates from all milestones
echo -e "${BLUE}📅 Removing due dates from milestones...${NC}"

remove_milestone_due_date "🌱 Foundation & Authentication"
remove_milestone_due_date "🔍 AI Resume & Job Parsing"
remove_milestone_due_date "🎯 Matching Algorithm & Core Features"
remove_milestone_due_date "📊 Analytics & Advanced Features"
remove_milestone_due_date "🚀 Production & Launch"

echo ""
echo -e "${GREEN}🎉 All milestone due dates removed successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Milestones without due dates:${NC}"
echo "- 🌱 Foundation & Authentication"
echo "- 🔍 AI Resume & Job Parsing"
echo "- 🎯 Matching Algorithm & Core Features"
echo "- 📊 Analytics & Advanced Features"
echo "- 🚀 Production & Launch"
echo ""
echo -e "${GREEN}Milestones will no longer show as overdue! 🚀${NC}" 