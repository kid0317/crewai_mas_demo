# 第26课示例代码：任务链与信息传递——数字员工的协作协议

本课演示 Manager 和 PM 通过**邮箱（mailbox）**协作完成一条完整任务链。
与第25课（两个角色各自独立）不同，本课由编排器（`m4l26_run.py`）驱动四步流程，角色间通过共享工作区传递消息。

---

## 核心教学点

| 概念 | 说明 |
|------|------|
| **共享工作区** | Manager 在步骤0调用 `create_workspace` 建立协作基础设施 |
| **邮箱协议** | 角色通过 `mailboxes/manager.json` / `pm.json` 传递结构化消息 |
| **三态状态机** | 消息状态：`unread → in_progress → done`，防止崩溃重复消费 |
| **编排器负责确认** | 每步 Crew 成功后，由 `run.py` 调用 `mark_done_all_in_progress`，而非 Agent 自己改状态 |

---

## 目录结构

```
m4l26/
├── m4l26_run.py              # 编排器（主入口，四步流程）
├── m4l26_manager.py          # Manager 角色（ManagerAssignCrew / ManagerReviewCrew）
├── m4l26_pm.py               # PM 角色（PMExecuteCrew）
├── m4l26_mailbox/
│   ├── mailbox_ops.py        # 邮箱操作（send/read/mark_done）
│   ├── workspace_ops.py      # create_workspace 实现
│   └── mailbox_tools.py      # CrewAI Tool 封装
├── sandbox-docker-compose.yaml
├── demo_input/
│   └── project_requirement.md  # XiaoPaw 宠物健康记录需求
└── workspace/
    ├── manager/              # Manager 个人区（sessions、review_result.md）
    ├── pm/                   # PM 个人区（sessions、草稿）
    └── shared/               # 共享工作区
        ├── mailboxes/        # manager.json / pm.json（邮箱）
        ├── needs/            # requirements.md（需求文档）
        ├── design/           # product_spec.md（产品文档，PM输出）
        └── WORKSPACE_RULES.md
```

---

## 运行步骤

### 第一步：启动沙盒

```bash
cd /path/to/crewai_mas_demo/m4l26

# Manager 和 PM 按需独立启动（端口不同）
docker compose -f sandbox-docker-compose.yaml --profile manager up -d  # 端口 8025
docker compose -f sandbox-docker-compose.yaml --profile pm up -d       # 端口 8026

# 或一次性全启动
docker compose -f sandbox-docker-compose.yaml --profile manager --profile pm up -d
```

| 角色 | 沙盒端口 | 个人区挂载 | 共享区挂载 |
|------|---------|-----------|-----------|
| Manager | 8025 | `workspace/manager` | `workspace/shared` |
| PM | 8026 | `workspace/pm` | `workspace/shared` |

### 第二步：运行演示

```bash
cd /path/to/crewai_mas_demo
python m4l26/m4l26_run.py
```

---

## 四步流程说明

```
步骤0  Manager   create_workspace（建立共享工作区）
  ↓
步骤1  Manager   读需求 → 发 task_assign → pm.json
  ↓
步骤2  PM        读邮件 → 写 product_spec.md → 发 task_done → manager.json
  ↓  （编排器确认：PM 邮箱 in_progress → done）
步骤3  Manager   读邮件 → 验收文档 → 写 review_result.md
     （编排器确认：Manager 邮箱 in_progress → done）
```

**编排器会在每步之间做结构检查**，任何一步失败会打印警告并终止，不会继续执行后续步骤。

---

## 运行测试（不需要沙盒）

```bash
cd /path/to/crewai_mas_demo

# 单元测试（邮箱、workspace 操作）
python -m pytest m4l26/test_m4l26.py -v

# 集成测试（四步全流程，需要沙盒和 LLM）
python -m pytest m4l26/test_m4l26_integration.py -v
```

---

## 常见问题

**Q：沙盒端口 8025/8026 被占用？**
```bash
docker compose -f sandbox-docker-compose.yaml --profile manager --profile pm down
docker compose -f sandbox-docker-compose.yaml --profile manager --profile pm up -d
```

**Q：想清除状态重新跑？**
```bash
# 清邮箱（重置三态）
echo "[]" > workspace/shared/mailboxes/manager.json
echo "[]" > workspace/shared/mailboxes/pm.json
# 清输出文件
rm -f workspace/shared/design/product_spec.md
rm -f workspace/manager/review_result.md
# 清 session
rm -f workspace/manager/sessions/*.json workspace/manager/sessions/*.jsonl
rm -f workspace/pm/sessions/*.json workspace/pm/sessions/*.jsonl
```

**Q：报 `ModuleNotFoundError`？**
确认从 `crewai_mas_demo/` 目录运行，不要在 `m4l26/` 内直接运行。
