#!/bin/bash
# Gemini API 快捷运行脚本（简写版）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate" && python3 "$SCRIPT_DIR/test.py" "$@"
