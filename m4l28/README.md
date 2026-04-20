# 第28课：数字员工的自我进化

本课在第27课四步任务链基础上，新增**三层日志系统**和**复盘机制**，让数字团队越用越好。

> **核心教学点**：三层日志（L1/L2/L3）、复盘即 Skill（Agent 用 LLM 推理做分析，脚本只提供数据查询）、五个递进问题的漏斗模型、root_cause 枚举打破复述式反思、三档 HITL 审批

---

## 运行演示前（重要）

每次运行复盘演示前，先执行 seed_logs.py 重新生成模拟数据：

```bash
cd /path/to/crewai_mas_demo/m4l28
python3 seed_logs.py
```

这会：
1. 基于当前时刻重新生成过去 7 天的日志（确保 log_query 能查到数据）
2. 将 PM 工作区文件（agent.md / soul.md / memory.md / product_design SKILL.md）重置到 baseline

> baseline 文件存放在 `baselines/` 目录。即使 workspace 下的文件被复盘流程修改后意外提交，运行 seed_logs.py 即可恢复。

---

## 目录结构

```
m4l28/
├── schemas.py                    # Pydantic 模型（L2LogRecord / RetroOutput / ImprovementProposal）
├── seed_logs.py                  # 预置7天模拟日志 + 重置工作区文件到 baseline
├── baselines/                    # PM 工作区文件的基准版本（seed_logs 重置源）
│   ├── pm_agent.md
│   ├── pm_soul.md
│   ├── pm_memory.md
│   └── pm_product_design_skill.md
├── scheduler.py                  # 极薄 Scheduler（双条件：24h间隔 + 5条最少任务数）
├── hooks/
│   └── l2_task_callback.py       # L2 日志 task_callback 工厂
├── tools/
│   ├── mailbox_ops.py            # 邮箱操作（to=human 自动写 L1）
│   ├── log_ops.py                # 三层日志读写 Python 库
│   ├── log_query.py              # ⚡ 统一日志查询 CLI（Agent 通过 bash 调用）
│   └── proposal_ops.py           # 提案读取 + 分档 + 闸门校验
├── test_m4l28_v8.py              # 端到端测试（14 tests）
├── conftest.py                   # pytest fixtures
└── workspace/
    ├── manager/skills/
    │   ├── team_retrospective/SKILL.md   # 团队复盘思考框架
    │   └── review_proposal/SKILL.md      # 审批流程框架
    ├── pm/
    │   ├── agent.md              # PM 工作规范（含复盘执行流程）
    │   ├── soul.md               # PM 决策偏好
    │   ├── memory.md             # PM 跨session记忆
    │   └── skills/
    │       └── self_retrospective/SKILL.md  # ⚡ 自我复盘思考框架（纯描述，无脚本）
    └── shared/
        ├── mailboxes/            # 邮箱通信
        ├── logs/                 # 三层日志（seed_logs 生成）
        │   ├── l1_human/         # L1：人类纠正（黄金数据）
        │   ├── l2_task/          # L2：任务质量摘要
        │   └── l3_react/         # L3：ReAct 步骤
        └── proposals/            # 复盘产出（RetroOutput JSON）
```

---

## 核心设计：Skill = 思考框架，Script = 数据查询

```
┌─────────────────────────────────────────────────────────────────┐
│  self_retrospective/SKILL.md（思考框架）                         │
│  - 五个递进问题                                                  │
│  - root_cause 枚举约束                                           │
│  - 输出格式要求                                                  │
└─────────────────���─────┬─────────────────────────────────────────┘
                        │ Agent 按需调用
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  tools/log_query.py（统一 CLI）                                  │
│  - stats:       整体统计                                         │
│  - tasks:       任务列表（可排序/筛选）                           │
│  - steps:       ReAct 步骤回放                                   │
│  - l1:          人类纠正记录                                     │
│  - all-agents:  全员统计                                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │ Agent 推理分析
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  RetroOutput JSON（结构化产出）                                  │
│  - retrospective_report: 发现 + 证据                            │
│  - improvement_proposals: root_cause + before/after_text        │
└───────────────────────┬─────────────────────────────────────────┘
                        │ Manager 审批 → PM 执行
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  文件变更（agent.md / soul.md / memory.md / skills/*.md）       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 快速开始

```bash
# 1. 生成模拟数据
python3 seed_logs.py

# 2. 验证日志查询
python3 tools/log_query.py stats --agent-id pm --days 7
python3 tools/log_query.py tasks --agent-id pm --sort quality_asc --limit 3
python3 tools/log_query.py l1 --days 7 --keyword "移动端"

# 3. 运行测试
python3 -m pytest test_m4l28_v8.py -v
```

---

## 端到端流程

```
seed_logs.py（生成7天模拟数据）
    ↓
Scheduler.tick()（24h间隔 + ≥5条任务 → 发 retro_trigger）
    ↓
PM 加载 self_retrospective Skill
    ↓
PM 调用 log_query CLI 查数据 → LLM 推理分析
    ↓
PM 产出 RetroOutput JSON（report + proposals）
    ↓
PM 发 retro_report 邮件给 Manager
    ↓
Manager 加载 review_proposal Skill → 分档审批
    ↓
Manager 发 retro_approved 邮件给 PM
    ↓
PM 执行 before_text → after_text 替换
    ↓
PM 发 retro_applied 确认邮件
```

---

## 三层日志

| 层级 | 写入方式 | 保留策略 | 用途 |
|------|---------|---------|------|
| L1 | `send_mail(to="human")` AOP自动写入 | 永久 | 人类纠正（黄金数据） |
| L2 | `task_callback` hook 自动写入 | 90天 | 任务质量定位 |
| L3 | 复用 session 日志 + task_id 索引 | 30天 | ReAct 步骤回放 |

---

## 改进提案 Schema（v8）

```python
class ImprovementProposal(BaseModel):
    root_cause:           Literal["sop_gap", "prompt_ambiguity", "ability_gap", "integration_issue"]
    target_file:          str           # 要改的文件（agent.md/soul.md/memory.md/skills/*.md）
    current_behavior:     str           # 当前行为
    proposed_change:      str           # 改动描述
    before_text:          str           # 定位锚点（文件中的原文）
    after_text:           str           # 替换后的文本
    expected_improvement: str           # 预期指标变化
    evidence:             list[str]     # 支撑日志 ID（不允许为空）

class RetroOutput(BaseModel):
    retrospective_report:   RetroReport
    improvement_proposals:  list[ImprovementProposal]   # 最多3条
```
