#!/bin/bash

# Create GitHub Issues for HireIQ
# This script creates all the issues using the correct GitHub CLI syntax

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Creating GitHub Issues for HireIQ${NC}"
echo "=========================================="

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    local milestone="$4"
    
    echo -e "${YELLOW}Creating issue: $title${NC}"
    
    # Create the issue
    gh issue create --title "$title" --body "$body" --label "$labels" --milestone "$milestone"
    
    echo -e "${GREEN}✅ Created issue: $title${NC}"
}

# Milestone 1: Foundation & Authentication
echo -e "${BLUE}📋 Creating Milestone 1 Issues...${NC}"

create_issue \
    "🏗️ Set up Django REST API Project Structure" \
    "## Description
Set up the Django REST Framework project with proper folder structure, settings configuration, and basic API setup.

## Acceptance Criteria
- [ ] Django project initialized with REST framework
- [ ] PostgreSQL database configuration
- [ ] Environment variables setup (.env)
- [ ] Docker configuration for development
- [ ] Basic API health check endpoint
- [ ] CORS configuration for React frontend

## Estimated Time
3-4 days

## Technical Notes
- Use Django 4.2+ with Django REST Framework 3.14+
- Configure PostgreSQL with proper connection pooling
- Set up environment-based settings (development, production, testing)
- Include Docker Compose for local development
- Implement proper logging configuration" \
    "type:infrastructure,area:backend,priority:critical,complexity:medium" \
    "🌱 Foundation & Authentication"

create_issue \
    "🎨 Initialize React 19 Frontend with Tailwind CSS v4" \
    "## Description
Set up the React 19 frontend application with Tailwind CSS v4, proper routing, and development environment.

## Acceptance Criteria
- [ ] React 19 project with Vite setup
- [ ] Tailwind CSS v4 configuration
- [ ] React Router setup for SPA navigation
- [ ] ESLint and Prettier configuration
- [ ] Basic component structure and styling system
- [ ] Development environment scripts

## Estimated Time
2-3 days

## Technical Notes
- Use Vite for fast development and building
- Configure TypeScript for type safety
- Set up proper folder structure for components, pages, hooks
- Include Storybook for component documentation
- Configure hot reload and development tools" \
    "type:infrastructure,area:frontend,priority:critical,complexity:medium" \
    "🌱 Foundation & Authentication"

create_issue \
    "🔐 Implement User Authentication System" \
    "## Description
Build comprehensive authentication system supporting multiple user types (candidates, recruiters, admins).

## Acceptance Criteria
- [ ] JWT-based authentication
- [ ] User registration with email verification
- [ ] Login/logout functionality
- [ ] Password reset flow
- [ ] Role-based user types (Candidate, Recruiter, Admin)
- [ ] Protected routes on frontend
- [ ] Authentication middleware for API

## Estimated Time
5-7 days

## Technical Notes
- Use Django REST Framework JWT for token management
- Implement email verification with Django's email backend
- Create custom user model with role-based permissions
- Set up refresh token rotation for security
- Include rate limiting for authentication endpoints" \
    "type:feature,area:auth,priority:critical,complexity:large" \
    "🌱 Foundation & Authentication"

create_issue \
    "👤 Create User Profile Management" \
    "## Description
Build user profile pages with different interfaces for candidates and recruiters.

## Acceptance Criteria
- [ ] Candidate profile creation and editing
- [ ] Recruiter company profile setup
- [ ] Profile picture upload functionality
- [ ] Skills and experience management
- [ ] Contact information management
- [ ] Profile completion progress indicator

## Estimated Time
6-8 days

## Technical Notes
- Use Django's ImageField for profile pictures
- Implement file upload with proper validation
- Create separate profile models for candidates and recruiters
- Include profile completion scoring algorithm
- Set up image optimization and CDN integration" \
    "type:feature,area:frontend,area:backend,priority:high,complexity:large" \
    "🌱 Foundation & Authentication"

create_issue \
    "📱 Responsive UI/UX Design System" \
    "## Description
Create a cohesive design system with reusable components and responsive layouts.

## Acceptance Criteria
- [ ] Design system documentation
- [ ] Reusable UI components (buttons, forms, cards)
- [ ] Responsive layout for mobile/tablet/desktop
- [ ] Dark/light theme support
- [ ] Loading states and error handling
- [ ] Accessibility compliance (WCAG 2.1)

## Estimated Time
4-5 days

## Technical Notes
- Create component library with Storybook
- Use CSS custom properties for theming
- Implement proper focus management for accessibility
- Include responsive breakpoints for all screen sizes
- Set up design tokens for consistent styling" \
    "type:feature,area:frontend,priority:high,complexity:medium" \
    "🌱 Foundation & Authentication"

# Milestone 2: AI Resume & Job Parsing
echo -e "${BLUE}📋 Creating Milestone 2 Issues...${NC}"

create_issue \
    "🤖 Integrate AI Resume Parsing" \
    "## Description
Implement AI-powered resume parsing using OpenAI GPT-4 to extract structured data from uploaded resumes.

## Acceptance Criteria
- [ ] File upload functionality (PDF, DOC, DOCX)
- [ ] Integration with OpenAI API
- [ ] Structured data extraction (skills, experience, education)
- [ ] Resume content storage and indexing
- [ ] Error handling for parsing failures
- [ ] Progress tracking for async processing

## Estimated Time
8-10 days

## Technical Notes
- Use OpenAI GPT-4 for intelligent text extraction
- Implement file validation and virus scanning
- Create structured data models for parsed resume content
- Set up async processing with Celery
- Include fallback parsing for unsupported formats
- Implement retry logic for API failures" \
    "type:feature,area:ai,area:backend,priority:critical,complexity:large" \
    "🔍 AI Resume & Job Parsing"

create_issue \
    "📄 Job Description AI Analysis" \
    "## Description
Build AI system to analyze job descriptions and extract requirements, skills, and qualifications.

## Acceptance Criteria
- [ ] Job description input and validation
- [ ] AI analysis for required skills extraction
- [ ] Experience level determination
- [ ] Salary range suggestions based on market data
- [ ] Job category classification
- [ ] Structured job data storage

## Estimated Time
7-9 days

## Technical Notes
- Use OpenAI GPT-4 for job description analysis
- Implement skill taxonomy matching
- Create experience level classification algorithm
- Integrate with salary data APIs for market insights
- Set up job category taxonomy system
- Include confidence scoring for extracted data" \
    "type:feature,area:ai,area:backend,priority:critical,complexity:large" \
    "🔍 AI Resume & Job Parsing"

create_issue \
    "📊 Resume & Job Data Models" \
    "## Description
Design and implement database models for storing parsed resume and job data with proper relationships.

## Acceptance Criteria
- [ ] Resume data model with skills, experience, education
- [ ] Job posting model with requirements and details
- [ ] Skills taxonomy and standardization
- [ ] Experience level categorization
- [ ] Location and remote work preferences
- [ ] Database migrations and indexing

## Estimated Time
3-4 days

## Technical Notes
- Design normalized database schema for scalability
- Implement full-text search capabilities
- Create skills taxonomy with parent-child relationships
- Set up proper database indexing for performance
- Include data validation and constraints
- Plan for future data migration strategies" \
    "type:feature,area:backend,area:database,priority:high,complexity:medium" \
    "🔍 AI Resume & Job Parsing"

create_issue \
    "🔄 Background Job Processing" \
    "## Description
Set up Celery with Redis for handling asynchronous AI processing tasks.

## Acceptance Criteria
- [ ] Celery configuration with Redis broker
- [ ] Async task queue for resume parsing
- [ ] Job status tracking and notifications
- [ ] Error handling and retry logic
- [ ] Task monitoring and logging
- [ ] Docker setup for Celery workers

## Estimated Time
3-4 days

## Technical Notes
- Configure Celery with Redis as message broker
- Set up task routing and priority queues
- Implement task result storage and monitoring
- Create health checks for worker processes
- Include task timeout and retry policies
- Set up Flower for task monitoring dashboard" \
    "type:infrastructure,area:backend,priority:high,complexity:medium" \
    "🔍 AI Resume & Job Parsing"

# Milestone 3: Matching Algorithm & Core Features
echo -e "${BLUE}📋 Creating Milestone 3 Issues...${NC}"

create_issue \
    "🎯 AI-Powered Matching Algorithm" \
    "## Description
Develop the core matching algorithm that scores and ranks candidates against job requirements.

## Acceptance Criteria
- [ ] Skill matching with weighted scoring
- [ ] Experience level compatibility
- [ ] Location and remote work preferences
- [ ] Salary range alignment
- [ ] Education requirements matching
- [ ] Machine learning model for continuous improvement
- [ ] A/B testing framework for algorithm optimization

## Estimated Time
10-14 days

## Technical Notes
- Implement weighted scoring algorithm for multiple criteria
- Use machine learning for pattern recognition and optimization
- Create configurable matching parameters
- Include bias detection and mitigation
- Set up A/B testing infrastructure
- Implement real-time scoring updates" \
    "type:feature,area:ai,area:backend,priority:critical,complexity:epic" \
    "🎯 Matching Algorithm & Core Features"

create_issue \
    "🔍 Advanced Search & Filtering" \
    "## Description
Build comprehensive search and filtering system for both recruiters and candidates.

## Acceptance Criteria
- [ ] Full-text search with Elasticsearch integration
- [ ] Multi-criteria filtering (skills, location, experience)
- [ ] Saved search functionality
- [ ] Search result ranking and sorting
- [ ] Real-time search suggestions
- [ ] Search analytics and optimization

## Estimated Time
6-8 days

## Technical Notes
- Integrate Elasticsearch for fast full-text search
- Implement faceted search with multiple filters
- Create search suggestion system with autocomplete
- Set up search result caching for performance
- Include search analytics for optimization
- Implement search result highlighting" \
    "type:feature,area:frontend,area:backend,priority:high,complexity:large" \
    "🎯 Matching Algorithm & Core Features"

create_issue \
    "💼 Job Posting Management" \
    "## Description
Create comprehensive job posting system for recruiters with AI assistance.

## Acceptance Criteria
- [ ] Job posting creation form with AI suggestions
- [ ] Job description optimization recommendations
- [ ] Posting status management (draft, active, closed)
- [ ] Applicant tracking for each job
- [ ] Job posting templates and duplication
- [ ] Bulk job management operations

## Estimated Time
5-7 days

## Technical Notes
- Create rich text editor for job descriptions
- Implement AI-powered job description optimization
- Set up job posting workflow with approval process
- Include job posting analytics and performance tracking
- Create job template system for common roles
- Implement job posting scheduling and automation" \
    "type:feature,area:frontend,area:backend,priority:high,complexity:large" \
    "🎯 Matching Algorithm & Core Features"

create_issue \
    "📧 Notification & Communication System" \
    "## Description
Build real-time notification system and in-app messaging between recruiters and candidates.

## Acceptance Criteria
- [ ] Real-time notifications with WebSockets
- [ ] Email notification system
- [ ] In-app messaging between users
- [ ] Notification preferences management
- [ ] Message history and search
- [ ] File sharing in conversations

## Estimated Time
6-8 days

## Technical Notes
- Use Django Channels for WebSocket support
- Implement email templates with dynamic content
- Create real-time chat interface with message persistence
- Set up notification queuing and delivery tracking
- Include file upload and sharing in messages
- Implement message encryption for privacy" \
    "type:feature,area:backend,area:frontend,priority:high,complexity:large" \
    "🎯 Matching Algorithm & Core Features"

create_issue \
    "📝 Application Management System" \
    "## Description
Create system for managing job applications, candidate shortlisting, and recruitment pipeline.

## Acceptance Criteria
- [ ] One-click application system
- [ ] Application status tracking
- [ ] Recruiter candidate shortlisting
- [ ] Interview scheduling integration
- [ ] Application withdrawal functionality
- [ ] Bulk application management

## Estimated Time
5-7 days

## Technical Notes
- Create application workflow with status transitions
- Implement interview scheduling with calendar integration
- Set up application analytics and reporting
- Include bulk operations for recruiters
- Create application templates and automation
- Implement application scoring and ranking" \
    "type:feature,area:frontend,area:backend,priority:high,complexity:large" \
    "🎯 Matching Algorithm & Core Features"

create_issue \
    "🏆 Candidate Scoring & Ranking" \
    "## Description
Implement detailed scoring system that provides transparency in candidate ranking.

## Acceptance Criteria
- [ ] Detailed score breakdown by criteria
- [ ] Visual score representation
- [ ] Score explanation and reasoning
- [ ] Recruiter feedback integration
- [ ] Score calibration based on hiring outcomes
- [ ] Bias detection and mitigation

## Estimated Time
4-5 days

## Technical Notes
- Create transparent scoring algorithm with explanations
- Implement visual score charts and breakdowns
- Set up feedback collection system for score improvement
- Include bias detection algorithms
- Create score calibration based on hiring success
- Implement score confidence intervals" \
    "type:feature,area:ai,area:backend,priority:medium,complexity:medium" \
    "🎯 Matching Algorithm & Core Features"

# Milestone 4: Analytics & Advanced Features
echo -e "${BLUE}📋 Creating Milestone 4 Issues...${NC}"

create_issue \
    "📊 Recruiter Analytics Dashboard" \
    "## Description
Build comprehensive analytics dashboard for recruiters with insights and metrics.

## Acceptance Criteria
- [ ] Job posting performance metrics
- [ ] Candidate pipeline analytics
- [ ] Time-to-hire tracking
- [ ] Success rate analysis
- [ ] Market insights and benchmarking
- [ ] Exportable reports and data

## Estimated Time
6-8 days

## Technical Notes
- Use Chart.js or D3.js for interactive visualizations
- Implement real-time data aggregation and caching
- Create customizable dashboard widgets
- Set up automated report generation
- Include data export functionality (CSV, PDF)
- Implement dashboard sharing and collaboration" \
    "type:feature,area:frontend,area:backend,priority:medium,complexity:large" \
    "📊 Analytics & Advanced Features"

create_issue \
    "📈 Candidate Career Insights" \
    "## Description
Provide candidates with career insights, skill gap analysis, and job market trends.

## Acceptance Criteria
- [ ] Skill gap identification
- [ ] Career progression recommendations
- [ ] Salary benchmarking
- [ ] Market demand analysis for skills
- [ ] Learning resource recommendations
- [ ] Career path visualization

## Estimated Time
4-6 days

## Technical Notes
- Integrate with external APIs for market data
- Implement AI-powered skill gap analysis
- Create personalized learning recommendations
- Set up career path visualization with interactive charts
- Include salary data from multiple sources
- Implement skill demand forecasting" \
    "type:feature,area:frontend,area:ai,priority:medium,complexity:medium" \
    "📊 Analytics & Advanced Features"

create_issue \
    "🔐 Admin Panel & User Management" \
    "## Description
Create comprehensive admin panel for platform management and user administration.

## Acceptance Criteria
- [ ] User management and moderation
- [ ] Platform analytics and monitoring
- [ ] Content moderation tools
- [ ] System configuration management
- [ ] Audit logs and activity tracking
- [ ] Performance monitoring dashboard

## Estimated Time
5-7 days

## Technical Notes
- Create role-based admin interface
- Implement comprehensive audit logging
- Set up real-time system monitoring
- Include content moderation workflows
- Create admin notification system
- Implement bulk user management operations" \
    "type:feature,area:backend,area:frontend,priority:medium,complexity:large" \
    "📊 Analytics & Advanced Features"

create_issue \
    "💰 Subscription & Payment System" \
    "## Description
Implement subscription plans and payment processing for premium features.

## Acceptance Criteria
- [ ] Stripe payment integration
- [ ] Subscription plan management
- [ ] Usage-based billing
- [ ] Invoice generation and management
- [ ] Payment history and receipts
- [ ] Trial period management

## Estimated Time
6-8 days

## Technical Notes
- Integrate Stripe for secure payment processing
- Implement webhook handling for payment events
- Create subscription plan management system
- Set up usage tracking and billing
- Include invoice generation and email delivery
- Implement trial period with automatic conversion" \
    "type:feature,area:backend,area:frontend,priority:medium,complexity:large" \
    "📊 Analytics & Advanced Features"

create_issue \
    "🌐 API Rate Limiting & Security" \
    "## Description
Implement comprehensive security measures and API protection.

## Acceptance Criteria
- [ ] API rate limiting with Redis
- [ ] Request throttling and quotas
- [ ] SQL injection protection
- [ ] XSS prevention measures
- [ ] Data encryption for sensitive information
- [ ] Security audit logging

## Estimated Time
3-4 days

## Technical Notes
- Use Django REST Framework throttling classes
- Implement Redis-based rate limiting
- Set up comprehensive security headers
- Include input validation and sanitization
- Implement audit logging for security events
- Create security monitoring and alerting" \
    "type:infrastructure,area:backend,priority:high,complexity:medium" \
    "📊 Analytics & Advanced Features"

# Milestone 5: Production & Launch
echo -e "${BLUE}📋 Creating Milestone 5 Issues...${NC}"

create_issue \
    "🐳 Production Deployment Setup" \
    "## Description
Set up production environment with Docker, CI/CD pipeline, and monitoring.

## Acceptance Criteria
- [ ] Docker production configuration
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Production database setup
- [ ] SSL certificate configuration
- [ ] Load balancing and scaling
- [ ] Backup and disaster recovery

## Estimated Time
5-7 days

## Technical Notes
- Use Docker Compose for production deployment
- Set up GitHub Actions for automated testing and deployment
- Configure Nginx as reverse proxy with SSL termination
- Implement database backup and restore procedures
- Set up monitoring with Prometheus and Grafana
- Include health checks and auto-scaling" \
    "type:infrastructure,priority:critical,complexity:large" \
    "🚀 Production & Launch"

create_issue \
    "🧪 Comprehensive Testing Suite" \
    "## Description
Implement full testing coverage including unit, integration, and end-to-end tests.

## Acceptance Criteria
- [ ] Frontend unit tests with Jest/React Testing Library
- [ ] Backend unit tests with Django TestCase
- [ ] API integration tests
- [ ] End-to-end tests with Playwright
- [ ] Performance testing
- [ ] Security testing

## Estimated Time
6-8 days

## Technical Notes
- Achieve >90% code coverage for critical components
- Set up automated testing in CI/CD pipeline
- Implement performance testing with load testing tools
- Include security testing with OWASP ZAP
- Create test data factories and fixtures
- Set up test environment with isolated databases" \
    "type:testing,priority:high,complexity:large" \
    "🚀 Production & Launch"

create_issue \
    "📚 Documentation & User Guides" \
    "## Description
Create comprehensive documentation for users, developers, and administrators.

## Acceptance Criteria
- [ ] User onboarding guides
- [ ] API documentation with Swagger
- [ ] Developer setup instructions
- [ ] Deployment documentation
- [ ] Troubleshooting guides
- [ ] Video tutorials for key features

## Estimated Time
3-4 days

## Technical Notes
- Use Sphinx for technical documentation
- Create interactive API documentation with Swagger UI
- Include video tutorials for complex features
- Set up documentation hosting and versioning
- Create troubleshooting knowledge base
- Include developer contribution guidelines" \
    "type:documentation,priority:medium,complexity:medium" \
    "🚀 Production & Launch"

create_issue \
    "🔍 Performance Optimization" \
    "## Description
Optimize application performance for production load and user experience.

## Acceptance Criteria
- [ ] Frontend bundle optimization
- [ ] Database query optimization
- [ ] Caching strategy implementation
- [ ] Image optimization and CDN
- [ ] API response time optimization
- [ ] Performance monitoring setup

## Estimated Time
4-5 days

## Technical Notes
- Implement code splitting and lazy loading
- Set up Redis caching for database queries
- Optimize database indexes and queries
- Configure CDN for static assets
- Implement API response compression
- Set up performance monitoring with APM tools" \
    "type:improvement,priority:medium,complexity:medium" \
    "🚀 Production & Launch"

create_issue \
    "🎯 Launch Preparation & Marketing" \
    "## Description
Prepare platform for public launch with marketing pages and user acquisition.

## Acceptance Criteria
- [ ] Landing page with feature highlights
- [ ] Pricing page and plan comparison
- [ ] Terms of service and privacy policy
- [ ] Blog setup for content marketing
- [ ] Social media integration
- [ ] Email marketing setup

## Estimated Time
2-3 days

## Technical Notes
- Create responsive landing page with conversion optimization
- Set up blog with SEO optimization
- Implement social media sharing functionality
- Configure email marketing with Mailchimp or similar
- Include analytics tracking for marketing campaigns
- Set up A/B testing for landing page optimization" \
    "type:feature,priority:medium,complexity:small" \
    "🚀 Production & Launch"

echo ""
echo -e "${GREEN}🎉 All issues created successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Summary:${NC}"
echo "- Total issues created: 25"
echo "- Milestone 1 (Foundation): 5 issues"
echo "- Milestone 2 (AI Parsing): 4 issues"
echo "- Milestone 3 (Matching): 6 issues"
echo "- Milestone 4 (Analytics): 5 issues"
echo "- Milestone 5 (Production): 5 issues"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}" 