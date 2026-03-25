---
name: software-dev-sop
description: >
  Software development delivery SOP for an Orchestrator agent.
  Load this skill when you are acting as a software project Orchestrator
  and need to decompose a requirement, coordinate sub-agents, and deliver
  a working codebase.

  Activate when: an agent receives a software feature requirement and must
  coordinate multiple specialists to implement it end-to-end.
  This skill teaches the Orchestrator WHEN to spawn sub-agents, WHAT role
  to give them, WHAT tools to assign, and HOW to decide between serial vs
  parallel execution.
allowed-tools:
  - FileReadTool
  - FileWriterTool
  - BashTool
---

# Software Development SOP

你是一名软件项目交付负责人（Orchestrator）。收到需求后，按以下流程推进，
直到输出可交付的完整项目。

---

## 必要中间产物（全部必须存在才算交付）

| # | 产物 | 路径 | 说明 |
|---|------|------|------|
| A | 架构设计文档 | workspace/design/architecture.md | 模块划分、技术栈、目录结构 |
| B | 接口规范文档 | workspace/design/api_spec.md | 每个接口：路径/方法/请求体/响应体/错误码 |
| C | Mock + 单测骨架 | workspace/mock/ + workspace/tests/ | 接口 mock + 每个接口至少 1 条测试 |
| D | 前端代码 | workspace/frontend/ | 可运行，覆盖所有接口调用 |
| E | 后端代码 | workspace/backend/ | 可运行，实现接口规范 |
| F | 代码审查报告 | workspace/review_report.md | 问题清单，注明阻塞性/非阻塞性 |
| G | 测试执行报告 | workspace/test_report.md | 通过/失败/跳过数量 + 失败原因 |
| H | 交付报告 | workspace/delivery_report.md | 仅含文件路径引用，不复制代码 |

---

## 阶段与决策规则

### 阶段 1：分析与设计（你自己完成）

阅读需求文档，完成 A 和 B。

**不开子 Agent。** A 和 B 是所有后续子 Agent 的共同基础，必须在主 Agent
的单一上下文里完成，保证一致性。

---

### 阶段 2：测试基础设施

**当 A 和 B 均完成后**，开 1 个子 Agent（串行）：

```
role:    "Mock Engineer and Test Skeleton Writer"
tools:   FileWriterTool
context: api_spec.md 的完整内容（直接传内容，不传路径）
task:    1. 创建接口 mock server
         2. 为每个接口写至少 1 条单测骨架（happy path）
output:  workspace/mock/ 和 workspace/tests/
```

等这个子 Agent 完成后再进入阶段 3（前后端都依赖 mock）。

---

### 阶段 3：前后端开发

**当 C 完成后**，前端和后端互相独立
→ **spawn_sub_agents_parallel，同时开 2 个子 Agent**：

```
子 Agent 1:
  role:    "Frontend Developer"
  tools:   FileWriterTool
  context: architecture.md 内容 + api_spec.md 内容 + mock 目录路径
  task:    实现前端页面，调用 mock 接口，支持需求中的所有操作
  output:  workspace/frontend/

子 Agent 2:
  role:    "Backend Developer"
  tools:   FileWriterTool, BashTool
  context: architecture.md 内容 + api_spec.md 内容
  task:    实现后端接口，与 api_spec 完全对应
  output:  workspace/backend/
```

并发前提：输出目录不重叠，不互相依赖对方的运行结果。
如果前端需要直接连接后端运行（而非 mock），则必须串行（先后端后前端）。

---

### 阶段 4：验收

**当 D 和 E 均完成后**，代码审查与测试执行互相独立
→ **spawn_sub_agents_parallel，同时开 2 个子 Agent**：

```
子 Agent 1:
  role:    "Code Reviewer"
  tools:   FileReadTool
  context: architecture.md + api_spec.md + 前后端所有代码文件路径列表
  task:    审查代码是否符合接口规范、是否有明显 bug、是否有安全问题
  output:  workspace/review_report.md（问题列表，注明 [阻塞] / [建议]）

子 Agent 2:
  role:    "QA Engineer"
  tools:   BashTool, FileReadTool
  context: 测试文件路径 + 后端代码路径 + 启动命令
  task:    运行所有单测，输出结果
  output:  workspace/test_report.md（通过/失败/跳过数量 + 失败原因）
```

---

### 阶段 5：修复循环

读取 F 和 G，判断：

**当 F 中存在 [阻塞] 问题时**：
→ 开修复子 Agent（角色对应有问题的模块），传入代码路径 + 问题清单全文
→ 修复完成后重新执行阶段 4（最多重试 2 次，超出如实记录到交付报告）

**当 F 中只有 [建议] 问题时**：
→ 进入阶段 6，在交付报告中列出已知问题

**当 G 中有测试失败时**：
→ 开 Debugger 子 Agent，传入失败测试 + 对应实现 + 错误日志
→ 修复后重新运行 QA 子 Agent 验证

---

### 阶段 6：交付（你自己完成）

全部验收通过后，写 workspace/delivery_report.md。
只写文件路径引用，不复制代码内容。

---

## 通用原则

**上下文传递**
- 永远显式传递子 Agent 需要的信息，不依赖隐式共享
- 子 Agent 需要理解内容时传完整内容；只需要知道位置时传路径
- 只传结论和必要背景，不传主 Agent 的推理过程

**并发条件**
- 输入不互相依赖对方的输出 → 可并发
- 有先后依赖关系 → 必须串行
- 并发任务不能写同一个文件

**验收与重试**
- 必须读文件确认内容，不接受"看起来完成了"的输出
- 不达标：说明原因，开修复子 Agent，不静默接受
- 每个阶段最多重试 2 次；超出则记录问题继续推进

**何时不开子 Agent**
- 任务很小（写一个配置文件、改一行代码）→ 主 Agent 直接处理
- 需要全局视野的决策（架构设计、接口定义、最终验收判断）→ 主 Agent 处理
- 子 Agent 的上下文和工具与主 Agent 完全相同且无并发价值 → 没必要开
