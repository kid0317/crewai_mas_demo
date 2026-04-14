# 第27课示例代码：Human as 甲方——人工介入的三个工程节点

本课在第26课四步任务链基础上增加**两个人工确认节点**。
Manager 和 PM 之间的协作机制不变，区别在于：编排器（`m4l27_run.py`）在关键决策点主动暂停，等待人类确认后再继续。

---

## 核心教学点

| 概念 | 说明 |
|------|------|
| **单一接口原则** | `human.json` 只由 `run.py`（以 manager 身份）写入，LLM Agent 不直接接触人类 |
| **编排器控制时机** | 何时打扰人由 `run.py` 决定，不由 LLM 自行判断 |
| **wait_for_human()** | FileLock 读 `human.json`，命令行 `input()` 等待用户确认，y/n 控制流程走向 |
| **步骤1新增** | `RequirementsDiscoveryCrew`：Manager 先做需求澄清，再拆解任务（相比第26课多了这一步） |

---

## 目录结构

```
m4l27/
├── m4l27_run.py              # 编排器（主入口，4步 + 2个确认节点）
├── m4l27_manager.py          # Manager 三个 Crew（需求澄清 / 任务分配 / 验收）
├── m4l27_pm.py               # PM Crew（读邮件 → 写产品文档 → 通知）
├── tools/
│   └── mailbox_ops.py        # send_mail 等操作（含 human.json 写入）
├── sandbox-docker-compose.yaml
└── workspace/
    ├── manager/              # Manager 个人区（sessions、review_result.md）
    ├── pm/                   # PM 个人区（sessions）
    └── shared/               # 共享工作区
        ├── mailboxes/        # manager.json / pm.json / human.json
        ├── needs/            # requirements.md（需求澄清后写入）
        ├── design/           # product_spec.md（PM输出）
        └── sop/              # 产品设计SOP（Manager读取后按步骤分配任务）
```

---

## 运行步骤

### 第一步：启动沙盒

第27课的两个沙盒**同时启动**（`docker-compose.yaml` 无 profile 分组）：

```bash
cd /path/to/crewai_mas_demo/m4l27
docker compose -f sandbox-docker-compose.yaml up -d
```

| 角色 | 沙盒端口 | 个人区挂载 | 共享区挂载 |
|------|---------|-----------|-----------|
| Manager | 8027 | `workspace/manager` | `workspace/shared` |
| PM | 8028 | `workspace/pm` | `workspace/shared` |

### 第二步：运行演示

```bash
cd /path/to/crewai_mas_demo
python m4l27/m4l27_run.py
```

启动后会先提示输入需求：
```
请告诉 Manager 你要做什么：
```
输入后流程自动推进，**遇到确认节点时暂停等待 y/n 输入**。

---

## 完整流程说明

```
步骤1  Manager   需求澄清（RequirementsDiscoveryCrew）→ 写 requirements.md
  ↓
⏸️ 确认节点1  run.py 写 human.json(needs_confirm)
              → 终端提示用户打开 needs/requirements.md 确认
              → 输入 y 继续 / n 终止
  ↓
步骤2  Manager   读SOP → 向PM发 task_assign（ManagerAssignCrew）
  ↓
步骤3  PM        读邮件 → 写 product_spec.md → 发 task_done（PMExecuteCrew）
  ↓
⏸️ 确认节点2  run.py 写 human.json(checkpoint_request)
              → 终端提示用户打开 design/product_spec.md 确认
              → 输入 y 继续 / n 终止
  ↓
步骤4  Manager   读邮件 → 验收文档 → 写 review_result.md（ManagerReviewCrew）
```

---

## 与第26课的对比

| 项目 | 第26课 | 第27课 |
|------|--------|--------|
| 步骤数 | 4步（步骤0-3） | 4步（步骤1-4） |
| 人工节点 | 无 | 2个（确认需求 + 确认设计） |
| Manager Crew 数量 | 2（分配+验收） | 3（澄清+分配+验收） |
| human.json | 无 | 有（单一接口，只由 run.py 写） |
| 沙盒启动 | 按 profile 分开 | `up -d` 同时启动 |
| 共享区多出内容 | — | `sop/`（产品设计SOP） |

---

## 运行测试（不需要沙盒）

```bash
cd /path/to/crewai_mas_demo
python -m pytest m4l27/test_m4l27.py -v
```

---

## 常见问题

**Q：运行到确认节点卡住不动？**
这是正常行为——程序在等 `input()`。终端会显示：
```
⏸️  [人工确认节点] 需求文档确认
  你的决定 (y/n)：
```
输入 `y` 回车继续，输入 `n` 回车终止。

**Q：想清除状态重新跑？**
```bash
echo "[]" > workspace/shared/mailboxes/manager.json
echo "[]" > workspace/shared/mailboxes/pm.json
echo "[]" > workspace/shared/mailboxes/human.json
rm -f workspace/shared/needs/requirements.md
rm -f workspace/shared/design/product_spec.md
rm -f workspace/manager/review_result.md
rm -f workspace/manager/sessions/*.json workspace/manager/sessions/*.jsonl
rm -f workspace/pm/sessions/*.json workspace/pm/sessions/*.jsonl
```

**Q：报 `ModuleNotFoundError`？**
确认从 `crewai_mas_demo/` 目录运行，不要在 `m4l27/` 内直接运行。

**Q：`n` 拒绝后想重新触发确认？**
本 demo 直接退出。在真实系统中，拒绝会重新触发对应阶段（由编排器决定逻辑）。
