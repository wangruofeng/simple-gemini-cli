# Simple Gemini CLI

> 一个简单优雅的 Gemini API 命令行测试工具，支持 Markdown 美化渲染、多模型切换、一键运行

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-API-orange.svg)

## ✨ 特性

- 🚀 **一键运行** - 无需每次激活虚拟环境，直接运行
- 🎨 **Markdown 渲染** - 支持代码高亮、表格、列表等格式美化
- 🔄 **智能重试** - 自动切换模型，支持配额限制处理
- 📦 **多模型支持** - 支持 Gemini 2.0/1.5/2.5/3.0 系列共 13 个模型
- 🔒 **安全配置** - 使用 .env 文件管理 API 密钥，不硬编码
- ⚙️ **灵活配置** - 支持命令行参数和代码调用

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/wangruofeng/simple-gemini-cli.git
cd simple-gemini-cli
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install google-genai "httpx[socks]" rich python-dotenv
```

### 3. 配置 API 密钥

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
GEMINI_API_KEY=your-api-key-here
```

从 [Google AI Studio](https://ai.google.dev/) 获取免费的 API 密钥。

### 4. 开始使用

```bash
# 一键运行（默认提示词：你好）
./gemini.sh

# 自定义问题
./gemini.sh -p "解释什么是量子计算"

# 指定模型
./gemini.sh -m gemini-2.5-pro -p "写一首诗"

# 查看所有可用模型
./gemini.sh --list-models
```

---

## 💡 使用示例

### 基础问答

```bash
./gemini.sh -p "Python 是什么？"
```

**输出效果**：
```
✓ 成功使用模型: gemini-2.5-flash-lite

╭──────────────────────────────────── 回答 ────────────────────────────────────╮
│                                                                              │
│  Python 是一种高级编程语言，以其简洁易读的语法而闻名...                       │
│                                                                              │
│  **特点**：                                                                  │
│   • 易于学习和使用                                                           │
│   • 丰富的库和框架                                                           │
│   • 跨平台支持                                                               │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 代码生成（带语法高亮）

```bash
./gemini.sh -p "写一个Python快速排序"
```

**特点**：
- ✅ Python 代码带语法高亮
- ✅ 注释清晰可读
- ✅ 自动格式化显示

---

## 📋 命令行参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--model` | `-m` | 指定使用的模型 |
| `--prompt` | `-p` | 指定提示词 |
| `--list-models` | `-l` | 列出所有可用模型 |
| `--help` | `-h` | 显示帮助信息 |

### 使用示例

```bash
# 查看帮助
./gemini.sh --help

# 使用默认模型
./gemini.sh

# 指定单个模型
./gemini.sh --model gemini-2.5-flash

# 自定义提示词
./gemini.sh --prompt "用简单的语言解释量子计算"

# 组合使用
./gemini.sh -m gemini-2.5-flash -p "写一首关于春天的诗"
```

---

## 📦 可用模型

### Gemini 2.5 系列（默认推荐）⭐

| 模型 | 状态 | 说明 |
|------|------|------|
| `gemini-2.5-flash-lite` | ✅ 可用 | **默认模型**，推荐日常使用 |
| `gemini-2.5-flash` | ✅ 可用 | 快速模型，性能和速度的平衡 |
| `gemini-2.5-pro` | ✅ 可用 | 专业模型，复杂推理和编码 |

### Gemini 2.0 系列

| 模型 | 状态 | 说明 |
|------|------|------|
| `gemini-2.0-flash-exp` | ✅ 可用 | 实验性快速模型 |
| `gemini-2.0-flash` | ✅ 可用 | 快速模型（⚠️ 将于 2026-03-31 停用） |

### Gemini 3.0 系列（最新）

| 模型 | 状态 | 说明 |
|------|------|------|
| `gemini-3-pro` | ❌ 404 | 多模态理解的最强模型 |
| `gemini-3-flash` | ❌ 404 | 快速响应模型 |

### Gemini 1.5 系列

| 模型 | 状态 | 说明 |
|------|------|------|
| `gemini-1.5-pro` | ❌ 404 | 专业模型（当前不可用） |
| `gemini-1.5-flash` | ❌ 404 | 轻量级快速模型（当前不可用） |

**注意**：部分模型（如 Gemini 3.0 系列）可能需要特殊 API 权限或尚未完全公开。

📊 **查看完整的模型状态报告**: [MODELS_STATUS.md](MODELS_STATUS.md)

---

## 🎯 代码调用示例

```python
from google import genai
from dotenv import load_dotenv
import httpx
import os

# 加载环境变量
load_dotenv()

# 创建客户端
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options=httpx.Client(proxy=None)
)

# 生成内容
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="你好"
)

print(response.text)
```

---

## 🔧 配置

### API 密钥配置

项目使用 `.env` 文件管理环境变量（推荐方式）：

1. 复制示例文件：`cp .env.example .env`
2. 编辑 `.env` 文件，设置您的 API 密钥
3. 从 [Google AI Studio](https://ai.google.dev/) 获取 API 密钥

**安全提示**：`.env` 文件已添加到 `.gitignore`，不会被提交到版本控制。

### 代理设置

如果需要使用代理，可以修改 `test.py` 中的客户端配置：

```python
client = genai.Client(
    api_key=api_key,
    http_options=httpx.Client(proxy="http://proxy.example.com:8080")
)
```

---

## 📁 项目结构

```
simple-gemini-cli/
├── test.py              # 主程序文件
├── gemini.sh            # 快捷运行脚本（推荐）
├── run.sh              # 运行脚本
├── check_models.py      # 模型可用性检查工具
├── .env.example        # 环境变量示例文件
├── MODELS_STATUS.md     # 模型状态测试报告
├── venv/               # Python 虚拟环境（已忽略）
├── .gitignore          # Git 忽略文件
├── LICENSE             # MIT 开源许可证
└── README.md           # 本文档
```

---

## 🛠️ 模型测试

### 检查所有模型的可用性

项目提供了一个工具来检查所有 Gemini 模型的可用性：

```bash
# 激活虚拟环境后运行
source venv/bin/activate
python3 check_models.py
```

该工具会：
- 测试所有模型是否可用
- 生成美观的控制台表格输出
- 自动生成详细的 Markdown 报告（`MODELS_STATUS.md`）

查看测试结果：
```bash
cat MODELS_STATUS.md
```

---

## 🔥 技术栈

### 核心库
- **google-genai** - Google Gemini API 官方 SDK
- **httpx[socks]** - HTTP 客户端，支持 SOCKS 代理
- **rich** - 终端美化输出库，提供 Markdown 渲染功能
- **python-dotenv** - 从 .env 文件加载环境变量

### Markdown 渲染效果

本工具使用 [Rich](https://rich.readthedocs.io/) 库进行美化输出，支持：

- ✅ **代码高亮** - Python、JavaScript、Bash 等多种语言
- ✅ **格式化列表** - 有序/无序列表美化显示
- ✅ **表格渲染** - Markdown 表格格式化
- ✅ **标题样式** - 不同级别标题的颜色和粗细
- ✅ **链接高亮** - 自动识别并高亮显示链接

---

## 📚 故障排除

### 连接错误

**错误**：`Server disconnected without sending a response`

**解决方案**：
1. 检查网络连接
2. 配置代理（见代理设置部分）
3. 确认 API 密钥有效

### 配额超限

**错误**：`429 API quota exceeded`

**解决方案**：
1. 等待一段时间后重试
2. 检查配额使用情况：https://ai.dev/rate-limit
3. 尝试使用其他模型

### 模型不可用

**错误**：`404 Model not found`

**解决方案**：
1. 使用 `./gemini.sh --list-models` 查看可用模型
2. 查看模型状态报告：[MODELS_STATUS.md](MODELS_STATUS.md)

### 环境变量未设置

**错误**：`ValueError: ❌ 错误：未找到 GEMINI_API_KEY 环境变量`

**解决方案**：
1. 复制示例文件：`cp .env.example .env`
2. 编辑 `.env` 文件，添加您的 API 密钥
3. 从 [Google AI Studio](https://ai.google.dev/) 获取密钥

---

## ❓ 常见问题

### 1. 默认提示词是什么？

默认提示词是 `你好`，你可以通过 `--prompt` 或 `-p` 参数自定义。

### 2. 如何禁用 Markdown 渲染？

编辑 `test.py`，注释掉 Rich 相关代码，改用普通 `print()` 输出。

### 3. 支持哪些 Gemini 模型？

支持 Gemini 2.0/1.5/2.5/3.0 系列的多个公开模型。详见：[MODELS_STATUS.md](MODELS_STATUS.md)

### 4. 如何设置 API 密钥？

推荐使用 `.env` 文件：
```bash
cp .env.example .env
# 然后编辑 .env 文件，设置 GEMINI_API_KEY
```

---

## 🎯 适用场景

- 📝 **快速测试** - 快速测试 Gemini API 的效果
- 🎓 **学习研究** - 了解不同模型的输出差异
- 🔍 **调试开发** - 开发 Gemini 应用时的调试工具
- 📊 **模型对比** - 比较不同模型的表现
- 💬 **命令行聊天** - 在终端中与 AI 对话

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) - 详见 LICENSE 文件

---

## 🔗 相关链接

- [Gemini API 官方文档](https://ai.google.dev/gemini-api/docs)
- [模型列表](https://ai.google.dev/gemini-api/docs/models)
- [配额限制](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Rich 文档](https://rich.readthedocs.io/)
- [Google AI Studio](https://ai.google.dev/)

---

## 🌟 项目亮点

- 📦 开箱即用的一键脚本
- 🎨 美观的 Markdown 渲染
- 🔒 安全的环境变量管理
- 📊 完整的模型状态报告
- 📚 详尽的使用文档
- 🚀 简单优雅的设计

---

## 📈 路线图

- [ ] 支持多轮对话
- [ ] 支持流式输出
- [ ] 添加历史记录功能
- [ ] 支持图片输入（多模态）
- [ ] 添加配置文件支持

---

**如果这个项目对你有帮助，请给个 Star 支持一下！** ⭐

---

**安全提示**：
- ✅ `.env` 文件已添加到 `.gitignore`，不会被提交到 Git
- ✅ 请勿将包含真实 API 密钥的 `.env` 文件分享给他人
- ✅ 定期更换 API 密钥以保证安全
- ✅ 使用 `.env.example` 作为模板分享项目配置
