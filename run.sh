#!/bin/bash
# Gemini API 运行脚本 - 自动激活虚拟环境并运行

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 激活虚拟环境并运行
source "$SCRIPT_DIR/venv/bin/activate" && python3 "$SCRIPT_DIR/test.py" "$@"
