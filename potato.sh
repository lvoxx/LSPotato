#!/usr/bin/env bash
set -euo pipefail

# ================================
#  User Configurable Variables
# ================================
ADDON_NAME="LSPotato"
SOURCE_DIR="src"
DIST_DIR="dist"
DEFAULT_BLENDER_VERSION="4.3"

# Initialize paths
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)/"
BLENDER_BASE="$HOME/.config/blender"
OPERATION="help"

# Get current Git branch
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Parse command-line arguments
if [[ $# -ge 1 ]]; then
  OPERATION="$1"
fi
if [[ $# -ge 2 ]]; then
  BLENDER_VERSION="$2"
else
  BLENDER_VERSION="$DEFAULT_BLENDER_VERSION"
fi

# Calculate full paths
FULL_SOURCE="${ROOT_DIR}${SOURCE_DIR}"
FULL_DIST="${ROOT_DIR}${DIST_DIR}"
ADDON_INSTALL_DIR="${BLENDER_BASE}/${BLENDER_VERSION}/scripts/addons"

# Verify source directory exists
if [[ ! -d "$FULL_SOURCE" ]]; then
  echo "[ERROR]: Source directory not found at $FULL_SOURCE"
  exit 1
fi

# ================================
#  Functions
# ================================

help() {
  echo
  echo "============================================="
  echo "  $ADDON_NAME Blender Addon - Build Script Help"
  echo "============================================="
  echo "Location: $ROOT_DIR"
  echo "Branch: $GIT_BRANCH"
  echo
  echo "Usage: ./potato.sh [command] [blender_version]"
  echo
  echo "Commands:"
  echo "  package     - Build addon zip package"
  echo "  install     - Install to specified Blender version"
  echo "  uninstall   - Remove from Blender addons directory"
  echo "  clean       - Clean build artifacts"
  echo "  test        - Run code checks (requires flake8)"
  echo "  dev         - Clean + package + install"
  echo "  reload      - Uninstall + dev"
  echo
  echo "Blender Version:"
  echo "  Default: $DEFAULT_BLENDER_VERSION"
  echo "  Current: $BLENDER_VERSION"
  echo "  Install path: $ADDON_INSTALL_DIR"
  echo
  echo "Examples:"
  echo "  ./potato.sh install"
  echo "  ./potato.sh install 3.6"
  echo "  ./potato.sh uninstall 4.0"
  echo "==============================================="
}

clean() {
  echo
  echo "[INFO] Cleaning build artifacts..."
  rm -rf "$FULL_DIST"
  find "$FULL_SOURCE" -name "*.pyc" -delete
  echo "[SUCCESS] Clean dist done."
}

package() {
  clean
  echo
  echo "[INFO] Packaging addon [$GIT_BRANCH]..."
  mkdir -p "$FULL_DIST"

  ZIP_PATH="${FULL_DIST}/${ADDON_NAME}_${GIT_BRANCH}.zip"

  python3 package.py "$FULL_SOURCE" "$ZIP_PATH"

  if [[ ! -f "$ZIP_PATH" ]]; then
    echo "[ERROR] Failed to create zip package"
    exit 1
  fi
  echo "[INFO] Created: $ZIP_PATH"
}

install() {
  package
  echo
  echo "[INFO] Installing [$GIT_BRANCH] to Blender $BLENDER_VERSION..."

  if [[ ! -d "$ADDON_INSTALL_DIR" ]]; then
    echo "[ERROR] Blender $BLENDER_VERSION not found at: $ADDON_INSTALL_DIR"
    echo "[ERROR] Please verify Blender version and installation"
    exit 1
  fi

  mkdir -p "$ADDON_INSTALL_DIR/$ADDON_NAME"
  rsync -a --delete "$FULL_SOURCE/" "$ADDON_INSTALL_DIR/$ADDON_NAME/"

  echo "[INFO] Installed to: $ADDON_INSTALL_DIR/$ADDON_NAME"
  echo "[INFO] Branch: $GIT_BRANCH"
  echo "[INFO] Please restart Blender to activate the addon"
}

uninstall() {
  echo
  echo "[SUCCESS] Uninstalling from Blender $BLENDER_VERSION..."
  ADDON_PATH="$ADDON_INSTALL_DIR/$ADDON_NAME"

  if [[ -d "$ADDON_PATH" ]]; then
    rm -rf "$ADDON_PATH"
    echo "[INFO] Removed: $ADDON_PATH"
  else
    echo "[ERROR] Addon not found: $ADDON_PATH"
  fi
}

test_code() {
  echo
  echo "Running code checks..."
  flake8 "$FULL_SOURCE" || {
    echo "[ERROR] Code checks failed"
    exit 1
  }
  echo "[SUCCESS] All tests passed!"
}

dev() {
  clean
  install
  echo
  echo "[SUCCESS] Development cycle complete for [$GIT_BRANCH]!"
}

reload() {
  uninstall
  install
  echo
  echo "[SUCCESS] Development cycle complete for [$GIT_BRANCH]!"
  echo "!! Happy Cherrying !!"
  echo
}

# ================================
#  Main command router
# ================================
case "$OPERATION" in
  help) help ;;
  clean) clean ;;
  package) package ;;
  install) install ;;
  uninstall) uninstall ;;
  test) test_code ;;
  dev) dev ;;
  reload) reload ;;
  *) help ;;
esac
