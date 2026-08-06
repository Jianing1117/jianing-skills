#!/usr/bin/env bash
# deploy.sh — Deploy a slide deck to Netlify (primary) or Vercel (fallback)
#
# Usage:
#   bash scripts/deploy.sh <path-to-slide-folder-or-html>
#
# Examples:
#   bash scripts/deploy.sh ./my-pitch-deck/
#   bash scripts/deploy.sh ./presentation.html
#
# What this does:
#   1. Tries Netlify first (better for users in China)
#   2. Falls back to Vercel if Netlify fails
#   3. Deploys the slide deck to a public URL
#   4. Prints the live URL
#
# The deployed URL is permanent and works on any device (mobile, tablet, desktop).
set -euo pipefail

# ─── Colors ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${CYAN}ℹ${NC} $*"; }
ok()    { echo -e "${GREEN}✓${NC} $*"; }
warn()  { echo -e "${YELLOW}⚠${NC} $*"; }
err()   { echo -e "${RED}✗${NC} $*" >&2; }

# ─── Input validation ─────────────────────────────────────

if [[ $# -lt 1 ]]; then
    err "Usage: bash scripts/deploy.sh <path-to-slide-folder-or-html>"
    err ""
    err "Examples:"
    err "  bash scripts/deploy.sh ./my-pitch-deck/"
    err "  bash scripts/deploy.sh ./presentation.html"
    exit 1
fi

INPUT="$1"

# If input is a single HTML file, create a temp directory with it as index.html
if [[ -f "$INPUT" && "$INPUT" == *.html ]]; then
    DEPLOY_DIR=$(mktemp -d)
    cp "$INPUT" "$DEPLOY_DIR/index.html"
    PARENT_DIR=$(dirname "$INPUT")

    # Parse the HTML for local file references (src="...", url('...'), href="...")
    # and copy any referenced local files into the deploy directory
    grep -oE '(src|href|url\()["'"'"']?[^"'"'"'>)]+' "$INPUT" 2>/dev/null | \
        sed "s/^src=//; s/^href=//; s/^url(//; s/[\"']//g" | \
        grep -v '^http' | grep -v '^data:' | grep -v '^#' | grep -v '^/' | \
        sort -u | while read -r ref; do
            # Resolve the reference relative to the HTML file's directory
            SOURCE_FILE="$PARENT_DIR/$ref"
            if [[ -e "$SOURCE_FILE" ]]; then
                # Preserve directory structure for nested paths (e.g., assets/img.png)
                TARGET_DIR="$DEPLOY_DIR/$(dirname "$ref")"
                mkdir -p "$TARGET_DIR"
                cp -r "$SOURCE_FILE" "$TARGET_DIR/"
            fi
        done

    # Also copy any assets/ folder if it exists (common convention)
    if [[ -d "$PARENT_DIR/assets" ]]; then
        cp -r "$PARENT_DIR/assets" "$DEPLOY_DIR/assets" 2>/dev/null || true
    fi

    CLEANUP_TEMP=true
    info "Single HTML file detected — preparing for deployment..."
elif [[ -d "$INPUT" ]]; then
    # Verify the folder has an index.html
    if [[ ! -f "$INPUT/index.html" ]]; then
        err "Folder '$INPUT' does not contain an index.html file."
        err "Make sure your presentation folder has an index.html."
        exit 1
    fi
    DEPLOY_DIR="$INPUT"
    CLEANUP_TEMP=false
else
    err "'$INPUT' is not a valid HTML file or directory."
    exit 1
fi

# ─── Check for Node.js ─────────────────────────────────────

if ! command -v npx &>/dev/null; then
    err "Node.js is required but not installed."
    err ""
    err "Install Node.js:"
    err "  macOS:   brew install node"
    err "  or visit https://nodejs.org and download the installer"
    exit 1
fi

# ─── Helper function: Deploy via Netlify ──────────────────

deploy_netlify() {
    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║      Deploy Slides to Netlify         ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    info "Checking Netlify CLI..."

    # Check if netlify is available
    if command -v netlify &>/dev/null; then
        NETLIFY_CMD="netlify"
        ok "Netlify CLI found"
    elif npx --yes netlify-cli --version &>/dev/null 2>&1; then
        NETLIFY_CMD="npx --yes netlify-cli"
        ok "Netlify CLI available via npx"
    else
        info "Installing Netlify CLI..."
        npm install -g netlify-cli
        NETLIFY_CMD="netlify"
        ok "Netlify CLI installed"
    fi

    # Check login status
    echo ""
    info "Checking Netlify login status..."

    if ! $NETLIFY_CMD status &>/dev/null 2>&1; then
        echo ""
        warn "You're not logged in to Netlify yet."
        echo ""
        echo -e "${BOLD}To log in, run this command and follow the prompts:${NC}"
        echo ""
        echo "    netlify login"
        echo ""
        echo "If you don't have a Netlify account yet:"
        echo "  1. Go to https://app.netlify.com/signup"
        echo "  2. Sign up with GitHub, GitLab, email, or any method"
        echo "  3. Come back here and run: netlify login"
        echo "  4. Then re-run this deploy script"
        echo ""

        # Try interactive login
        echo -e "${YELLOW}Attempting interactive login now...${NC}"
        echo ""
        $NETLIFY_CMD login || {
            err "Login failed. Please run 'netlify login' manually and try again."
            return 1
        }
        echo ""
        ok "Logged in to Netlify!"
    fi

    NETLIFY_USER=$($NETLIFY_CMD status 2>/dev/null | head -1 || echo "unknown")
    ok "Account: $NETLIFY_USER"

    # Deploy
    echo ""
    info "Deploying slides to Netlify..."
    echo ""

    DEPLOY_OUTPUT=$($NETLIFY_CMD deploy --dir="$DEPLOY_DIR" --prod 2>&1) || {
        err "Netlify deployment failed:"
        echo "$DEPLOY_OUTPUT"
        return 1
    }

    # Extract the URL from output
    DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -o 'https://[^ ]*\.netlify\.app' | tail -1)

    if [[ -z "$DEPLOY_URL" ]]; then
        # Try alternative extraction
        DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -oE 'https://[a-zA-Z0-9-]+\.netlify\.app' | tail -1)
    fi

    echo ""
    echo -e "${BOLD}════════════════════════════════════════${NC}"
    ok "Slides deployed to Netlify!"
    echo ""
    echo -e "  ${BOLD}Live URL:${NC}  $DEPLOY_URL"
    echo ""
    echo "  This URL works on any device — phones, tablets, laptops."
    echo "  Share it via Slack, email, text, or anywhere."
    echo ""
    echo -e "  ${CYAN}Tip:${NC} To take it down later, visit https://app.netlify.com"
    echo -e "       and delete the site."
    echo -e "${BOLD}════════════════════════════════════════${NC}"
    echo ""

    return 0
}

# ─── Helper function: Deploy via Vercel ───────────────────

deploy_vercel() {
    echo ""
    echo -e "${BOLD}╔══════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║       Deploy Slides to Vercel         ║${NC}"
    echo -e "${BOLD}╚══════════════════════════════════════╝${NC}"
    echo ""

    info "Checking Vercel CLI..."

    # Check if vercel is available
    if command -v vercel &>/dev/null; then
        VERCEL_CMD="vercel"
        ok "Vercel CLI found"
    elif npx --yes vercel --version &>/dev/null 2>&1; then
        VERCEL_CMD="npx --yes vercel"
        ok "Vercel CLI available via npx"
    else
        info "Installing Vercel CLI..."
        npm install -g vercel
        VERCEL_CMD="vercel"
        ok "Vercel CLI installed"
    fi

    # Check login status
    echo ""
    info "Checking Vercel login status..."

    if ! $VERCEL_CMD whoami &>/dev/null 2>&1; then
        echo ""
        warn "You're not logged in to Vercel yet."
        echo ""
        echo -e "${BOLD}To log in, run this command and follow the prompts:${NC}"
        echo ""
        echo "    vercel login"
        echo ""
        echo "If you don't have a Vercel account yet:"
        echo "  1. Go to https://vercel.com/signup"
        echo "  2. Sign up with GitHub, GitLab, email, or any method"
        echo "  3. Come back here and run: vercel login"
        echo "  4. Then re-run this deploy script"
        echo ""

        # Try interactive login
        echo -e "${YELLOW}Attempting interactive login now...${NC}"
        echo ""
        $VERCEL_CMD login || {
            err "Login failed. Please run 'vercel login' manually and try again."
            return 1
        }
        echo ""
        ok "Logged in to Vercel!"
    fi

    VERCEL_USER=$($VERCEL_CMD whoami 2>/dev/null || echo "unknown")
    ok "Logged in as: $VERCEL_USER"

    # Deploy
    echo ""
    info "Deploying slides to Vercel..."
    echo ""

    DECK_NAME=$(basename "$DEPLOY_DIR")
    if [[ "$CLEANUP_TEMP" == "true" ]]; then
        DECK_NAME=$(basename "$INPUT" .html)
    fi

    # Sanitize project name
    DECK_NAME=$(echo "$DECK_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9._-]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-100)

    # Rename deploy directory for Vercel
    if [[ "$CLEANUP_TEMP" == "true" ]]; then
        RENAMED_DIR="$(dirname "$DEPLOY_DIR")/$DECK_NAME"
        mv "$DEPLOY_DIR" "$RENAMED_DIR"
        DEPLOY_DIR="$RENAMED_DIR"
    fi

    DEPLOY_OUTPUT=$($VERCEL_CMD deploy "$DEPLOY_DIR" --yes --prod 2>&1) || {
        err "Vercel deployment failed:"
        echo "$DEPLOY_OUTPUT"
        return 1
    }

    # Extract the URL from output
    DEPLOY_URL=$(echo "$DEPLOY_OUTPUT" | grep -o 'https://[^ ]*' | tail -1)

    echo ""
    echo -e "${BOLD}════════════════════════════════════════${NC}"
    ok "Slides deployed to Vercel!"
    echo ""
    echo -e "  ${BOLD}Live URL:${NC}  $DEPLOY_URL"
    echo ""
    echo "  This URL works on any device — phones, tablets, laptops."
    echo "  Share it via Slack, email, text, or anywhere."
    echo ""
    echo -e "  ${CYAN}Tip:${NC} To take it down later, visit https://vercel.com/dashboard"
    echo -e "       and delete the project '${DECK_NAME}'."
    echo -e "${BOLD}════════════════════════════════════════${NC}"
    echo ""

    return 0
}

# ─── Main deployment logic ────────────────────────────────

# Try Netlify first (better for users in China)
if deploy_netlify; then
    # Cleanup temp directory on success
    if [[ "$CLEANUP_TEMP" == "true" ]]; then
        rm -rf "$DEPLOY_DIR"
    fi
    exit 0
fi

# Netlify failed, try Vercel as fallback
warn "Netlify deployment failed. Trying Vercel as fallback..."
echo ""

if deploy_vercel; then
    # Cleanup temp directory on success
    if [[ "$CLEANUP_TEMP" == "true" ]]; then
        rm -rf "$DEPLOY_DIR"
    fi
    exit 0
fi

# Both failed
err "Both Netlify and Vercel deployment failed."
err ""
err "Please try deploying manually:"
err "  1. Netlify: Drag and drop your folder to https://app.netlify.com/drop"
err "  2. Vercel: Run 'npx vercel' in your project directory"

# Cleanup
if [[ "$CLEANUP_TEMP" == "true" ]]; then
    rm -rf "$DEPLOY_DIR"
fi

exit 1
