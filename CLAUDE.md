# CLAUDE.md

## 项目定位

Simple Gemini CLI —— 一个 Python 命令行工具，用于快速测试 Gemini API：发送提示词、Markdown 美化渲染输出、多模型自动切换重试。学习/实验性质的个人项目。

## 怎么跑

```bash
# 一键运行（自动激活 venv，默认提示词「你好」）
./gemini.sh
./gemini.sh -m gemini-2.5-pro -p "问题"   # 指定模型和提示词
./gemini.sh --list-models                 # 列出内置 13 个模型

# 依赖环境（venv 已就绪，重建时）
python3 -m venv venv && source venv/bin/activate
pip install google-genai "httpx[socks]" rich python-dotenv
```

- API 密钥放 `.env` 的 `GEMINI_API_KEY`（模板见 `.env.example`；`.env` 已 gitignore，严禁提交）
- 无端口/无服务，纯 CLI；`python3 check_models.py` 可重测模型可用性并重写 MODELS_STATUS.md

## 技术栈

Python 3.13 · google-genai SDK（v1beta）· httpx（禁代理 `proxy=None`）· rich（Markdown 渲染）· python-dotenv

## 目录与约定

- `test.py` 主程序（13 个模型的优先级列表 + 429 配额自动等待重试）
- `gemini.sh` 推荐入口；`run.sh` 与其完全同功能（历史早期版）
- `check_models.py` 模型可用性检查 → 生成 `MODELS_STATUS.md`（报告注明测试日期）
- `venv/` 已忽略；本仓库无测试套件、无 CI

## 当前状态与下一步

- 2026-01-25 实测：5/13 模型可用，默认 `gemini-2.5-flash-lite`；Gemini 3.0 系列 404
- README 路线图（多轮对话、流式输出、历史记录、图片输入）均未实现
- 模型可用性随 Google 侧变动，引用前先跑 check_models.py 刷新报告
