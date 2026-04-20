---
name: self_retrospective
type: task
description: 自我复盘思考框架。当你收到 type=retro_trigger 的邮件、或被要求"反思本周工作"/"自我复盘"时加载此 Skill。用 log_query CLI 查数据，用 LLM 推理做分析，产出结构化复盘报告和改进提案。
---

# 自我复盘

## 你的任务

分析过去 7 天的工作记录，找出系统性问题，产出改进方案。

## 可用工具

通过 bash 调用 `tools/log_query.py`，支持以下查询（按需使用，不限顺序）：

```bash
# 整体统计
python3 tools/log_query.py stats --agent-id {agent_id} --days 7

# 任务列表（可排序）
python3 tools/log_query.py tasks --agent-id {agent_id} --days 7 --sort quality_asc --limit 5

# 某任务的 ReAct 步骤回放
python3 tools/log_query.py steps --task-id <TASK_ID> --sessions-dir workspace/{agent_id}/sessions [--only-failed]

# 人类纠正记录
python3 tools/log_query.py l1 --days 7 [--keyword "关键词"]
```

## 思考框架（非强制顺序，按需使用）

你的分析目标是回答五个递进问题：

1. **哪些任务做得差？** — 从统计和任务列表中发现模式
2. **差在哪一步？** — 下钻具体任务的执行步骤
3. **人类怎么看？** — L1 纠正记录提供独立视角
4. **根因是什么类型？** — 必须从枚举中选择（见下方）
5. **应该改哪个文件的哪一段？** — 精确到可执行的 before/after 改动

## root_cause 枚举（必选其一，禁止自由文本）

| 枚举值 | 含义 | 对应改动对象 |
|--------|------|-------------|
| `sop_gap` | 流程/SOP 缺步骤 | agent.md 或 skills/*.md |
| `prompt_ambiguity` | 提示词/soul 指令模糊 | soul.md |
| `ability_gap` | 知识/经验不足 | memory.md |
| `integration_issue` | 与其他 Agent 协作问题 | agent.md 协作部分 |

## 输出格式（必须严格遵守）

产出一份 JSON，写入 `workspace/shared/proposals/{agent_id}_retro_{date}.json`：

```json
{
  "retrospective_report": {
    "agent_id": "{agent_id}",
    "period": "2026-04-07 ~ 2026-04-13",
    "summary": "一句话总结本周主要问题",
    "findings": [
      {
        "pattern": "描述发现的模式",
        "evidence_task_ids": ["t001", "t003", "t006"],
        "l1_corroboration": "人类纠正记录是否验证了这个发现"
      }
    ]
  },
  "improvement_proposals": [
    {
      "root_cause": "sop_gap",
      "target_file": "skills/product_design/SKILL.md",
      "current_behavior": "当前行为描述",
      "proposed_change": "具体改动描述（自然语言）",
      "before_text": "定位锚点：要改的那段原文",
      "after_text": "改后的完整文本",
      "expected_improvement": "预期指标变化",
      "evidence": ["t001", "t003"]
    }
  ]
}
```

## 约束

- **evidence 不允许为空** — 每条提案必须有日志 ID 支撑
- **一次复盘最多 3 条提案** — 聚焦最重要的改进
- **target_file 只允许改自己的文件**：agent.md / soul.md / memory.md / skills/*.md
- **不要自己执行改动** — 你只产出方案，由 Manager 审批后你再执行
- **样本不足时跳过** — task_count < 5 直接报告"样本不足，跳过复盘"
- **禁止复述式反思** — "下次要注意 XX"不是根因分析，必须指向具体文件改动

## 完成后

发邮件给 Manager：
- type: `retro_report`
- subject: "自我复盘完成，{N}条提案待审阅"
- content: proposals 文件路径

⚠️ **不直接发 Human**。所有对外通信必须经过 Manager。
