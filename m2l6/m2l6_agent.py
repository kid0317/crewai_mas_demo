"""
课程：10｜多模态模型：让你的Agent拥有"眼睛" 示例代码
多模态视觉分析示例

演示如何使用多模态 Agent 分析本地图片，生成结构化的视觉分析报告。

本示例展示了：
1. 多模态 Agent 配置：如何使用 AddImageToolLocal 处理本地图片
2. 图片处理流程：读取本地文件 → 转换为 Base64 → 传递给多模态模型
3. 结构化输出：使用 Pydantic 模型定义视觉分析报告的结构
4. 中间思考保存：使用 IntermediateTool 保存 Agent 的思考过程
5. Agent 人设优化：如何通过 backstory 塑造专业的视觉分析师

适用场景：
- 产品图片质量评估
- 视觉内容分析
- 图片素材筛选
- 小红书笔记配图分析

学习要点：
- 多模态能力：如何让 Agent 具备"看"的能力
- 图片处理：如何将本地图片转换为模型可处理的格式
- 结构化输出：如何定义视觉分析的结构化数据格式
- 工具集成：如何集成图片处理工具到 Agent 中
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
from tools.add_image_tool_local import AddImageToolLocal
from tools.intermediate_tool import IntermediateTool
from typing import List


# ==============================================================================
# 数据模型定义
# ==============================================================================

class ImageAnalysis(BaseModel):
    """
    单张图片的深度分析详情
    
    用于结构化输出图片分析的各个维度信息，包括主体内容、风格氛围、
    视觉细节、质量评分和突出特点等。
    """
    file_name: str = Field(..., description="图片文件名或ID，用于标识图片。")
    subject_description: str = Field(
        ..., 
        description="【主体内容】客观描述画面中的核心物体、人物或场景，要求详细准确，不遗漏关键元素。"
    )
    atmosphere_vibe: str = Field(
        ..., 
        description="【风格氛围】用形容词描述画面的情绪价值和整体氛围感，例如：静谧、复古、松弛感、治愈、精致等。"
    )
    visual_details: List[str] = Field(
        ..., 
        description="【细节点列表】列出画面中容易被忽略但具象的元素，至少3个，这些细节可以作为后续笔记撰写的素材。"
    )
    image_quality_score: str = Field(
        ..., 
        description="【质量评价】1-10分打分，基于构图、光线和清晰度三个维度，并给出打分的原因和具体评价。"
    )
    highlight_feature: str = Field(
        ..., 
        description="【突出特点】这张图最抓人眼球的一个视觉锚点（Visual Hook），是用户第一眼看到图片时最容易被吸引的元素。"
    )


# ==============================================================================
# 图片路径处理
# ==============================================================================

# 获取图片绝对路径（图片在当前脚本目录下）
script_dir = Path(__file__).parent
image_path = (script_dir / "20260129172715_135_6.jpg").resolve()

# 检查图片是否存在
if not image_path.exists():
    print(f"❌ 错误：图片文件不存在: {image_path}")
    print(f"请确保图片文件位于: {script_dir}")
    exit(1)

print(f"✅ 图片路径: {image_path}")


# ==============================================================================
# Agent 定义：多模态视觉分析师
# ==============================================================================
# 本 Agent 展示了如何配置多模态能力：
# 1. tools=[AddImageToolLocal()]：使用本地图片加载工具
# 2. output_pydantic=ImageAnalysis：指定结构化输出格式
# 3. image_model="qwen3-vl-plus"：指定多模态模型
# 4. multimodal=False：使用 AddImageToolLocal 时无需设置 multimodal=True

image_analyst = Agent(
    role="资深小红书笔记MCN机构视觉分析师",
    goal="分析本地产品图片，提供详细、专业、结构化的视觉分析报告，为后续内容创作提供视觉素材评估和选择依据。",
    backstory="""
    你是一位拥有8年以上经验的产品视觉分析师，曾服务于国内头部MCN机构和小红书内容创作团队。
    你深谙小红书平台的视觉内容标准和用户审美偏好，擅长从商业和内容创作的角度分析图片。
    
    **核心理论储备**：
    - 视觉锚点理论（Visual Hook）：图片中能够第一时间抓住用户注意力的元素
    - 情绪价值传递：图片不仅要展示产品，更要传递情绪和氛围感
    - 小红书视觉标准：构图简洁、光线柔和、色彩协调、细节丰富
    - 质量评估维度：构图（30%）、光线（30%）、清晰度（20%）、色彩（20%）
    
    **分析流程**：
    1. 整体观察：首先观察图片的整体构图、色调和氛围感
    2. 主体识别：识别图片中的核心主体（产品、人物、场景等）
    3. 细节挖掘：寻找画面中容易被忽略但具有价值的细节元素
    4. 质量评估：从构图、光线、清晰度三个维度进行客观评分
    5. 视觉锚点：识别最能吸引用户注意力的视觉元素
    
    **分析原则**：
    - 客观性：描述要客观准确，不夸大不贬低
    - 专业性：使用专业的视觉分析术语
    - 实用性：分析结果要能为后续内容创作提供实际指导
    - 细节性：不遗漏关键细节，这些细节可能是内容创作的素材
    
    **行为边界**：
    - 只负责视觉分析，不进行内容策划或文案撰写
    - 分析要基于图片本身，不进行过度解读
    - 评分要客观公正，给出明确的评分依据
    
    **语言要求**：所有思考过程、工具调用和最终输出都必须使用中文。
    """,
    verbose=True,
    allow_delegation=False,
    tools=[AddImageToolLocal()],  #  本地图片（读文件转 Base64）
    output_pydantic=ImageAnalysis,  # 指定结构化输出模型
    multimodal=False,  # 使用 AddImageToolLocal 替代默认 AddImageTool，无需 multimodal=True
    llm=AliyunLLM(
        image_model="qwen3-vl-plus",
        model="qwen-plus",  # 使用支持多模态的模型
        api_key=os.getenv("QWEN_API_KEY"),
        region="cn",
    ),
)


# ==============================================================================
# Task 定义：图片分析任务
# ==============================================================================
# 本 Task 展示了多模态任务的定义方式：
# 1. description 中明确说明需要使用 AddImageToolLocal 加载图片
# 2. expected_output 中说明需要输出的结构化数据格式
# 3. output_pydantic 指定输出必须符合 ImageAnalysis 模型

task_image_analysis = Task(
    description=f"""
    **任务要求**：
    1. 使用 Add image to content Local 加载并分析本地图片：{image_path}
    2. 如果用户提供了图片内容，直接读取图片内容
    3. 仔细观察图片的各个维度，包括构图、光线、色彩、细节等
    4. 按照 ImageAnalysis 模型的要求，提供详细、专业的分析报告
    
    **分析维度**：
    1. **主体内容描述**：
       - 客观描述画面中的核心物体、人物或场景
       - 要求详细准确，不遗漏关键元素
       - 描述要具体，避免泛泛而谈
    
    2. **风格氛围分析**：
       - 用形容词描述画面的情绪价值和整体氛围感
       - 例如：静谧、复古、松弛感、治愈、精致、温暖等
       - 要能体现图片传递的情绪价值
    
    3. **视觉细节挖掘**：
       - 列出画面中容易被忽略但具象的元素
       - 至少列出3个细节，这些细节可以作为后续笔记撰写的素材
       - 细节要具体，例如："书页上的光斑"、"杯口边缘的咖啡渍"等
    
    4. **质量评估**：
       - 从构图、光线、清晰度三个维度进行1-10分打分
       - 给出每个维度的具体评分和评分依据
       - 提供综合评分和总体评价
    
    5. **视觉锚点识别**：
       - 识别这张图最抓人眼球的一个视觉锚点（Visual Hook）
       - 这是用户第一眼看到图片时最容易被吸引的元素
       - 要说明为什么这个元素能够成为视觉锚点
    
    **重要提示**：
    - 必须使用 AddImageToolLocal 加载图片（图片路径已提供）
    - 如果图片内容加载失败，直接返回错误，不要自己瞎编
    - 分析要客观专业，不进行过度解读
    - 使用 IntermediateTool 保存中间思考过程
    - 所有输出必须使用中文
    - 确保输出符合 ImageAnalysis 模型的所有字段要求
    """,
    expected_output=f"""
    一个完整的 ImageAnalysis 结构化输出，包含：
    - file_name: 图片文件名
    - subject_description: 详细的主体内容描述
    - atmosphere_vibe: 风格氛围描述
    - visual_details: 至少3个视觉细节列表
    - image_quality_score: 质量评分和评分依据
    - highlight_feature: 视觉锚点描述
    可参考以下示例：
    {{"file_name":"xx.jpg","subject_description":"xx","atmosphere_vibe":"xx","visual_details":["xx","xx","xx"],"image_quality_score":"xx","highlight_feature":"xx"}}
    """,
    agent=image_analyst,
    output_pydantic=ImageAnalysis,
)


# ==============================================================================
# Crew 定义：多模态分析工作流
# ==============================================================================
# 虽然只有一个任务，但展示了多模态 Agent 的完整工作流程

crew = Crew(
    agents=[image_analyst],
    tasks=[task_image_analysis],
    process=Process.sequential,  # 顺序执行（虽然只有一个任务，但保持一致性）
    verbose=True,
)

print("=" * 80)
print("开始执行多模态视觉分析任务...")
print("=" * 80)
print(f"图片路径: {image_path}")
print(f"Agent: {image_analyst.role}")
print(f"模型: qwen3-vl-plus")
print("=" * 80)

try:
    result = crew.kickoff(inputs={"image_path": str(image_path)})
    
    # 打印执行完成信息
    print("\n" + "=" * 80)
    print("任务执行完成！")
    print("=" * 80)
    
    # 打印原始输出
    print("\n【原始输出】")
    print("-" * 80)
    print(result.raw)
    
    # 打印结构化输出
    if result.pydantic:
        print("\n" + "=" * 80)
        print("结构化输出（ImageAnalysis）")
        print("=" * 80)
        analysis = result.pydantic
        
        print(f"\n【图片文件名】\n{analysis.file_name}\n")
        print(f"【主体内容描述】\n{analysis.subject_description}\n")
        print(f"【风格氛围】\n{analysis.atmosphere_vibe}\n")
        print(f"【视觉细节列表】")
        for i, detail in enumerate(analysis.visual_details, 1):
            print(f"  {i}. {detail}")
        print(f"\n【质量评分】\n{analysis.image_quality_score}\n")
        print(f"【视觉锚点】\n{analysis.highlight_feature}\n")
        
        # 打印 JSON 格式的结构化数据（便于后续使用）
        print("=" * 80)
        print("JSON 格式输出（便于后续使用）")
        print("=" * 80)
        print(json.dumps(analysis.model_dump(), indent=2, ensure_ascii=False))
    
    # 打印任务输出信息
    print("\n" + "=" * 80)
    print("任务输出详情")
    print("=" * 80)
    for i, task_output in enumerate(result.tasks_output, 1):
        print(f"\n任务 {i}: {task_output.description}")
        if task_output.pydantic:
            print(f"  输出类型: {type(task_output.pydantic).__name__}")
        print(f"  原始输出长度: {len(task_output.raw)} 字符")
        
except Exception as e:
    print(f"\n❌ 执行出错：{e}")
    import traceback
    traceback.print_exc()
    exit(1)

