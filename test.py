from google import genai
from google.genai import errors
import os
import time
import httpx
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

# 加载 .env 文件
load_dotenv()

# 从环境变量获取API密钥
api_key = os.environ.get("GEMINI_API_KEY")

# 如果未设置 API 密钥，提示用户
if not api_key:
    raise ValueError(
        "❌ 错误：未找到 GEMINI_API_KEY 环境变量\n"
        "请按以下步骤设置：\n"
        "1. 复制 .env.example 为 .env: cp .env.example .env\n"
        "2. 在 .env 文件中设置您的 API 密钥\n"
        "3. 从 https://ai.google.dev/ 获取 API 密钥"
    )

# 创建客户端（禁用代理）
client = genai.Client(
    api_key=api_key,
    http_options=httpx.Client(proxy=None)
)

# ============================================================================
# Gemini API 模型列表（按优先级排序，如果第一个失败则尝试下一个）
# ============================================================================
# 详细模型列表和说明请参考：https://ai.google.dev/gemini-api/docs/models
#
# Gemini 3.0 系列（最新最强）
# --------------------------
# - gemini-3-pro: 多模态理解的最强模型（最新）
# - gemini-3-flash: 快速响应模型，平衡性能和速度
#
# Gemini 2.5 系列（先进）
# --------------------------
# - gemini-2.5-pro: Google 最先进的 AI 模型，复杂推理和编码
# - gemini-2.5-flash: 快速模型，性能和速度的平衡
# - gemini-2.5-flash-lite: 轻量级快速模型（默认，推荐日常使用）
#
# 多模态生成模型
# --------------------------
# - gemini-3-pro-image: 图像生成和理解模型
# - gemini-2.5-flash-preview-image: 图像生成预览模型
#
# Gemini 2.0 系列（实验性/快速）
# --------------------------
# - gemini-2.0-flash-exp: 实验性快速模型
# - gemini-2.0-flash: 快速响应模型（⚠️ 将于 2026-03-31 停用）
#
# Gemini 1.5 系列（稳定版）
# --------------------------
# - gemini-1.5-flash: 轻量级快速模型，适合简单任务
# - gemini-1.5-flash-8b: 8B 参数的超轻量级模型，速度最快
# - gemini-1.5-pro: 专业版模型，更强的推理能力
# - gemini-1.5-pro-002: Pro 版本的特定迭代
#
# 其他专用模型
# --------------------------
# - imagen-3.0-generate-001: 图像生成
# - text-embedding-004: 文本嵌入（⚠️ 将于 2026-01-14 弃用）
#
# 重要提示：
# 1. 免费版 API 可能无法访问所有模型
# 2. 部分模型有区域限制
# 3. 默认使用 gemini-2.5-flash-lite 作为稳定且快速的选择
# ============================================================================

models = [
    'gemini-2.5-flash-lite',         # 轻量级快速模型（默认，推荐）
    'gemini-3-flash',                # Gemini 3 快速模型
    'gemini-3-pro',                  # Gemini 3 专业模型（最新最强）
    'gemini-2.5-flash',              # Gemini 2.5 快速模型
    'gemini-2.5-pro',                # Gemini 2.5 专业模型
    'gemini-3-pro-image',            # 多模态图像生成模型
    'gemini-2.5-flash-preview-image', # 多模态图像预览模型
    'gemini-2.0-flash-exp',          # 实验性快速模型
    'gemini-1.5-pro',                # 稳定的专业模型
    'gemini-2.0-flash',              # 快速模型（⚠️ 即将停用）
    'gemini-1.5-flash',              # 轻量级快速模型
    'gemini-1.5-pro-002',            # Pro 版本迭代
    'gemini-1.5-flash-8b',           # 超轻量级模型
]

def generate_with_retry(prompt, model=None, custom_models=None, max_retries=3):
    """
    带重试机制的生成函数

    Args:
        prompt: 提示词
        model: 指定单个模型（如果指定，只使用该模型）
        custom_models: 自定义模型列表（如果指定，使用该列表而非默认列表）
        max_retries: 每个模型的最大重试次数

    Returns:
        (response, model): 响应对象和使用的模型名
    """
    # 确定要使用的模型列表
    if model:
        # 如果指定了单个模型，只使用该模型
        model_list = [model]
        print(f"使用指定模型: {model}")
    elif custom_models:
        # 使用自定义模型列表
        model_list = custom_models
        print(f"使用自定义模型列表: {', '.join(model_list)}")
    else:
        # 使用默认模型列表
        model_list = models

    for model in model_list:
        print(f"尝试使用模型: {model}")
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response, model
            except errors.ClientError as e:
                if e.code == 429:  # 配额超限
                    error_msg = str(e)
                    # 尝试提取等待时间
                    if 'retry in' in error_msg.lower():
                        # 提取等待时间（秒）
                        try:
                            wait_time = float(error_msg.split('retry in ')[1].split('s')[0])
                            print(f"配额超限，等待 {wait_time:.1f} 秒后重试...")
                            time.sleep(wait_time + 1)  # 多等1秒确保安全
                        except:
                            wait_time = 60  # 默认等待60秒
                            print(f"配额超限，等待 {wait_time} 秒后重试...")
                            time.sleep(wait_time)
                    else:
                        print(f"配额超限，等待 60 秒后重试...")
                        time.sleep(60)
                    
                    if attempt < max_retries - 1:
                        print(f"重试 {attempt + 1}/{max_retries}")
                        continue
                    else:
                        print(f"模型 {model} 重试 {max_retries} 次后仍失败，尝试下一个模型...")
                        break
                else:
                    # 其他错误，直接抛出
                    raise
        print(f"模型 {model} 不可用，尝试下一个模型...")
    
    raise Exception("所有模型都不可用，请检查您的 API 配额或稍后再试")


def main():
    """主函数，支持命令行参数"""
    parser = argparse.ArgumentParser(
        description='Gemini API 文本生成工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  # 使用默认模型列表
  python3 test.py

  # 指定单个模型
  python3 test.py --model gemini-1.5-pro

  # 指定提示词
  python3 test.py --prompt "解释什么是人工智能"

  # 指定模型和提示词
  python3 test.py --model gemini-2.0-flash-exp --prompt "写一首诗"

  # 查看可用模型列表
  python3 test.py --list-models
        """
    )

    parser.add_argument(
        '--model', '-m',
        type=str,
        help='指定使用的模型（例如: gemini-1.5-pro, gemini-2.0-flash-exp）'
    )

    parser.add_argument(
        '--prompt', '-p',
        type=str,
        default='你好',
        help='要发送的提示词（默认: 你好）'
    )

    parser.add_argument(
        '--list-models', '-l',
        action='store_true',
        help='列出所有可用的模型'
    )

    args = parser.parse_args()

    # 创建 Rich Console 对象用于美化输出
    console = Console()

    # 如果要求列出模型
    if args.list_models:
        console.print(Panel.fit(
            "[bold cyan]可用的 Gemini API 模型列表：[/bold cyan]",
            border_style="cyan"
        ))
        for i, m in enumerate(models, 1):
            console.print(f"{i}. [green]{m}[/green]")
        console.print("\n更多模型信息请访问：https://ai.google.dev/gemini-api/docs/models")
        return

    # 生成文本
    try:
        if args.model:
            console.print(f"[dim]指定模型: {args.model}[/dim]")
            response, used_model = generate_with_retry(args.prompt, model=args.model)
        else:
            console.print("[dim]使用默认模型列表[/dim]")
            response, used_model = generate_with_retry(args.prompt)

        # 使用 Rich 渲染 Markdown 输出
        console.print(f"\n[bold green]✓ 成功使用模型: {used_model}[/bold green]\n")

        # 将响应文本渲染为 Markdown
        markdown_response = Markdown(response.text)
        console.print(Panel(
            markdown_response,
            title="[bold]回答[/bold]",
            border_style="green",
            padding=(1, 2)
        ))

    except errors.ClientError as e:
        if e.code == 429:
            print("\n❌ 错误：API 配额已耗尽")
            print("\n可能的原因：")
            print("1. 免费层配额已用完（每分钟/每天的请求数或 token 数超限）")
            print("2. 使用的模型配额已用完")
            print("\n解决方案：")
            print("1. 等待一段时间后重试（通常需要等待几分钟到几小时）")
            print("2. 检查您的配额使用情况：https://ai.dev/rate-limit")
            print("3. 查看配额限制文档：https://ai.google.dev/gemini-api/docs/rate-limits")
            print("4. 考虑升级到付费计划以获得更高配额")
            print(f"\n错误详情：{e}")
        else:
            print(f"\n❌ 发生错误：{e}")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")


if __name__ == "__main__":
    main()
