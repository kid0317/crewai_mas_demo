# 企业级多智能体设计实战

> 参透 CrewAI 底层逻辑，攻克多 Agent 落地难题

本仓库是《企业级多智能体设计实战》在线视频课程的配套示例代码仓库。

## 📚 课程简介

这是一门专为致力于构建生产级、高可靠 AI 应用的研发人员和架构师设计的实战课程。

### 你将获得

- **告别"野路子"demo**：掌握 MAS 核心设计模式
- **手把手教学**：构建、调试、部署多智能体系统
- **生产环境稳定可用**：企业级 AI 应用治理体系
- **4 大高价值场景实践案例**：自己动手实现 OpenClaw

### 课程特色

✅ **无需魔法，低成本上手**：全程兼容 DeepSeek、Kimi、通义千问等国内优质大模型接口  
✅ **真实生产级案例**：拒绝"贪吃蛇"类玩具案例，提供贴近真实生产环境的场景  
✅ **架构思维优先**：不是框架使用手册，而是 AI 时代的"建筑学"  
✅ **工程化实践**：测试评估、可观测性、容灾设计等生产级治理体系

## 🎯 课程结构

### 架构思维篇：AI 时代的设计模式（4 课）

建立 AI 应用开发的全局认知框架，理解从 Prompt 到 Multi-Agent 的底层演进逻辑。

- **01 | 拨开迷雾**：AI 应用开发的四种架构范式
- **02 | 解构智能体**：Agent 的解剖学与 ReAct 范式
- **03 | Multi-Agent 系统**：Agent、Task、Process 的协作美学
- **04 | 架构师的决断**：AI 应用开发选型工具

### 工程落地篇：从0构建生产级多智能体系统

从零开始构建生产级的多智能体系统，掌握工具集成、上下文管理、协作设计模式。

#### 先导准备（2 课）

- **05 | 工程全景图**：构建企业级多智能体系统的"施工蓝图"
- **06 | 工欲善其器**：课程学习的基础代码环境准备

#### 模块一：运行你的第一个企业级 Multi-Agent（5 课）

- **07 | 定义Agent**：从"提示词工程"到"人设工程"
- **08 | 定义Task**：从"步骤控制"到"契约驱动"
- **09 | 定义Process**：任务调度与信息传递
- **10 | 多模态模型**：让你的Agent拥有"眼睛"
- **11 | 项目实战1**：小红书爆款笔记生成项目

#### 模块二：工具大全，赋予Agent与物理世界交互的能力（6 课）

- **12 | 工具设计哲学**：从 API 到 Agent Tool 的范式跃迁
- **13 | 自定义工具封装**：构建 Tools 的五步标准SOP
- **14 | MCP协议**：标准化定义工具接口
- **15 | Skills协议**：面向Agent的工具升级
- **16 | 王牌超能力**：代码解释器与无头浏览器
- **17 | 项目实战2**：能力篇——OpenClaw 本地工作助手（上）

#### 模块三：上下文管理让Agent拥有记忆，突破Token限制（5 课）

- **18 | 记忆管理的使用**：Short-term、Long-term & Entity Memory
- **19 | 自定义管理上下文**：Step_Callback与数据流观测
- **20 | 知识库的使用与Embedding**：RAG在CrewAI中的实现
- **21 | 超越信息的知识**：通过动态沉淀skill让你的agent自主进化
- **22 | 项目实战3**：记忆篇——OpenClaw 本地工作助手（下）

#### 模块四：协作与设计模式，掌握5大架构设计模式（7 课）

- **23 | 架构模式（一）**：路由模式
- **24 | 架构模式（二）**：中心化调度模式
- **25 | 架构模式（三）**：并行与投票模式
- **26 | 架构模式（四）**：评价-优化循环模式
- **27 | Agent自主协作**：Delegation委托机制
- **28 | Human in the Loop**：关键节点的审批模式
- **29 | 项目实战4**：全栈软件开发团队项目

#### 模块五：企业级加固，确保系统安全可控（4 课）

- **30 | 提高健壮性**：Replay、Test与Retry策略
- **31 | Guardrails**：输入输出的安全护栏
- **32 | Hook**：全链路监控与埋点
- **33 | 项目实战5**：系统加固你的OpenClaw 本地工作助手

### 生产交付篇：全生命周期工程化（7 课）

从技术实现转向生产交付，关注需求分析、测试评估、可观测性、合规治理。

- **34 | 需求边界**：如何使用"AI适用性评估表"识别高ROI场景？
- **35 | 场景演练**：面向10万行代码库的"文档自动维护专家"架构拆解
- **36 | 持续集成（CI/CD）**：基于GitOps的Knowledge库自动更新流水线
- **37 | 自动化测试（Eval）**：引入LLM-as-a-Judge构建AI系统的"单元测试"
- **38 | 全链路可观测性**：集成LangTrace实现Agent思考路径的可视化追踪
- **39 | 生产合规**：Prompt版本管理、灰度发布与PII数据脱敏策略
- **40 | 组织进化**：从Agent开发者到AI系统架构师的能力跃迁

## 📁 项目结构

```
crewai_mas_demo/
├── requirements.txt                    # Python 依赖包列表
│
├── llm/                                # 自定义 LLM 实现（课程06）
│   ├── __init__.py                    # 模块初始化
│   ├── aliyun_llm.py                  # 阿里云通义千问 LLM 实现（核心组件）
│   └── test_*.py                      # LLM 测试用例
│
├── tools/                              # 自定义工具（课程13）
│   ├── __init__.py                    # 模块初始化
│   ├── baidu_search.py                # 百度搜索工具（课程13示例）
│   ├── intermediate_tool.py           # 中间结果保存工具（课程07辅助工具）
│   ├── add_image_tool_local.py        # 本地图片加载工具（课程10核心工具）
│   ├── fixed_directory_read_tool.py   # 目录读取工具（课程13示例）
│   └── test_*.py                      # 工具测试用例
│
├── m1l2/                               # 课程02、07示例代码
│   ├── m1l2_agent.py                  # 单 Agent 调研示例（课程07）
│   ├── m1l2_raw_agent.py              # 原生 Agent 实现（课程02）
│   └── *.md                            # 示例输出文件
│
├── m1l3/                               # 课程09示例代码
│   ├── m1l3_multi_agent.py            # Multi-Agent 协作示例
│   └── *.md                            # 示例输出文件
│
├── m2l2/                               # 课程06示例代码
│   └── m2l2_llm_openai.py             # LLM 配置示例
│
├── m2l3/                               # 课程07示例代码
│   └── m2l3_agent.py                  # Agent 直接执行任务示例
│
├── m2l4/                               # 课程08示例代码
│   └── m2l4_task.py                   # Task 定义与结构化输出示例
│
├── m2l5/                               # 课程09示例代码
│   └── m2l5_crew.py                    # Sequential Process 多任务执行示例
│
├── m2l6/                               # 课程10示例代码
│   └── m2l6_agent.py                  # 多模态视觉分析示例
│
├── m2l8/                               # 课程19示例代码
│   ├── m2l8_context.py                # API 请求级上下文管理
│   └── m2l8_tools_call.py             # 工具调用 Hook 示例
│
├── m2l9/                               # 课程14示例代码
│   └── m2l9_mcp.py                     # MCP 服务器集成示例
│
└── （定稿）上线素材｜企业级多智能体设计实战.md  # 课程大纲
```

## 🚀 快速开始

### 环境准备

- **Python 3.10+**
- **通义千问 API Key**（必需）：访问 [阿里云 DashScope](https://dashscope.console.aliyun.com/) 获取
- **百度搜索 API Key**（必需）：访问 [百度智能云](https://cloud.baidu.com/) 获取

> 💡 **提示**：本课程全程使用国内可访问的大模型接口，无需科学上网。

### 安装与配置

```bash
# 1. 克隆仓库
git clone <repository-url>
cd crewai_mas_demo

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API Key（二选一）
# 方式一：环境变量（推荐）
export QWEN_API_KEY="your-qwen-api-key-here"
export BAIDU_API_KEY="your-baidu-api-key-here"  # 可选

# 方式二：创建 .env 文件
# 在项目根目录创建 .env 文件，内容如下：
# QWEN_API_KEY=your-qwen-api-key-here
# BAIDU_API_KEY=your-baidu-api-key-here
```

### 运行示例

#### 示例 1：原生 Agent 实现（课程02）

理解 Agent 的核心原理和 ReAct 范式。

```bash
cd m1l2
python3 m1l2_raw_agent.py
```

**学习要点**：
- Agent 的本质：循环调用 LLM 和执行工具
- ReAct 范式：Reasoning → Acting → Observation
- 工具调用机制：解析 LLM 输出并执行工具
- 对话历史管理：维护 LLM 上下文

**对应课程**：02｜解构智能体：Agent 的解剖学与 ReAct 范式

---

#### 示例 2：单 Agent 调研（课程07，推荐新手入门）

学习如何定义 Agent 的"人设"。

```bash
cd m1l2
python3 m1l2_agent.py
```

**学习要点**：
- Agent 的 Role、Goal、Backstory 定义（人设工程）
- 工具集成（搜索、网页抓取、文件写入）
- ReAct 循环的实际运行过程
- Task 和 Crew 的创建

**输出结果**：
- 控制台：Agent 的思考过程（Thought/Action/Observation）
- 文件：`m1l2/极客时间-最终报告.md`

**对应课程**：07｜定义Agent：从"提示词工程"到"人设工程"

**预期时间**：约 2-5 分钟

---

#### 示例 3：Agent 直接执行任务（课程07）

演示 Agent.kickoff() 直接与 Agent 交互。

```bash
cd m2l3
python3 m2l3_agent.py
```

**学习要点**：
- Agent.kickoff() 的使用方法
- 无需创建 Task 和 Crew 的简单场景
- IntermediateTool 的使用

**对应课程**：07｜定义Agent：从"提示词工程"到"人设工程"

---

#### 示例 4：Task 定义与结构化输出（课程08）

学习"契约驱动"的任务设计。

```bash
cd m2l4
python3 m2l4_task.py
```

**学习要点**：
- Pydantic 模型定义数据结构（契约）
- Task 的 output_pydantic 参数
- Task 的 context 参数实现任务依赖
- Mock 上游任务输出

**对应课程**：08｜定义Task：从"步骤控制"到"契约驱动"

---

#### 示例 5：Multi-Agent 协作（课程09）

学习多 Agent 协作和任务调度。

```bash
cd m1l3
python3 m1l3_multi_agent.py
```

**学习要点**：
- 多 Agent 协作（Researcher、Searcher、Writer、Editor）
- Sequential Process 实现
- 任务依赖关系（context 参数）
- Agent 委托机制（allow_delegation）

**输出结果**：
- 控制台：多个 Agent 的协作过程
- 文件：`m1l3/极客时间平台全面调研报告-*.md`（大纲、步骤1-6、最终报告）

**对应课程**：09｜定义Process：任务调度与信息传递

**预期时间**：约 5-10 分钟

---

#### 示例 6：Sequential Process 多任务流程（课程09）

演示多任务的顺序执行和数据传递。

```bash
cd m2l5
python3 m2l5_crew.py
```

**学习要点**：
- 多个 Task 的定义和依赖关系
- Sequential Process 确保任务顺序执行
- 任务之间的数据传递（context 和 inputs）
- 结构化输出的链式传递

**对应课程**：09｜定义Process：任务调度与信息传递

---

#### 示例 7：多模态视觉分析（课程10）

让 Agent 具备"看"的能力。

```bash
cd m2l6
python3 m2l6_agent.py
```

**学习要点**：
- 多模态 Agent 配置（AddImageToolLocal）
- 图片处理流程（读取 → Base64 → 多模态模型）
- 结构化输出（Pydantic 模型）
- 视觉分析报告的生成

**对应课程**：10｜多模态模型：让你的Agent拥有"眼睛"

---

#### 示例 8：上下文管理与 Hook（课程19）

学习 API 请求级上下文管理和工具调用拦截。

```bash
cd m2l8
python3 m2l8_tools_call.py
```

**学习要点**：
- Hook 机制（before_tool_call、after_tool_call）
- 上下文变量（contextvars）的使用
- 文件路径安全校验和重定向
- 多租户工作空间隔离

**对应课程**：19｜自定义管理上下文：Step_Callback与数据流观测

---

#### 示例 9：MCP 协议集成（课程14）

学习如何通过 MCP 协议集成外部工具服务。

```bash
cd m2l9
python3 m2l9_mcp.py
```

**学习要点**：
- MCP 服务器配置（HTTP 方式）
- 工具过滤器（Tool Filter）的使用
- 多租户支持（通过 headers 传递 user_id）
- 工具缓存（cache_tools_list）

**对应课程**：14｜MCP协议：标准化定义工具接口

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| `ModuleNotFoundError: No module named 'crewai'` | `pip install -r requirements.txt` |
| `ValueError: API Key 未提供` | 检查环境变量：`echo $QWEN_API_KEY`（Linux/macOS）或 `echo $env:QWEN_API_KEY`（Windows） |
| `No module named 'llm'` | 确保在示例目录下运行：`cd m1l2 && python3 m1l2_agent.py` |

## 🛠️ 核心组件

### 自定义 LLM（`llm/aliyun_llm.py`）

基于 CrewAI `BaseLLM` 的阿里云通义千问实现，完全兼容 CrewAI 接口，支持 Function Calling 和多地域配置。

```python
from llm import aliyun_llm

llm = aliyun_llm.AliyunLLM(
    model="qwen-plus",
    api_key=os.getenv("QWEN_API_KEY"),
    region="cn",  # 支持 "cn", "intl", "finance"
)
```

### 自定义工具（`tools/`）

课程13的示例代码展示了如何按照五步标准SOP封装自定义工具。

#### 百度搜索工具（`baidu_search.py`）

支持网页、视频、图片等多种资源类型，演示完整的工具封装流程。

```python
from tools import BaiduSearchTool

agent = Agent(
    role="网络调研专家",
    tools=[BaiduSearchTool()],
    # ...
)
```

**功能特点**：
- 支持时间筛选（week/month/semiyear/year）
- 支持指定站点搜索
- 完整的错误处理和日志记录
- 格式化的搜索结果输出

#### 其他工具

- **IntermediateTool**（`intermediate_tool.py`）：中间结果保存工具，支持 Agent 的"慢思考"模式
- **AddImageToolLocal**（`add_image_tool_local.py`）：本地图片加载工具，支持多模态 Agent
- **FixedDirectoryReadTool**（`fixed_directory_read_tool.py`）：目录读取工具，修复了原版本的路径处理问题

## 📖 学习路径

### 第一阶段：基础入门（课程02-06）

1. **理解 Agent 本质**（课程02）
   - 运行 `m1l2/m1l2_raw_agent.py`，理解 ReAct 范式
   - 掌握 Agent 的核心工作原理

2. **环境准备**（课程06）
   - 配置 LLM 环境（`llm/aliyun_llm.py`）
   - 了解自定义 LLM 的实现方式

### 第二阶段：核心能力（课程07-10）

3. **定义 Agent**（课程07）
   - 运行 `m1l2/m1l2_agent.py` 和 `m2l3/m2l3_agent.py`
   - 学习 Role、Goal、Backstory 的"人设工程"
   - 掌握工具集成方法

4. **定义 Task**（课程08）
   - 运行 `m2l4/m2l4_task.py`
   - 学习"契约驱动"的任务设计
   - 掌握 Pydantic 结构化输出

5. **定义 Process**（课程09）
   - 运行 `m1l3/m1l3_multi_agent.py` 和 `m2l5/m2l5_crew.py`
   - 学习多 Agent 协作和任务调度
   - 掌握任务依赖关系

6. **多模态能力**（课程10）
   - 运行 `m2l6/m2l6_agent.py`
   - 学习如何让 Agent 具备"看"的能力
   - 掌握图片处理和多模态模型集成

### 第三阶段：工具与上下文（课程12-19）

7. **工具封装**（课程13）
   - 学习 `tools/baidu_search.py` 的实现
   - 掌握五步标准SOP封装工具
   - 理解工具设计的最佳实践

8. **MCP 协议**（课程14）
   - 运行 `m2l9/m2l9_mcp.py`
   - 学习如何集成外部工具服务
   - 掌握工具过滤器和多租户支持

9. **上下文管理**（课程19）
   - 运行 `m2l8/m2l8_tools_call.py`
   - 学习 Hook 机制和上下文变量
   - 掌握多租户数据隔离

### 第四阶段：实战项目（课程11、17、22、29、33）

- **项目实战1**（课程11）：小红书爆款笔记生成项目
- **项目实战2**（课程17）：OpenClaw 本地工作助手（上）
- **项目实战3**（课程22）：OpenClaw 本地工作助手（下）
- **项目实战4**（课程29）：全栈软件开发团队项目
- **项目实战5**（课程33）：系统加固你的OpenClaw 本地工作助手

### 第五阶段：生产交付（课程34-40）

学习需求分析、测试评估、可观测性、合规治理等生产级实践。

## 🔧 开发指南

### 代码注释说明

本仓库的所有 Python 代码都包含详细的课程关联注释，遵循统一的标准：

1. **文件头部注释**：包含课程信息、示例说明、学习要点
2. **分节注释**：使用 `# ==============================================================================` 分隔代码块
3. **关键代码注释**：对重要代码段进行详细说明
4. **课程关联**：每个文件都明确标注对应的课程章节

**注释标准参考**：`m2l3/m2l3_agent.py`

### 日志配置

```bash
export LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
```

### 运行测试

```bash
# LLM 测试
cd llm && pytest test_aliyun_llm.py

# 工具测试
cd tools && pytest test_baidu_search.py
```

### 代码结构说明

- **m1lX/**：架构思维篇和模块一的示例代码
- **m2lX/**：模块二的示例代码
- **llm/**：自定义 LLM 实现（核心组件）
- **tools/**：自定义工具实现（示例代码）

每个示例代码文件都对应特定的课程章节，文件名中的数字对应课程编号。

## 📚 相关资源

- [CrewAI 官方文档](https://docs.crewai.com/)
- [通义千问 API 文档](https://help.aliyun.com/zh/model-studio/)
- [百度千帆搜索 API](https://cloud.baidu.com/doc/AppBuilder/s/8lq6h7hqa)

## 👨‍🏫 关于课程

### 讲师介绍

**晓寒** - 前百度资深架构师

曾任业务线EE工程效率负责人、AI产品负责人，目前为某头部金融企业智能技术发展部架构师，负责公司内大模型相关业务落地转型及内部AI基础平台建设工作。

2024年～2025年在公司内部进行了自研AI基础平台（模型使用平台、RAG知识库、可拖拽工作流平台、Agent平台）、业务场景AI落地解决方案（智能客服、业务数据分析、CUI业务流程改造）以及开源平台企业落地改造（基于开源Coze进行企业内多租户、权限、内部系统对接能力等改造）。

同时他也是公司内的AI布道和培训师，2025年给公司管理层及各业务部门长进行了10余次AI技术和产品趋势讲解，进行了6次公司级AI技能培训及10余次受邀的部门级AI落地培训，注重互动与启发，多次为企业内外部提供培训，帮助学员提升实战能力，广受好评。

### 课程理念

本课程旨在帮助学员完成从**"Prompt 调优者"到"AI 系统架构师"**的身份蜕变。

**核心理念**：
- 不是框架的使用手册，而是 AI 时代的"建筑学"
- 用架构管理不确定性，而非用代码消除不确定性
- 从"操作员"到"部门经理"的思维升级
- 从架构设计到生产部署，打造高可靠、可治理的智能体军团

### 课程特色

✅ **无需魔法，低成本上手**：全程兼容 DeepSeek、Kimi、通义千问等国内优质大模型接口  
✅ **真实生产级案例**：拒绝"贪吃蛇"类玩具案例，提供贴近真实生产环境的场景  
✅ **架构思维优先**：不是框架使用手册，而是 AI 时代的"建筑学"  
✅ **工程化实践**：测试评估、可观测性、容灾设计等生产级治理体系  
✅ **完整代码注释**：所有代码都包含详细的课程关联注释，便于学员理解

> 📝 **提示**：本仓库为课程配套代码，建议结合视频课程学习使用。课程详细大纲请参考 `（定稿）上线素材｜企业级多智能体设计实战.md`。
