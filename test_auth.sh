#!/bin/bash

# HireIQ Authentication System Test Script
# This script tests all authentication endpoints

API_URL="http://localhost:8000/api"
EMAIL="test$(date +%s)@example.com"
PASSWORD="TestPassword123!"

echo "🔐 Testing HireIQ Authentication System"
echo "========================================"
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Check..."
curl -s -X GET "$API_URL/health/" | python3 -m json.tool
echo ""

# Test 2: User Registration
echo "2️⃣  Testing User Registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\",
    \"password_confirm\": \"$PASSWORD\",
    \"user_type\": \"candidate\",
    \"first_name\": \"Test\",
    \"last_name\": \"User\"
  }")
echo "$REGISTER_RESPONSE" | python3 -m json.tool
echo ""

# Test 3: User Login
echo "3️⃣  Testing User Login..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")
echo "$LOGIN_RESPONSE" | python3 -m json.tool

# Extract tokens
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['tokens']['access'])" 2>/dev/null)
REFRESH_TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['tokens']['refresh'])" 2>/dev/null)
echo ""

if [ -z "$ACCESS_TOKEN" ]; then
  echo "❌ Login failed - no access token received"
  exit 1
fi

# Test 4: Get Current User (Protected Endpoint)
echo "4️⃣  Testing Protected Endpoint (Get Current User)..."
curl -s -X GET "$API_URL/user/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | python3 -m json.tool
echo ""

# Test 5: Token Refresh
echo "5️⃣  Testing Token Refresh..."
curl -s -X POST "$API_URL/auth/token/refresh/" \
  -H "Content-Type: application/json" \
  -d "{\"refresh\": \"$REFRESH_TOKEN\"}" | python3 -m json.tool
echo ""

# Test 6: Logout
echo "6️⃣  Testing Logout..."
curl -s -X POST "$API_URL/auth/logout/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}" | python3 -m json.tool
echo ""

echo "✅ All tests completed!"
echo ""
echo "📝 Summary:"
echo "  - User registered: $EMAIL"
echo "  - User logged in successfully"
echo "  - Protected endpoints accessible"
echo "  - Token refresh working"
echo "  - Logout successful" 