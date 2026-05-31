#!/usr/bin/env bash
# Create private GitHub repo and push initial commit using token from .env
# Usage: ./scripts/push_to_github.sh

set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -f .env ]]; then
  echo "ERROR: .env not found. Copy .env.example to .env and fill in values."
  exit 1
fi

# Load .env (export each KEY=VALUE)
set -a
# shellcheck disable=SC1091
source .env
set +a

: "${GITHUB_TOKEN:?GITHUB_TOKEN missing in .env}"
: "${GITHUB_USER:?GITHUB_USER missing in .env}"
: "${GITHUB_REPO:?GITHUB_REPO missing in .env}"

REPO_URL="https://api.github.com/user/repos"
PUSH_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

echo "==> Checking if repo ${GITHUB_USER}/${GITHUB_REPO} exists..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}")

if [[ "$HTTP_CODE" == "404" ]]; then
  echo "==> Creating private repo ${GITHUB_USER}/${GITHUB_REPO}..."
  curl -fsS -X POST "$REPO_URL" \
    -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    -d "{\"name\":\"${GITHUB_REPO}\",\"private\":true,\"description\":\"Record decisions as they happen. Recall them 3 months later.\"}" \
    > /dev/null
  echo "    Created."
elif [[ "$HTTP_CODE" == "200" ]]; then
  echo "    Already exists. Skipping create."
else
  echo "ERROR: unexpected HTTP code $HTTP_CODE while checking repo."
  exit 1
fi

echo "==> Ensuring main branch..."
git branch -M main

echo "==> Setting remote..."
if git remote | grep -q '^origin$'; then
  git remote set-url origin "$PUSH_URL"
else
  git remote add origin "$PUSH_URL"
fi

echo "==> Pushing..."
git push -u origin main

# Sanitize remote URL after push (don't leave token in .git/config)
git remote set-url origin "https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

echo ""
echo "Done."
echo "Repo: https://github.com/${GITHUB_USER}/${GITHUB_REPO}"
echo ""
echo "Next: invite your friend as collaborator at:"
echo "  https://github.com/${GITHUB_USER}/${GITHUB_REPO}/settings/access"
