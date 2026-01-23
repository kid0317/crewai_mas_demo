import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径，以便能够导入项目模块
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


from crewai import Agent, Task, Crew, Process
from llm.aliyun_llm import AliyunLLM
from tools.intermediate_tool import IntermediateTool
# ==============================================================================
# 0. 模拟上游输入 (视觉分析报告 + 用户意图)
# ==============================================================================
visual_report_input = """
【视觉分析报告】
1. 画面主体：一只墨绿色的粗陶马克杯，杯口有不规则的金边。
2. 背景环境：午后的窗边，有树影落在木质桌面上，旁边放着一本打开的英文书。
3. 氛围关键词：松弛感、复古、独处、静谧。
"""

user_intent_input = "我想卖这个杯子，突出它的质感，想吸引那些喜欢宅家读书记笔记的女生。"

# ==============================================================================
# 1. 定义 Agent: 爆款营销策划 (The Strategist)
#    - 深度融合《小红书营销策略研究》报告精髓
# ==============================================================================
content_strategist = Agent(
    # [R] Role: 激活 "小红书增长黑客" 知识域
    role='资深小红书增长策略专家 (CES算法专家)',

    # [G] Goal: 锁定 KPI —— 不仅仅是写内容，而是设计"高互动率"的引擎
    goal='基于CES互动评分算法，为产品制定一套能穿透"L1冷启动池"并具有长尾搜索价值的内容策略。',

    # [B] Backstory: 注入专家灵魂 (四部曲)
    backstory="""
    # [1. Identity & Context: 身份锚点]
    你曾是国内顶级 MCN 机构的内容总监，深谙小红书 2025 年的算法变迁。
    你不再相信简单的流量铺张，而是坚信"价值耕耘"和"KFS闭环"。
    
    # [2. Knowledge: 核心理论储备]
    - **CES 评分机制**: 你知道 评论(4分) > 收藏(1分) > 点赞(1分)。因此你的策略总是优先考虑"如何骗评论"和"如何骗收藏"。
    - **反漏斗模型 (Anti-Funnel)**: 你坚持"窄即是宽"。你总是先锁定最精准的核心人群(Core)，再寻求破圈。
    - **语义工程 SOP**: 你熟背爆款标题公式：【痛点场景】+【解决方案/情绪钩子】+【群体标签】。

    # [3. Methodology & Mindset: 思维心法] (CoT)
    在制定策略时，你严格遵循以下逻辑链路：
    
    1. **Anti-Funnel Targeting (反漏斗定位)**: 
       不要泛泛而谈。先找到该产品最"痛"的那个细分场景（例如：不是"喝水"，而是"独处时的精神避难所"）。
    
    2. **Designing the "Hook" (设计钩子)**:
       - **Interaction Bait (互动钩子)**: 设计一个能引发争议或共鸣的问题，放在文案结尾骗评论（例如："大家觉得墨绿好看还是复古红好看？"）。
       - **Value Anchor (价值锚点)**: 提炼一个干货点（如"如何打造书桌氛围感"），诱导用户为了以后能用到而点击"收藏"。
    
    3. **Keyword Layout (关键词布局)**:
       虽然你不是 SEO 专员，但你必须在策略中指定 3 个核心长尾词（Long-tail Keywords），为后续的搜索流量复活做准备。

    4. **Slow Thinking (分步骤慢思考)**:
       你会分步思考，每一步都会使用 IntermediateTool 工具保存中间结果，以便后续步骤可以继续使用。

    # [4. Boundaries: 行为边界]
    - **Strategy Only**: 你只负责输出策略大纲（Brief），**绝对不要**撰写最终的正文或者示例文案。
    """,
    
    verbose=True, # 开启上帝视角，观察 Agent 思考过程
    allow_delegation=False,
    tools=[IntermediateTool()],
    llm=AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",  # 使用 region 参数，可选值: "cn", "intl", "finance"
    ),
)

# ==============================================================================
# 2. 定义 Task: 要求结构化输出策略
# ==============================================================================
strategy_task = Task(
    description=f"""
    请根据输入信息，运用你的 CES 算法知识和反漏斗模型，制定一篇小红书爆款笔记的**策略简报**。
    
    ---输入信息---
    {visual_report_input}
    
    {user_intent_input}
    -------------
    """,
    expected_output="""
    一份结构化的 JSON 格式策略简报，包含以下字段：
    示例格式：
    {
        "Target_Core_Audience": "核心细分人群（越窄越好）",
        "Pain_Point_Scene": "具体的痛点或使用场景",
        "Title_Formula": "建议的标题逻辑（痛点+钩子+人群）",
        "Content_Brief": "文案内容的策略大纲",
        "Interaction_Plan": "如何设计评论诱饵（提高CES评论分）",
        "Value_Proposition": "为什么用户会收藏这篇笔记（提高CES收藏分）",
        "Core_Keywords": ["3个建议布局的长尾关键词1", "关键词2", "关键词3"]
    }
    """,
    agent=content_strategist
)

# ==============================================================================
# 3. 运行 Crew
# ==============================================================================
crew = Crew(
    agents=[content_strategist],
    tasks=[strategy_task],
    process=Process.sequential
)

print("############# 开始制定高 CES 增长策略 #############")
result = crew.kickoff()

print("\n\n############# 最终策略产出 #############")
print(result)