#!/usr/bin/env python3
"""检查所有 Gemini 模型的可用性"""

from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import httpx
from rich.console import Console
from rich.table import Table

# 加载 .env 文件
load_dotenv()

console = Console()

# API 密钥
api_key = os.environ.get("GEMINI_API_KEY")

# 如果未设置 API 密钥，提示用户
if not api_key:
    console.print("[bold red]❌ 错误：未找到 GEMINI_API_KEY 环境变量[/bold red]")
    console.print("\n请按以下步骤设置：")
    console.print("1. 复制 .env.example 为 .env: [cyan]cp .env.example .env[/cyan]")
    console.print("2. 在 .env 文件中设置您的 API 密钥")
    console.print("3. 从 https://ai.google.dev/ 获取 API 密钥")
    exit(1)

# 创建客户端
client = genai.Client(
    api_key=api_key,
    http_options=httpx.Client(proxy=None)
)

# 所有要测试的模型
models_to_test = [
    ('gemini-2.5-flash-lite', 'Gemini 2.5', '文本生成', '默认模型'),
    ('gemini-3-flash', 'Gemini 3.0', '文本生成', '快速模型'),
    ('gemini-3-pro', 'Gemini 3.0', '文本生成', '专业模型'),
    ('gemini-2.5-flash', 'Gemini 2.5', '文本生成', '快速模型'),
    ('gemini-2.5-pro', 'Gemini 2.5', '文本生成', '专业模型'),
    ('gemini-3-pro-image', 'Gemini 3.0', '多模态', '图像生成'),
    ('gemini-2.5-flash-preview-image', 'Gemini 2.5', '多模态', '图像预览'),
    ('gemini-2.0-flash-exp', 'Gemini 2.0', '文本生成', '实验性'),
    ('gemini-1.5-pro', 'Gemini 1.5', '文本生成', '稳定版'),
    ('gemini-2.0-flash', 'Gemini 2.0', '文本生成', '即将停用'),
    ('gemini-1.5-flash', 'Gemini 1.5', '文本生成', '轻量级'),
    ('gemini-1.5-pro-002', 'Gemini 1.5', '文本生成', 'Pro 迭代'),
    ('gemini-1.5-flash-8b', 'Gemini 1.5', '文本生成', '超轻量级'),
]

def check_model(model_name):
    """检查单个模型的可用性"""
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Hi"
        )
        return True, "✅ 可用"
    except errors.ClientError as e:
        if e.code == 404:
            return False, "❌ 404 不可用"
        elif e.code == 429:
            return False, "⚠️ 配额超限"
        else:
            return False, f"❌ 错误 {e.code}"
    except Exception as e:
        return False, f"❌ {str(e)[:50]}"

# 创建表格
table = Table(title="Gemini API 模型可用性测试")
table.add_column("模型名称", style="cyan", no_wrap=True)
table.add_column("系列", style="magenta")
table.add_column("类型", style="green")
table.add_column("说明", style="yellow")
table.add_column("状态", style="bold")

console.print("\n[bold]正在测试所有模型的可用性...[/bold]\n")

results = []

for model_name, series, model_type, description in models_to_test:
    console.print(f"测试 {model_name}...", end=" ")
    is_available, status = check_model(model_name)
    console.print(status)

    results.append({
        'model': model_name,
        'series': series,
        'type': model_type,
        'description': description,
        'status': status,
        'available': is_available
    })

    # 添加到表格
    status_style = "green" if is_available else "red"
    table.add_row(
        model_name,
        series,
        model_type,
        description,
        f"[{status_style}]{status}[/{status_style}]"
    )

console.print("\n")
console.print(table)

# 生成 Markdown 表格
md_table = """# Gemini API 模型可用性测试报告

## 测试时间

自动生成于模型测试

## 模型状态总览

| 模型名称 | 系列 | 类型 | 说明 | 状态 |
|---------|------|------|------|------|
"""

for r in results:
    status_emoji = "✅" if r['available'] else "❌"
    md_table += f"| {r['model']} | {r['series']} | {r['type']} | {r['description']} | {status_emoji} {r['status']} |\n"

# 统计信息
available_count = sum(1 for r in results if r['available'])
total_count = len(results)

md_table += f"""

## 统计信息

- **总模型数**: {total_count}
- **可用模型数**: {available_count}
- **不可用模型数**: {total_count - available_count}
- **可用率**: {available_count/total_count*100:.1f}%

## 可用模型列表

"""

for r in results:
    if r['available']:
        md_table += f"- ✅ `{r['model']}` - {r['series']} {r['type']} {r['description']}\n"

md_table += "\n## 不可用模型列表\n\n"

for r in results:
    if not r['available']:
        md_table += f"- ❌ `{r['model']}` - {r['status']}\n"

md_table += """

## 注意事项

1. 部分最新模型（如 Gemini 3.0 系列）可能需要特殊 API 权限或尚未完全公开
2. 404 错误通常表示模型不存在或当前 API 密钥无法访问
3. 配额超限（429）表示请求过于频繁，需要等待后重试
4. 默认使用 `gemini-2.5-flash-lite`，它是目前最稳定且快速的选项

## 建议

- **日常使用**: 推荐使用 `gemini-2.5-flash-lite`（默认）
- **复杂任务**: 推荐使用 `gemini-2.5-pro` 或 `gemini-1.5-pro`
- **快速响应**: 推荐使用 `gemini-1.5-flash` 或 `gemini-1.5-flash-8b`
"""

# 保存到文件
with open('MODELS_STATUS.md', 'w', encoding='utf-8') as f:
    f.write(md_table)

console.print("\n[bold green]✓ Markdown 表格已保存到 MODELS_STATUS.md[/bold green]\n")
