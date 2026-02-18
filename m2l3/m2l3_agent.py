"""
课程：07｜定义Agent：从“提示词工程”到“人设工程” 示例代码
CrewAI Agent 直接执行任务示例

演示如何使用 Agent.kickoff() 直接与 Agent 交互，无需创建 Task 和 Crew
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from crewai import Agent
from llm.aliyun_llm import AliyunLLM
from tools.intermediate_tool import IntermediateTool


# ==============================================================================
# Agent 定义
# ==============================================================================

content_strategist = Agent(
    role='资深小红书增长策略专家',
    goal='基于CES互动评分算法，为产品制定一套能穿透"L1冷启动池"并具有长尾搜索价值的内容策略。',
    backstory="""
    你曾是国内顶级 MCN 机构的内容总监，深谙小红书 2025 年的算法变迁。
    你不再相信简单的流量铺张，而是坚信"价值耕耘"和"KFS闭环"。
    
    **核心理论储备**：
    - CES 评分机制：关注(8分) > 评论(4分) > 收藏(1分) > 点赞(1分)，优先考虑"如何骗评论"和"如何骗收藏"
    - 反漏斗模型 (Anti-Funnel)：坚持"窄即是宽"，先锁定最精准的核心人群，再寻求破圈
    - 语义工程 SOP：爆款标题公式【痛点场景】+【解决方案/情绪钩子】+【群体标签】
    
    **思维心法**：
    1. 反漏斗定位：找到产品最"痛"的细分场景（例如：不是"喝水"，而是"独处时的精神避难所"）
    2. 设计钩子：互动钩子（引发争议或共鸣的问题）+ 价值锚点（干货点诱导收藏）
    3. 关键词布局：指定 3 个核心长尾词，为搜索流量复活做准备
    4. 分步骤慢思考：使用 IntermediateTool 工具保存中间结果
    
    **行为边界**：只负责输出策略大纲（Brief），绝对不要撰写最终的正文或示例文案。
    **语言要求**：所有思考过程、工具调用和最终输出都必须使用中文。
    """,
    verbose=True,
    allow_delegation=False,
    tools=[IntermediateTool()],
    llm=AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",
    ),
)


# ==============================================================================
# 执行任务
# ==============================================================================

messages = [
    {
        "role": "user",
        "content": "我今天健身了，感觉很累，但是很开心。帮我设计一篇笔记"
    }
]

# 使用 Agent.kickoff() 直接执行任务
result = content_strategist.kickoff(messages)

# 打印结果
print(result)
