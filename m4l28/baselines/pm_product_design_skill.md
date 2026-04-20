---
name: product_design
type: reference
description: 产品文档设计规范，包含产品文档结构、写作要求和验收标准。
---

# 产品文档设计规范

本规范指导你如何撰写高质量的产品规格文档（product_spec.md）。

## 文档结构

产品规格文档（`/mnt/shared/design/product_spec.md`）必须包含以下章节：

```markdown
# 产品规格文档

## 项目背景
简要描述项目来源和业务价值（3-5句话）

## 目标用户
- 主要用户画像（1-2个）
- 核心使用场景

## 核心功能
| 功能模块 | 功能描述 | 优先级 |
|---------|---------|--------|
| 模块1   | ...     | P0/P1  |

## 用户故事
- 作为 [用户]，我希望 [功能]，以便 [价值]

## 验收标准
明确列出每个功能的验收条件（可验证的）

## 范围外（Out of Scope）
本期不做的内容，避免需求蔓延
```

## 写作原则

1. **需求来源**：从 `/mnt/shared/needs/requirements.md` 读取原始需求
2. **结构化优先**：表格 > 列表 > 段落
3. **可验证**：每个功能点必须有明确的验收标准
4. **简洁**：总长度控制在 500-1000 字

## 输出路径

产品文档写入：`/mnt/shared/design/product_spec.md`

完成后，通过 `mailbox` Skill 向 Manager 发送 `task_done` 邮件，邮件内容只写文档路径：
> 产品文档已写入 /mnt/shared/design/product_spec.md，请验收
