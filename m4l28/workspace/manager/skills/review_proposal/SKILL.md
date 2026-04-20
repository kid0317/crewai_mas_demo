---
name: review_proposal
type: task
description: 审批复盘提案（Manager 专用）。收到 type=retro_report 邮件时加载此 Skill。按改动深度分档，memory 自动批准（加闸门），skill/agent 转 Human 确认，soul 标记高风险转 Human。
---

# 审批复盘提案

## 触发条件

收到 type=`retro_report` 的邮件（来自某 Agent 的自我复盘产出）

## 流程

1. **读取 proposals JSON 文件**（路径在邮件 content 中）
2. **对每条提案做预审**：
   - evidence 是否充分？（至少 1 条日志 ID）
   - proposed_change 是否合理？（指向具体文件改动，不是"下次注意"）
   - 改动范围是否可控？（不跨越过多文件）
3. **按改动深度分档处理**：

| 档位 | target_file 包含 | 处理方式 |
|------|-----------------|---------|
| 档 1 | `memory.md` | 自动批准（硬闸门：3条/天，超过转档2） |
| 档 2 | `skills/*.md` / `agent.md` | 发给 Human 确认 |
| 档 3 | `soul.md` | 发给 Human 确认 + 标记⚠️高风险 |

4. **Human 批准后** → 发 `retro_approved` 邮件给提案 Agent，附改动清单
5. **Human 拒绝后** → 发 `retro_rejected` 邮件 + 附 review_notes（拒绝原因）

## retro_approved 邮件格式

```json
{
  "type": "retro_approved",
  "subject": "提案已批准，请执行改动",
  "content": {
    "proposal_file": "proposals/pm_retro_2026-04-13.json",
    "approved_indices": [0, 1],
    "changes": [
      {
        "target_file": "skills/product_design/SKILL.md",
        "before_text": "...",
        "after_text": "..."
      }
    ]
  }
}
```

## 约束

- **不自己执行改动** — 只做审批决策，执行由提案 Agent 完成
- **档 1 自动批准有上限** — 同一 Agent 同一天最多自动批准 3 条 memory 改动
- **soul.md 改动必须转 Human** — soul 改错会导致 Agent 所有后续判断偏移
