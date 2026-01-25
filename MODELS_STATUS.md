# Gemini API 模型可用性测试报告

## 测试信息

- **测试日期**: 2026年1月25日
- **测试工具**: check_models.py
- **API 版本**: v1beta

---

## 模型状态总览

| 模型名称 | 系列 | 类型 | 说明 | 状态 |
|---------|------|------|------|------|
| gemini-2.5-flash-lite | Gemini 2.5 | 文本生成 | 默认模型 | ✅ 可用 |
| gemini-3-flash | Gemini 3.0 | 文本生成 | 快速模型 | ❌ 404 不可用 |
| gemini-3-pro | Gemini 3.0 | 文本生成 | 专业模型 | ❌ 404 不可用 |
| gemini-2.5-flash | Gemini 2.5 | 文本生成 | 快速模型 | ✅ 可用 |
| gemini-2.5-pro | Gemini 2.5 | 文本生成 | 专业模型 | ✅ 可用 |
| gemini-3-pro-image | Gemini 3.0 | 多模态 | 图像生成 | ❌ 404 不可用 |
| gemini-2.5-flash-preview-image | Gemini 2.5 | 多模态 | 图像预览 | ❌ 404 不可用 |
| gemini-2.0-flash-exp | Gemini 2.0 | 文本生成 | 实验性 | ✅ 可用 |
| gemini-1.5-pro | Gemini 1.5 | 文本生成 | 稳定版 | ❌ 404 不可用 |
| gemini-2.0-flash | Gemini 2.0 | 文本生成 | 即将停用 | ✅ 可用 |
| gemini-1.5-flash | Gemini 1.5 | 文本生成 | 轻量级 | ❌ 404 不可用 |
| gemini-1.5-pro-002 | Gemini 1.5 | 文本生成 | Pro 迭代 | ❌ 404 不可用 |
| gemini-1.5-flash-8b | Gemini 1.5 | 文本生成 | 超轻量级 | ❌ 404 不可用 |

---

## 统计信息

- **总模型数**: 13
- **可用模型数**: 5
- **不可用模型数**: 8
- **可用率**: 38.5%

---

## ✅ 可用模型列表

### 推荐使用

1. **gemini-2.5-flash-lite** ⭐ 默认
   - Gemini 2.5 文本生成
   - 轻量级快速模型
   - **推荐日常使用**

2. **gemini-2.5-flash**
   - Gemini 2.5 文本生成
   - 快速模型
   - 性能和速度的平衡

3. **gemini-2.5-pro**
   - Gemini 2.5 文本生成
   - 专业模型
   - 适合复杂任务

4. **gemini-2.0-flash-exp**
   - Gemini 2.0 文本生成
   - 实验性快速模型

5. **gemini-2.0-flash**
   - Gemini 2.0 文本生成
   - ⚠️ 将于 2026-03-31 停用

---

## ❌ 不可用模型列表

### Gemini 3.0 系列（需要特殊权限）

- **gemini-3-flash** - 404 不可用
- **gemini-3-pro** - 404 不可用
- **gemini-3-pro-image** - 404 不可用

这些模型可能需要特殊 API 权限或尚未完全公开。

### Gemini 1.5 系列

- **gemini-1.5-pro** - 404 不可用
- **gemini-1.5-flash** - 404 不可用
- **gemini-1.5-pro-002** - 404 不可用
- **gemini-1.5-flash-8b** - 404 不可用

### 多模态模型

- **gemini-2.5-flash-preview-image** - 404 不可用

---

## 📝 使用建议

### 日常使用

```bash
# 默认使用 gemini-2.5-flash-lite（推荐）
./gemini.sh -p "你的问题"
```

### 复杂任务

```bash
# 使用 gemini-2.5-pro 处理复杂任务
./gemini.sh -m gemini-2.5-pro -p "复杂的问题"
```

### 快速响应

```bash
# 使用 gemini-2.5-flash 获取快速响应
./gemini.sh -m gemini-2.5-flash -p "简单问题"
```

---

## ⚠️ 注意事项

1. **API 权限**: 部分最新模型（如 Gemini 3.0 系列）可能需要特殊 API 权限
2. **404 错误**: 通常表示模型不存在或当前 API 密钥无法访问
3. **配额限制**: 429 错误表示请求过于频繁，需要等待后重试
4. **区域限制**: 某些模型可能有区域限制
5. **默认模型**: 推荐使用 `gemini-2.5-flash-lite`，它是目前最稳定且快速的选项

---

## 🔧 如何重新测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行模型测试工具
python3 check_models.py

# 查看生成的报告
cat MODELS_STATUS.md
```

测试工具会：
- 自动测试所有模型
- 生成美观的控制台表格
- 自动更新本报告文件

---

## 📊 模型系列对比

### Gemini 2.5 vs 2.0 vs 1.5

| 特性 | 2.5 系列 | 2.0 系列 | 1.5 系列 |
|------|---------|---------|---------|
| 可用性 | 高 (3/3) | 中 (2/2) | 低 (0/4) |
| 性能 | 最强 | 强 | 中等 |
| 速度 | 快 | 快 | 较快 |
| 稳定性 | 高 | 中 | 低 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ |

### 推荐优先级

1. **首选**: gemini-2.5-flash-lite（默认）
2. **复杂任务**: gemini-2.5-pro
3. **快速响应**: gemini-2.5-flash
4. **实验性**: gemini-2.0-flash-exp

---

## 🔗 相关资源

- [Gemini API 官方文档](https://ai.google.dev/gemini-api/docs)
- [模型列表](https://ai.google.dev/gemini-api/docs/models)
- [配额限制](https://ai.google.dev/gemini-api/docs/rate-limits)
- [API 密钥获取](https://ai.google.dev/)

---

**更新日期**: 2026-01-25
**测试环境**: macOS Python 3.13.0
