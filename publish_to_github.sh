#!/bin/bash
# publish_to_github.sh
# Run this once to create the GitHub repo and push everything.
#
# Usage:
#   chmod +x publish_to_github.sh
#   ./publish_to_github.sh YOUR_GITHUB_TOKEN
#
# Get a token at: https://github.com/settings/tokens
# Needs scopes: repo (full)

set -e

TOKEN=$1
GITHUB_USER="isaacattuah"       # ← your GitHub username
REPO_NAME="uscis-rfe-i765"
DESCRIPTION="AI skill for responding to USCIS I-765 RFE (OPT/CPT/STEM/DACA). Works with Claude and Gemini CLI."

if [ -z "$TOKEN" ]; then
  echo "Usage: ./publish_to_github.sh YOUR_GITHUB_TOKEN"
  echo "Get one at: https://github.com/settings/tokens (needs 'repo' scope)"
  exit 1
fi

echo "🚀 Creating GitHub repo: $GITHUB_USER/$REPO_NAME ..."

# Create the repo via GitHub API
curl -s -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$DESCRIPTION\",
    \"public\": true,
    \"has_issues\": true,
    \"has_wiki\": false,
    \"auto_init\": false
  }" | python3 -c "
import json,sys
r=json.load(sys.stdin)
if 'html_url' in r:
    print('✅ Repo created:', r['html_url'])
elif r.get('message'):
    print('❌ Error:', r['message'])
    sys.exit(1)
"

# Rename branch to main, add remote, push
git branch -m master main
git remote add origin "https://$TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main

echo ""
echo "✅ All done!"
echo "   🔗 https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Next: go to the repo and create a Release to attach the .skill file."
