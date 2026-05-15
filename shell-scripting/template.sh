#!/usr/bin/env bash

# ==========================================================================================
# Script Name: demo.sh
# Description: line 1
               line 2
# Author: [your name/team]
# Date: 2026-05-15
# Usage: ./demo.sh
# ==========================================================================================

set -euo pipefail

# Get the absolute path of the directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_CONFIG="${SCRIPT_DIR}/setting.txt"

# Structure logging
log_info() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') | [INFO] | $1"
}
log_success() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') | [SUCCESS] | $1"
}
log_warn() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') | [WARN] | $1"
}
log_error() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') | [ERROR] | $1" >&2
}

# Automatic cleanup on EXIT
cleanup() {
    echo "Cleaning up temporary files..."
    # command...
}
trap cleanup EXIT ERR INT TERM

main() {
    # Check if the correct number of argument was passed
    if [[ "$#" -ne 3 ]]; then
        log_error "Invalid argument."
        log_error "Usage: $0 <> <> <>"
        exit 1
    fi

    # command ...

    # Usage of logs
    log_info "info"
    log_success "success"
    log_warn "warning"
    log_error "error"

    # Best practice
    # 1. Bad: cd" $targe"t-dir -> Good: cd "$target-dir"
    # 2. use local for function variable
    # 3. Add ShellCheck to your Script: `shellcheck *.sh`
    # 4. Add idempotency to logics
    # 5. Add logs structure
}

# Pass all incoming script argument directly into the main function
main "$@"
