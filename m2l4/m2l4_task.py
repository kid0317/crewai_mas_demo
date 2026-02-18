"""
课程：08｜定义Task：从"步骤控制"到"契约驱动" 示例代码
Task 定义与结构化输出示例

演示如何使用 Pydantic 模型定义 Task 的结构化输出，实现"契约驱动"的任务设计：
1. 使用 Pydantic BaseModel 定义数据结构（契约）
2. Task 的 output_pydantic 参数指定输出格式
3. Task 的 context 参数实现任务依赖关系
4. 通过 TaskOutput 设置上游任务的输出（Mock 数据）

本示例展示了：
- 数据模型定义：如何用 Pydantic 定义结构化输出
- Task 依赖：如何通过 context 参数传递上游任务的输出
- Mock 数据：如何在开发阶段模拟上游任务的输出
- 结构化输出：如何确保 Agent 的输出符合预定义的数据结构

学习要点：
- 契约驱动：通过 Pydantic 模型定义任务输出的"契约"
- 任务依赖：context 参数如何实现任务之间的数据传递
- 结构化输出：如何确保 Agent 的输出格式符合预期
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from crewai import Agent, Task, Crew, Process, TaskOutput
from llm.aliyun_llm import AliyunLLM
from pydantic import BaseModel, Field
from tools.intermediate_tool import IntermediateTool
from typing import List


# ==============================================================================
# 数据模型定义（契约定义）
# ==============================================================================
# 使用 Pydantic BaseModel 定义数据结构，这是"契约驱动"的核心
# 这些模型定义了 Agent 输出的"契约"，确保输出格式符合预期

class ImageAnalysis(BaseModel):
    """单张图片的深度分析详情"""
    file_name: str = Field(..., description="图片文件名或ID。")
    subject_description: str = Field(..., description="【主体内容】客观描述画面中的核心物体、人物或场景。")
    atmosphere_vibe: str = Field(..., description="【风格氛围】用形容词描述画面的情绪价值。")
    visual_details: List[str] = Field(..., description="【细节点列表】列出画面中容易被忽略但具象的元素。")
    image_quality_score: str = Field(..., description="【质量评价】1-10分打分，基于构图、光线和清晰度给出打分的原因。")
    highlight_feature: str = Field(..., description="【突出特点】这张图最抓人眼球的一个视觉锚点（Visual Hook）。")


class VisualAnalysisReport(BaseModel):
    """视觉与意图分析报告 - 作为下游任务的输入上下文"""
    user_raw_intent: str = Field(..., description="用户的原始文字诉求摘要。")
    analyzed_images: List[ImageAnalysis] = Field(..., description="包含所有输入图片的详细分析列表。")
    overall_visual_summary: str = Field(..., description="综合所有图片得出的整体视觉基调总结。")


class ContentStrategyBrief(BaseModel):
    """爆款内容策划简报 - Strategist Agent 的交付物"""
    input_evaluation: str = Field(..., description="【素材评估】基于用户诉求和图片质量的综合评价，指出优势和劣势，并给出修图建议。")
    target_audience_persona: str = Field(..., description="【目标受众画像】采用反漏斗模型，定义最核心的细分人群（年龄段、职业标签、生活状态、心理诉求）。")
    core_pain_point: str = Field(..., description="【核心痛点/诉求】受众最想解决的问题或最渴望的情绪价值。")
    suggested_title: str = Field(..., description="【建议标题】遵循公式：'痛点场景 + 情绪/利益钩子 + 核心人群标签'，包含标点符号和Emoji，20字以内。")
    content_outline: List[str] = Field(..., description="【笔记大纲】笔记正文的结构安排（场景引入、沉浸式体验、干货植入、结尾强引导）。")
    engagement_strategy: str = Field(..., description="【点赞评论诱饵】设计具体的策略来引发评论互动。")
    retention_strategy: str = Field(..., description="【收藏诱饵】提供具体的实用价值让用户点击收藏。")
    seo_keywords: List[str] = Field(..., description="【关键词布局】基于 KFS 策略，列出 3 个必须埋入文案的长尾关键词。")


# ==============================================================================
# Agent 定义：内容策略专家
# ==============================================================================
# 本示例定义了一个内容策略专家 Agent，负责制定内容策略

content_strategist = Agent(
    role='资深小红书增长策略专家',
    goal='基于CES互动评分算法，为产品制定一套能穿透"L1冷启动池"并具有长尾搜索价值的内容策略。',
    backstory="""
    你曾是国内顶级 MCN 机构的内容总监，深谙小红书 2025 年的算法变迁。
    你不再相信简单的流量铺张，而是坚信"价值耕耘"和"KFS闭环"。
    
    **核心理论储备**：
    - CES 评分机制：评论(4分) > 收藏(1分) > 点赞(1分)，优先考虑"如何骗评论"和"如何骗收藏"
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
# Mock 上游任务输出（开发阶段使用）
# ==============================================================================
# 在实际开发中，上游任务可能还未实现，可以使用 Mock 数据来测试下游任务
# 通过 TaskOutput 设置上游任务的输出，模拟真实的任务执行结果

# 创建模拟的视觉分析报告
visual_report = VisualAnalysisReport(
    user_raw_intent="想卖这个墨绿色马克杯，主打独居女生市场，强调氛围感和情绪价值",
    analyzed_images=[
        ImageAnalysis(
            file_name="cup_001.jpg",
            subject_description="一只带有金色裂纹纹理的墨绿色陶瓷马克杯，放置在木质书桌上",
            atmosphere_vibe="静谧、复古、松弛感",
            visual_details=["书页上的光斑", "杯口边缘的咖啡渍", "背景虚化的绿植", "暖色调的台灯光线"],
            image_quality_score="6分，构图有些杂乱，光线有些暗，清晰度一般",
            highlight_feature="金色裂纹纹理在暖光下的反光效果"
        ),
        ImageAnalysis(
            file_name="cup_002.jpg",
            subject_description="同一只马克杯的特写，展示杯身的细节和质感",
            atmosphere_vibe="精致、温暖、治愈",
            visual_details=["陶瓷表面的细腻质感", "墨绿色与金色的对比", "杯内残留的咖啡液", "柔和的侧光"],
            image_quality_score="8分，构图、光线和清晰度都很好，特写的鱼眼效果稍微有点变形",
            highlight_feature="墨绿色与金色裂纹的强烈视觉对比"
        ),
        ImageAnalysis(
            file_name="cup_003.jpg",
            subject_description="一个长发女生的背影，坐在书周边，手上拿着一个马克杯",
            atmosphere_vibe="慵懒、放松、治愈",
            visual_details=["书桌上的台灯", "书桌上的绿植", "书桌上的咖啡杯", "书桌上的笔记本电脑"],
            image_quality_score="6分，背景有些杂乱，主体不突出，光线比较平",
            highlight_feature="女生的背影和书桌上的咖啡杯"
        )
    ],
    overall_visual_summary="整体素材偏向低饱和度的复古风格，色调温暖柔和，适合营造'独处时光'和'精神避难所'的情绪氛围。图片质量较高，构图简洁，但缺乏产品细节展示和场景多样性。"
)

# 创建上游任务并设置 mock 输出
# 注意：这个 Agent 只是用于 mock，不会真正执行，所以需要指定 LLM 避免使用默认配置
visual_agent = Agent(
    role="视觉分析专家",
    goal="分析图片",
    backstory="视觉分析师",
    llm=AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",
    ),
)

upstream_task = Task(
    description="分析用户提供的图片，生成视觉分析报告",
    expected_output="一个完整的 VisualAnalysisReport 结构化输出",
    agent=visual_agent,
    output_pydantic=VisualAnalysisReport,
)

# 设置 mock 输出（关键：必须在创建下游任务之前设置）
upstream_task.output = TaskOutput(
    raw=json.dumps(visual_report.model_dump(), indent=2, ensure_ascii=False),
    description="视觉分析报告",
    agent="视觉分析专家",  # 使用字符串，对应 upstream_task.agent.role
    pydantic=visual_report,
)

# 验证 mock 输出是否设置成功
print("=" * 80)
print("验证 Mock 上游任务输出:")
print("=" * 80)
print(f"upstream_task.output is None: {upstream_task.output is None}")
if upstream_task.output:
    print(f"upstream_task.output.agent: {upstream_task.output.agent}")
    print(f"upstream_task.output.raw 长度: {len(upstream_task.output.raw)} 字符")
    print(f"upstream_task.output.raw 预览: {upstream_task.output.raw[:200]}...")
    print(f"upstream_task.output.pydantic: {type(upstream_task.output.pydantic).__name__}")
print()


# ==============================================================================
# Task 定义：内容策划任务
# ==============================================================================
# 本 Task 展示了"契约驱动"的任务设计：
# 1. output_pydantic=ContentStrategyBrief：指定输出必须符合 ContentStrategyBrief 模型
# 2. context=[upstream_task]：指定任务依赖，可以访问上游任务的输出
# 3. description 中明确说明需要基于上游任务的输出进行分析

task_content_strategy = Task(
    description="""
    **任务要求**：
    1. 仔细分析视觉报告中的用户意图、图片质量和整体风格
    2. 基于 CES 算法和反漏斗模型，制定精准的内容策略
    3. 策略要具体可执行，不能泛泛而谈
    4. 使用 IntermediateTool 工具保存中间思考过程
    
    **重要提示**：
    - 必须基于上游任务的视觉分析报告进行分析（已通过 context 传递）
    - 上游任务输出包含：user_raw_intent、analyzed_images、overall_visual_summary
    - 策略要符合小红书平台的算法特点
    - 所有输出必须使用中文
    """,
    expected_output="一个完整的 ContentStrategyBrief 结构化输出，包含所有必填字段。",
    agent=content_strategist,
    output_pydantic=ContentStrategyBrief,
    context=[upstream_task],
)


# ==============================================================================
# 执行任务
# ==============================================================================
# Crew.kickoff() 会自动处理 context，从上游任务的 output 中获取数据
# 这是"契约驱动"的体现：下游任务依赖上游任务的输出格式

crew = Crew(
    agents=[content_strategist],
    tasks=[task_content_strategy],
    process=Process.sequential,
    verbose=True,
)

# 在执行前再次验证 context 设置
print("=" * 80)
print("验证任务 Context 设置:")
print("=" * 80)
print(f"task_content_strategy.context: {task_content_strategy.context}")
if task_content_strategy.context:
    for ctx_task in task_content_strategy.context:
        print(f"  - Context task: {ctx_task.description}")
        print(f"    Context task.output is None: {ctx_task.output is None}")
        if ctx_task.output:
            print(f"    Context task.output.raw 长度: {len(ctx_task.output.raw)} 字符")
            print(f"    Context task.output.agent: {ctx_task.output.agent}")
        else:
            print("    ⚠️ 警告：Context task.output 为 None！")
            print("    这会导致 Agent 无法接收到上游任务的输出。")
print()

# 验证通过后执行
if upstream_task.output is None:
    raise ValueError("❌ 错误：upstream_task.output 未设置！请确保在创建下游任务之前设置 mock 输出。")

result = crew.kickoff()
print("\n" + "="*80)
print("执行结果:")
print("="*80)
print(result)

# 访问结构化输出
if task_content_strategy.output and task_content_strategy.output.pydantic:
    strategy = task_content_strategy.output.pydantic
    print("\n" + "="*80)
    print("结构化输出:")
    print("="*80)
    print(f"素材评估: {strategy.input_evaluation}")
    print(f"目标受众: {strategy.target_audience_persona}")
    print(f"建议标题: {strategy.suggested_title}")
