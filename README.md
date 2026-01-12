# CrewAI 多智能体实战：从 Demo 到生产级应用构建

> 本仓库是《CrewAI 多智能体实战：从 Demo 到生产级应用构建》在线视频课程的配套示例代码仓库。

## 📚 课程简介

这是一门专为致力于构建生产级、高可靠 AI 应用的研发人员和架构师设计的实战课程。

### 核心价值

- **建立 AI 时代的架构思维**：从设计模式的角度理解多智能体系统，掌握 MAS 设计模式与选型决策
- **跨越 Demo 到 Production 的鸿沟**：学习工程化实践，构建可观测、可维护、可扩展的企业级 AI 系统
- **全生命周期工程化**：从需求分析、开发测试、部署运维到组织能力的完整治理体系

### 课程特色

✅ **无需魔法，低成本上手**：全程兼容 DeepSeek、Kimi、通义千问等国内优质大模型接口  
✅ **真实生产级案例**：拒绝"贪吃蛇"类玩具案例，提供贴近真实生产环境的场景  
✅ **架构思维优先**：不是框架使用手册，而是 AI 时代的"建筑学"  
✅ **工程化实践**：测试评估、可观测性、容灾设计等生产级治理体系

## 🎯 课程结构

### 第一篇：架构思维篇（4 课）
建立 AI 应用开发的全局认知框架，理解从 Prompt 到 Multi-Agent 的底层演进逻辑。

- **01 | 范式转移**：从"单体 Prompt 工程"到"多智能体架构（MAS）"
- **02 | 解构智能体**：Agent 的解剖学与 ReAct 范式
- **03 | 组织拓扑**：Multi-Agent 系统——Agent, Task, Process 的协作美学
- **04 | 选型决策**：C.U.P. 决策模型与选型矩阵

### 第二篇：工程落地篇（6 个模块）
从零开始构建生产级的多智能体系统，掌握工具集成、上下文管理、协作设计模式。

- **模块一**：先导准备 - 工程全景图与环境准备
- **模块二**：先跑起来 - Agent、Task、Process 基础
- **模块三**：工具大全 - 工具生态与设计范式
- **模块四**：上下文管理 - 记忆系统与 RAG
- **模块五**：协作与设计模式 - 5 大架构设计模式
- **模块六**：稳定性 - 企业级加固

### 第三篇：生产交付篇（8 课）
从技术实现转向生产交付，关注需求分析、测试评估、可观测性、合规治理。

## 📁 项目结构

```
crewai_mas_demo/
├── requirements.txt             # Python 依赖包列表
├── llm/                          # 自定义 LLM 实现
│   ├── aliyun_llm.py            # 阿里云通义千问 LLM 实现
│   ├── customLLM.md             # 自定义 LLM 文档
│   └── test_aliyun_llm.py       # LLM 测试用例
│
├── tools/                        # 自定义工具
│   ├── baidu_search.py         # 百度搜索工具
│   ├── fixed_directory_read_tool.py  # 目录读取工具
│   └── 百度搜索API.md           # 工具使用文档
│
├── m1l2/                        # 第一篇章第 2 课示例：单 Agent
│   ├── m1l2_agent.py            # 单 Agent 调研示例
│   └── 极客时间-最终报告.md     # 示例输出
│
├── m1l3/                        # 第一篇章第 3 课示例：Multi-Agent
│   ├── m1l3_multi_agent.py      # 多智能体协作示例
│   ├── 极客时间平台全面调研报告-报告大纲.md
│   └── 极客时间平台全面调研报告-步骤*.md  # 分步报告
│
├── 课程大纲模版.md              # 完整课程大纲
└── 课程第一篇章详细设计.md      # 第一篇章详细教学设计
```

## 🚀 快速开始

### 环境准备

- **Python 3.8+**（推荐 Python 3.10+）
- **通义千问 API Key**（必需）：访问 [阿里云 DashScope](https://dashscope.console.aliyun.com/) 获取
- **百度搜索 API Key**（可选）：访问 [百度智能云](https://cloud.baidu.com/) 获取

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

#### 示例 1：单 Agent 调研（推荐新手入门）

```bash
cd m1l2
python3 m1l2_agent.py
```

**学习要点**：
- Agent 的 Role、Goal、Backstory 定义
- 工具集成（搜索、网页抓取、文件写入）
- ReAct 循环的实际运行过程

**输出结果**：
- 控制台：Agent 的思考过程（Thought/Action/Observation）
- 文件：`m1l2/极客时间-最终报告.md`

**预期时间**：约 2-5 分钟

#### 示例 2：Multi-Agent 协作（进阶）

```bash
cd m1l3
python3 m1l3_multi_agent.py
```

**学习要点**：
- 多 Agent 协作（Researcher、Searcher、Writer、Editor）
- Sequential Process 实现
- 上下文隔离与任务传递

**输出结果**：
- 控制台：多个 Agent 的协作过程
- 文件：`m1l3/极客时间平台全面调研报告-*.md`（大纲、步骤1-6、最终报告）

**预期时间**：约 5-10 分钟

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

- **百度搜索工具**（`baidu_search.py`）：支持网页、视频、图片等多种资源类型
- **目录读取工具**（`fixed_directory_read_tool.py`）：文件系统操作工具

```python
from tools import BaiduSearchTool

agent = Agent(
    role="网络调研专家",
    tools=[BaiduSearchTool()],
    # ...
)
```

## 📖 学习路径

### 第一篇章：架构思维篇

通过"竞品分析报告生成"案例，展示四种架构范式的差异：
1. **Prompt Engineering**：单指令范式
2. **Workflow / Chain**：代码驱动的流水线
3. **Single Agent**：单智能体范式
4. **Multi-Agent System**：多智能体协作

**核心收获**：理解阿什比定律、掌握 C.U.P. 决策模型、建立"面向组织编程"的架构思维

### 实战案例

- 科技新闻全自动简报系统（Research + Writer Agent）
- 金融数据分析师（Code Interpreter）
- 企业私有知识库客服（RAG + Memory）
- 全栈软件开发团队（Evaluator-Optimizer 模式）

## 🔧 开发指南

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

## 📚 相关资源

- [CrewAI 官方文档](https://docs.crewai.com/)
- [通义千问 API 文档](https://help.aliyun.com/zh/model-studio/)
- [百度千帆搜索 API](https://cloud.baidu.com/doc/AppBuilder/s/8lq6h7hqa)

## 👨‍🏫 关于课程

本课程旨在帮助学员完成从**"Prompt 调优者"到"AI 系统架构师"**的身份蜕变。

**核心理念**：
- 不是框架的使用手册，而是 AI 时代的"建筑学"
- 用架构管理不确定性，而非用代码消除不确定性
- 从"操作员"到"部门经理"的思维升级

> 📝 **提示**：本仓库为课程配套代码，建议结合视频课程学习使用。课程详细大纲请参考 `课程大纲模版.md` 和 `课程第一篇章详细设计.md`。
