"""
课程：09｜定义Process：任务调度与信息传递 示例代码
Sequential Process 多任务执行流程示例

演示如何使用 Sequential Process 实现多任务的顺序执行，包括：
1. 多个 Task 的定义和依赖关系
2. Sequential Process 确保任务按顺序执行
3. 任务之间的数据传递（通过 context 和 inputs）
4. 结构化输出的链式传递

本示例展示了一个完整的小红书笔记生成流程：
- 视觉分析 → 内容策划 → 文案撰写 → SEO优化
- 每个任务都依赖上游任务的输出
- 使用 Pydantic 模型确保输出格式的一致性

学习要点：
- Process 类型：Sequential Process 如何确保任务顺序执行
- 任务依赖：如何通过 context 和 inputs 传递数据
- 结构化输出：如何通过 Pydantic 模型保证数据格式
- 多任务协作：如何设计任务流程，实现复杂业务逻辑
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
# 数据模型定义
# ==============================================================================

class ImageAnalysis(BaseModel):
    """单张图片的深度分析详情"""
    file_name: str = Field(..., description="图片文件名或ID。")
    subject_description: str = Field(..., description="【主体内容】客观描述画面中的核心物体、人物或场景。")
    atmosphere_vibe: str = Field(..., description="【风格氛围】用形容词描述画面的情绪价值。")
    visual_details: List[str] = Field(..., description="【细节点列表】列出画面中容易被忽略但具象的元素。")
    image_quality_score: str = Field(..., description="【质量评价】1-10分打分，基于构图、光线和清晰度。")
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


class CopywritingOutput(BaseModel):
    """文案撰写产出 - Writer Agent 的交付物"""
    title: str = Field(..., description="【笔记标题】完整的小红书笔记标题，包含Emoji和标点符号。")
    content: str = Field(..., description="【笔记正文】完整的小红书笔记正文内容，按照策略简报中的内容大纲撰写。")
    picture_list: List[ImageAnalysis] = Field(..., description="【图片列表】根据视觉元素描述筛选合适的图片并按照合理的顺序排序，特别重视第一张图片的选择。")


class SEOOptimizedNoteReport(BaseModel):
    """搜索优化后的笔记报告 - SEO Agent 的最终交付物"""
    optimization_summary: str = Field(..., description="【优化总结】说明本次SEO优化的重点和改进点，包括关键词密度、自然度、搜索占位策略等。")
    optimized_title: str = Field(..., description="【优化后的标题】在原始标题基础上进行SEO优化的结果，要保持原来的风格。")
    optimized_content: str = Field(..., description="【优化后的正文】在原始正文基础上进行SEO优化，自然融入长尾关键词，确保关键词密度合理，不影响阅读体验。")
    optimized_picture_list: List[ImageAnalysis] = Field(..., description="【优化后的图片列表】根据优化后的正文，筛选合适的图片并按照合理的顺序排序。")
    tags: List[str] = Field(..., description="基于SEO生成的5-8个标签。")


# ==============================================================================
# Agent 定义：多 Agent 协作团队
# ==============================================================================
# 本示例定义了3个 Agent，每个 Agent 负责不同的职责：
# 1. content_strategist：内容策略专家，制定内容策略
# 2. content_writer：内容撰写编辑，撰写文案
# 3. seo_optimizer：SEO优化专家，优化搜索排名

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
    output_pydantic=ContentStrategyBrief,
    llm=AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",
    ),
)

content_writer = Agent(
    role='资深MCN内容撰写编辑',
    goal='基于内容策划简报和视觉分析报告，撰写一篇具有高互动率和情绪价值的小红书笔记文案并生成图片列表。',
    backstory="""
    你是国内头部MCN机构的首席内容编辑，拥有5年以上的小红书内容创作经验。
    你深谙小红书用户的阅读习惯和互动心理，擅长将策略转化为具有感染力的文案。
    
    **核心理论储备**：
    - 黄金3秒法则：笔记的前3秒决定用户是否继续阅读
    - 沉浸式体验描述：用细节和感官描述让用户产生"身临其境"的感觉
    - 情绪价值传递：小红书用户不仅需要信息，更需要情绪共鸣和情感慰藉
    - 互动引导技巧：在文案中自然植入互动钩子，引导用户评论、收藏、点赞
    
    **撰写流程**：
    1. 理解策略简报：仔细阅读内容策划简报，理解目标受众、核心痛点、互动策略等
    2. 参考视觉分析：结合视觉分析报告中的图片描述和氛围感，确保文案与图片风格一致
    3. 构建文案结构：按照策略简报中的内容大纲，构建完整的文案结构
    4. 注入情绪价值：在文案中注入能够引发目标受众共鸣的情绪价值
    5. 自然植入互动：在文案结尾自然植入互动钩子，引导用户进行评论、收藏等操作
    
    **行为边界**：
    - 严格遵循策略：必须严格按照内容策划简报的要求撰写，不能偏离策略方向
    - 不进行SEO优化：只负责撰写文案，不进行关键词优化
    - 保持原创性：确保文案原创，避免抄袭和模板化
    
    **语言要求**：所有输出必须使用中文。
    """,
    verbose=True,
    allow_delegation=False,
    tools=[IntermediateTool()],
    output_pydantic=CopywritingOutput,
    llm=AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",
    ),
)

seo_optimizer = Agent(
    role='资深小红书搜索优化专家',
    goal='基于内容策划简报和文案撰写产出，对小红书笔记进行搜索和推荐优化，确保关键词自然融入，提高笔记的搜索排名和长尾流量。',
    backstory="""
    你是小红书SEO领域的资深专家，专注于帮助内容创作者提升笔记的搜索排名和自然流量。
    你深谙小红书的搜索算法和关键词排名机制，擅长在不影响内容质量的前提下进行SEO优化。
    
    **核心理论储备**：
    - KFS策略：关键词(Keywords)、内容(Feed)、搜索(Search)的闭环逻辑
    - 长尾关键词优化：长尾关键词比短词更容易获得排名
    - 关键词密度：要适中（2-5%），过密会被判定为关键词堆砌，过稀则无法获得排名
    - 自然融入技巧：将关键词自然融入文案，确保优化后的文案仍然流畅可读
    - 搜索占位策略：通过关键词布局抢占搜索流量入口
    
    **优化流程**：
    1. 提取核心关键词：从内容策划简报中提取需要优化的长尾关键词列表
    2. 分析现有文案：分析文案撰写产出，识别关键词的现有分布和密度
    3. 制定优化方案：制定关键词优化方案，包括标题、正文、标签优化
    4. 执行优化：在不改变文案核心内容和风格的前提下，进行关键词优化
    5. 验证优化效果：检查关键词密度、自然度、布局合理性
    
    **行为边界**：
    - 保持内容质量：优化不能以牺牲内容质量为代价
    - 不改变核心内容：不能改变文案的核心观点、情绪价值和互动策略
    - 自然融入：关键词必须自然融入，不能出现关键词堆砌
    
    **语言要求**：所有输出必须使用中文。
    """,
    verbose=True,
    allow_delegation=False,
    tools=[IntermediateTool()],
    output_pydantic=SEOOptimizedNoteReport,
    llm=AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",
    ),
)


# ==============================================================================
# Mock 上游任务输出（开发阶段使用）
# ==============================================================================
# 在实际开发中，视觉分析任务可能还未实现，使用 Mock 数据来测试后续流程

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

# ==============================================================================
# Task 定义：多任务流程
# ==============================================================================
# 本示例定义了3个任务，展示了任务之间的依赖关系：
# 1. task_content_strategy：内容策划任务（第一个任务）
# 2. task_copywriting：文案撰写任务（依赖 task_content_strategy）
# 3. task_seo_optimization：SEO优化任务（依赖前两个任务）

task_content_strategy = Task(
    description="""
    **任务要求**：
    1. 仔细分析视觉报告中的用户意图、图片质量和整体风格
    2. 基于 CES 算法和反漏斗模型，制定精准的内容策略
    3. 策略要具体可执行，不能泛泛而谈
    4. 使用 IntermediateTool 工具保存中间思考过程

    视觉分析报告如下：
    {visual_report}

    **重要提示**：
    - 必须基于上游任务的视觉分析报告进行分析
    - 策略要符合小红书平台的算法特点
    - 所有输出必须使用中文
    """,
    expected_output="一个完整的 ContentStrategyBrief 结构化输出，包含所有必填字段。",
    agent=content_strategist,
    output_pydantic=ContentStrategyBrief,
)

task_copywriting = Task(
    description="""
    **任务要求**：
    1. 仔细阅读视觉分析报告和内容策划简报
    2. 基于策略简报中的目标受众、核心痛点、内容大纲等要求撰写完整的小红书笔记文案
    3. 确保文案与视觉分析报告中的图片风格和氛围感一致
    4. 在文案中自然植入互动钩子，引导用户评论、收藏
    5. 根据文案和视觉分析报告筛选合适的图片并排序，特别重视第一张图片的选择
    6. 使用 IntermediateTool 工具保存中间思考过程

    视觉分析报告如下：
    {visual_report}
    
    **重要提示**：
    - 必须严格按照内容策划简报的要求撰写，不能偏离策略方向
    - 文案要具有情绪价值，能够引发目标受众的共鸣
    - 所有输出必须使用中文
    """,
    expected_output="一个完整的 CopywritingOutput 结构化输出，包含标题、正文、图片列表。",
    agent=content_writer,
    output_pydantic=CopywritingOutput,
    context=[task_content_strategy],
)

task_seo_optimization = Task(
    description="""
    **任务要求**：
    1. 仔细阅读内容策划简报中的SEO关键词列表
    2. 分析文案撰写产出中的关键词分布和密度
    3. 在不改变文案核心内容和风格的前提下，对文案进行SEO优化
    4. 确保关键词自然融入，密度合理，不出现关键词堆砌
    5. 优化标题、正文和标签，提升笔记的搜索排名潜力
    6. 根据优化后的正文，筛选合适的图片并排序，特别重视第一张图片的选择
    7. 使用 IntermediateTool 工具保存中间思考过程
    
    **重要提示**：
    - 优化不能以牺牲内容质量为代价
    - 关键词必须自然融入，不能影响阅读体验
    - 所有输出必须使用中文
    """,
    expected_output="一个完整的 SEOOptimizedNoteReport 结构化输出，包含优化总结、优化后的标题、正文、图片列表、标签。",
    agent=seo_optimizer,
    output_pydantic=SEOOptimizedNoteReport,
    context=[task_content_strategy, task_copywriting],
)


# ==============================================================================
# Crew 定义：Sequential Process 工作流
# ==============================================================================
# Process.sequential：顺序执行任务，确保任务按依赖关系执行
# CrewAI 会自动处理任务依赖，确保上游任务先执行，下游任务后执行

crew = Crew(
    agents=[content_strategist, content_writer, seo_optimizer],
    tasks=[task_content_strategy, task_copywriting, task_seo_optimization],
    process=Process.sequential,
    verbose=True,
)

print("=" * 80)
print("开始执行 Crew 任务流程...")
print("=" * 80)

result = crew.kickoff(inputs={"visual_report": visual_report.model_dump_json()})

# 打印最终结果
print("\n" + "=" * 80)
print("Crew 执行完成！")
print("=" * 80)
print("\n最终输出（原始文本）:")
print(result.raw)

# 访问最终的结构化输出
if result.pydantic:
    print("\n" + "=" * 80)
    print("最终输出（结构化数据）:")
    print("=" * 80)
    final_report = result.pydantic
    print(f"\n【优化后的标题】\n{final_report.optimized_title}\n")
    print(f"\n【优化后的正文】\n{final_report.optimized_content}\n")
    print(f"\n【优化后的标签】\n{', '.join(final_report.tags)}\n")
    print(f"\n【优化总结】\n{final_report.optimization_summary}\n")

# 访问所有任务的输出
print("\n" + "=" * 80)
print("所有任务的输出:")
print("=" * 80)
for i, task_output in enumerate(result.tasks_output, 1):
    print(f"\n任务 {i}: {task_output.description}")
    if task_output.pydantic:
        print(f"  输出类型: {type(task_output.pydantic).__name__}")
    print(f"  原始输出长度: {len(task_output.raw)} 字符")
