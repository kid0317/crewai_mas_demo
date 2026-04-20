---
name: team_retrospective
type: task
description: 团队复盘思考框架（Manager 专用）。当你收到 type=team_retro_trigger 的邮件、或被要求"做团队复盘"时加载此 Skill。从聚合视角分析全员数据，发现跨 Agent 问题，级联触发瓶颈 Agent 的自我复盘，发周报给 Human。
---

# 团队复盘

## 你的任务

从全局视角分析所有 Agent 的运行状况，发现自我复盘看不到的跨 Agent 问题。

## 可用工具

通过 bash 调用 `tools/log_query.py`（按需使用，不限顺序）：

```bash
# 全员统计
python3 tools/log_query.py all-agents --days 7

# 单 Agent 任务列表
python3 tools/log_query.py tasks --agent-id <id> --days 7 --sort quality_asc

# 人类纠正记录
python3 tools/log_query.py l1 --days 7 [--keyword "关键词"]
```

## 思考框架（非强制顺序）

1. **谁是瓶颈？** — 对比各 Agent 质量分布
2. **有没有跨 Agent 模式？** — 多个 Agent 犯同类错误 → 可能是模板/共享规范问题
3. **协作接口健康吗？** — 交接失败率、邮件往返次数异常
4. **上周改进生效了吗？** — 对比上周提案落地后的指标变化

## 输出格式

同 self_retrospective 的 JSON 格式，但：
- `target_file` 可以指向任何 Agent 的文件
- 可以触发下级 Agent 的自我复盘（发 retro_trigger 邮件）

写入 `workspace/shared/proposals/manager_team_retro_{date}.json`

## 完成后

1. 如发现瓶颈 Agent → 发 `retro_trigger` 邮件给该 Agent
2. 如有跨 Agent 提案 → 按 review_proposal 流程走 Human 审批
3. 发周报给 Human：type=`weekly_report`，内容包含本周恶化指标 + 瓶颈 Agent + 改进提案 + 上周验证结果

## 约束

- **不读 L3** — L3 是各 Agent 自己的工作域，你只看聚合数据
- **不提 ability_gap 类提案** — 能力差距由 Agent 自己发现
- **不替 Agent 做复盘** — 级联触发后由 Agent 自己完成
