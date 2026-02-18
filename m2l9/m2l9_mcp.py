"""
课程：14｜MCP协议：标准化定义工具接口 示例代码
MCP 服务器集成示例

演示如何使用 CrewAI 的 MCP（Model Context Protocol）功能集成外部工具服务，包括：
1. MCP 服务器配置（HTTP 方式）
2. 工具过滤器（Tool Filter）的使用
3. 多租户支持（通过 headers 传递 user_id）
4. 工具缓存（cache_tools_list）

本示例展示了：
- MCP 协议：如何通过标准协议集成外部工具服务
- HTTP MCP 服务器：如何使用 MCPServerHTTP 连接 HTTP 服务
- 工具过滤：如何使用 static_filter 限制 Agent 可用的工具
- 多租户支持：如何通过 headers 传递用户信息

学习要点：
- MCP 协议：标准化的工具接口协议
- 工具集成：如何将外部服务集成到 CrewAI Agent
- 安全控制：如何使用工具过滤器限制 Agent 的能力
- 多租户设计：如何在 MCP 中实现多租户支持
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径，以便能够导入项目模块
project_root = Path(__file__).resolve().parent.parent
print(project_root)
sys.path.insert(0, str(project_root))

from crewai import Agent, Task, Crew, Process
from llm import aliyun_llm
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE
from crewai.mcp.filters import create_static_tool_filter, create_dynamic_tool_filter, ToolFilterContext


# ==============================================================================
# MCP 服务器配置
# ==============================================================================
# 工具过滤器：限制 Agent 只能使用指定的工具
# 这是安全控制的重要机制，防止 Agent 使用不应该使用的工具

static_filter = create_static_tool_filter(
    allowed_tool_names=["send_email", "get_mail_list", "get_mail_detail"]
)

# 用户ID：用于多租户支持
user_id = "user01"


# ==============================================================================
# Agent 定义：邮件收发 Agent
# ==============================================================================
# 本 Agent 展示了如何集成 MCP 服务器：
# 1. mcps 参数：配置 MCP 服务器连接
# 2. tool_filter：限制可用的工具
# 3. headers：传递用户信息（多租户支持）
# 4. cache_tools_list：缓存工具列表，提高性能

email_agent = Agent(
    role="你是一个电子邮件收发员",
    goal="高效的完成电子邮件的收发",
    backstory="""
    你是一个经验丰富的电子邮件收发员，擅长使用电子邮件工具来完成电子邮件的收发，使用最少的操作完成任务。
    你通常会使用以下工具来完成任务：
    - 发送邮件：send_email
    - 查看邮箱邮件：get_mail_list
    - 查看邮件详情：get_mail_detail
    你非常善于撰写邮件支持的Multipart正文格式，并能够根据邮件内容生成相应的邮件正文。
    
    你只负责完成邮件的收发以及撰写邮件正文，保证所有信息都准确无误的传达，不要自己去理解和编造信息。
    """,
    # MCP 服务器配置：使用 HTTP 方式连接外部工具服务
    mcps=[MCPServerHTTP(
        url="http://localhost:8005/mcp",  # MCP 服务器地址
        headers={
            "Authorization": "Bearer qqkkk",  # 认证令牌
            "X-User-Id": user_id  # 用户ID（多租户支持）
        },
        streamable=True,  # 支持流式响应
        cache_tools_list=True,  # 缓存工具列表，提高性能
        tool_filter=static_filter,  # 工具过滤器，限制可用工具
    )],
    llm=aliyun_llm.AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",  # 使用 region 参数，可选值: "cn", "intl", "finance"
    ),
)


# ==============================================================================
# Task 定义：邮件任务
# ==============================================================================

send_email_task = Task(
    description="你需要帮我撰写一封邮件，使用我的邮箱569323972@qq.com，收件人是xh_1988@sina.com, 邮件主题是告诉对方我开发了一个邮箱的MCP服务，让他过来试用。",
    expected_output="成功调用send_email工具，发送邮件成功",
    agent=email_agent,
)

get_email_task = Task(
    description="你需要帮我查看我的邮箱xh_1988@sina.com，查看邮件列表，并将其中第一封邮件的详情告诉我。",
    expected_output="成功调用get_mail_list工具，查看邮件列表成功，并成功调用get_mail_detail工具，查看邮件详情成功，最终返回邮件列表和详情的信息给用户",
    agent=email_agent,
)

# ==============================================================================
# Crew 定义：邮件管理工作流
# ==============================================================================
# Process.sequential：顺序执行任务，先发送邮件，再查询邮件

crew = Crew(
    agents=[email_agent],
    tasks=[send_email_task, get_email_task],
    process=Process.sequential,  # 顺序执行模式
    verbose=True,
)


# ==============================================================================
# 执行任务
# ==============================================================================
# Agent 会通过 MCP 协议调用外部邮件服务，完成邮件发送和查询

result = crew.kickoff()
print(result)