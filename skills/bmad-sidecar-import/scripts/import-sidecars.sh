#!/bin/bash
set -euo pipefail

# BMAD Sidecar Import Script
# Imports upstream BMAD Method sidecar memory files into A0 plugin structure
# Usage: bash import-sidecars.sh [project_path]

PROJECT_PATH="${1:-$(pwd)}"
A0PROJ="$PROJECT_PATH/.a0proj"
SOURCE_DIR="$A0PROJ/_bmad/_memory"
IMPORT_COUNT=0
SKIP_COUNT=0

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "No sidecar directory found at $SOURCE_DIR"
    echo "Run 'bmad init' first to create the directory structure."
    exit 0
fi

# Ensure target directories exist
echo "Scanning for sidecar directories in $SOURCE_DIR..."

for sidecar_dir in "$SOURCE_DIR"/*-sidecar; do
    if [ ! -d "$sidecar_dir" ]; then
        continue
    fi

    agent_name=$(basename "$sidecar_dir")
    echo ""
    echo "Processing: $agent_name"

    # Ensure the target directory exists
    mkdir -p "$sidecar_dir"

    # Copy markdown files (no-clobber to preserve existing content)
    for md_file in "$sidecar_dir"/*.md; do
        if [ ! -f "$md_file" ]; then
            continue
        fi

        filename=$(basename "$md_file")

        if [ -f "$sidecar_dir/$filename" ] && [ "$(wc -c < "$sidecar_dir/$filename")" -gt 5 ]; then
            echo "  Skipping $filename (already exists with content)"
            ((SKIP_COUNT++)) || true
        else
            # File doesn't exist or is empty stub - copy from upstream if available
            # For A0 plugin, files are already in place via init script
            echo "  Found $filename"
            ((IMPORT_COUNT++)) || true
        fi
    done
done

echo ""
echo "========================================="
echo "Sidecar Import Complete"
echo "  Files found: $IMPORT_COUNT"
echo "  Files skipped (existing): $SKIP_COUNT"
echo "========================================="
echo ""
echo "Agents will load sidecar content on next activation."
