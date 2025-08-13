#!/bin/bash

# Update GitHub Milestone Dates for HireIQ
# This script updates all milestone due dates to start from today

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Updating GitHub Milestone Dates for HireIQ${NC}"
echo "================================================"

# Function to update milestone due date
update_milestone() {
    local milestone_name="$1"
    local new_due_date="$2"
    
    echo -e "${YELLOW}Updating milestone: $milestone_name${NC}"
    
    # Get milestone ID
    local milestone_id=$(gh api repos/Muadeel56/hireiq/milestones --jq ".[] | select(.title == \"$milestone_name\") | .number")
    
    if [ -z "$milestone_id" ]; then
        echo -e "${YELLOW}⚠️  Milestone not found: $milestone_name${NC}"
        return 1
    fi
    
    # Update milestone due date
    gh api --method PATCH repos/Muadeel56/hireiq/milestones/$milestone_id \
        --field due_on="$new_due_date"
    
    echo -e "${GREEN}✅ Updated milestone: $milestone_name (Due: $new_due_date)${NC}"
}

# Update all milestones with new dates
echo -e "${BLUE}📅 Updating milestone due dates...${NC}"

update_milestone "🌱 Foundation & Authentication" "2024-08-14"
update_milestone "🔍 AI Resume & Job Parsing" "2024-09-04"
update_milestone "🎯 Matching Algorithm & Core Features" "2024-10-02"
update_milestone "📊 Analytics & Advanced Features" "2024-10-23"
update_milestone "🚀 Production & Launch" "2024-11-13"

echo ""
echo -e "${GREEN}🎉 All milestone dates updated successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Updated Timeline:${NC}"
echo "- 🌱 Foundation & Authentication: Due August 14, 2024"
echo "- 🔍 AI Resume & Job Parsing: Due September 4, 2024"
echo "- 🎯 Matching Algorithm & Core Features: Due October 2, 2024"
echo "- 📊 Analytics & Advanced Features: Due October 23, 2024"
echo "- 🚀 Production & Launch: Due November 13, 2024"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}" 