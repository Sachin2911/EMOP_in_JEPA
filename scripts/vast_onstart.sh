#!/usr/bin/env bash
# Paste into Vast template / instance "On-start script" (SSH or Jupyter mode).
# Requires account env vars: WANDB_API_KEY, GITHUB_TOKEN (optional), HF_TOKEN (optional).
# Optional: REPO_URL, REPO_DIR, GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL

set -euo pipefail

# Make Vast account env vars visible in later SSH sessions
env >> /etc/environment

REPO_URL="${REPO_URL:-https://github.com/YOUR_USER/EMOP_in_JEPA.git}"
REPO_DIR="${REPO_DIR:-/workspace/EMOP_in_JEPA}"
mkdir -p "$(dirname "${REPO_DIR}")"

if [[ -d "${REPO_DIR}/.git" ]]; then
  echo "[onstart] pulling ${REPO_DIR}"
  git -C "${REPO_DIR}" pull --ff-only || git -C "${REPO_DIR}" pull
else
  echo "[onstart] cloning ${REPO_URL} -> ${REPO_DIR}"
  git clone "${REPO_URL}" "${REPO_DIR}"
fi

bash "${REPO_DIR}/scripts/vast_setup.sh"
