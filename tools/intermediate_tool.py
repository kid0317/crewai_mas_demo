"""
课程：07｜定义Agent：从"提示词工程"到"人设工程" 辅助工具
Intermediate Tool - 中间结果保存工具

用于在 Agent 执行过程中保存中间的思考产物，支持 Agent 的"慢思考"模式。

功能特点：
- 支持任意类型的输入（字符串、列表、字典等）
- 自动类型转换：将各种类型转换为字符串格式
- 简单易用：Agent 可以直接调用，无需关心类型转换

使用场景：
- Agent 需要分步骤思考时，保存中间结果
- Agent 需要记录思考过程时，保存思考产物
- Agent 需要传递复杂数据结构时，保存结构化数据

学习要点：
- 工具设计：如何设计简单易用的辅助工具
- 类型转换：如何处理不同类型的输入
- Agent 辅助：如何通过工具增强 Agent 的能力
"""
import json
from typing import Any, Union

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, field_validator


class IntermediateToolSchema(BaseModel):
    """Input for IntermediateTool."""

    intermediate_product: Any = Field(
        ..., 
        description=(
            "中间思考产物，需要保存的内容。"
            "支持任意类型：字符串、列表、字典等，会自动转换为字符串格式。"
            "例如：列表 ['item1', 'item2'] 会自动转换为 'item1\\nitem2'"
        )
    )
    
    @field_validator('intermediate_product', mode='before')
    @classmethod
    def convert_to_string(cls, v: Any) -> str:
        """
        将任意类型的输入转换为字符串
        
        转换规则：
        - 字符串：直接返回
        - 列表：使用换行符连接
        - 字典：转换为 JSON 字符串
        - 其他类型：使用 str() 转换
        """
        if isinstance(v, str):
            return v
        elif isinstance(v, list):
            # 列表：使用换行符连接每个元素
            return "\n".join(str(item) for item in v)
        elif isinstance(v, dict):
            # 字典：转换为 JSON 字符串（保持可读性）
            try:
                return json.dumps(v, ensure_ascii=False, indent=2)
            except (TypeError, ValueError):
                # 如果无法序列化为 JSON，使用 str()
                return str(v)
        else:
            # 其他类型：直接转换为字符串
            return str(v)


class IntermediateTool(BaseTool):
    """
    中间结果保存工具
    
    用于在 agent 执行过程中保存中间的思考产物，
    以便后续步骤可以继续使用。
    
    支持任意类型的输入（字符串、列表、字典等），
    会自动转换为字符串格式，无需手动转换。
    """
    name: str = "Save_Intermediate_Product_Tool"
    description: str = (
        "A tool that can be used to save intermediate thinking products "
        "during agent execution. "
        "\n\n"
        "✅ Supports any input type (string, list, dict, etc.) and automatically converts to string format. "
        "You can pass lists, dictionaries, or any other type directly - no need to convert manually. "
        "\n\n"
        "Examples: "
        "- String: 'my text' → saved as 'my text'"
        "- List: ['item1', 'item2'] → saved as 'item1\\nitem2'"
        "- Dict: {'key': 'value'} → saved as JSON string"
    )
    args_schema: type[BaseModel] = IntermediateToolSchema

    def _run(
        self,
        intermediate_product: str,
        **kwargs: Any,
    ) -> str:
        """
        保存中间思考产物
        
        Args:
            intermediate_product: 需要保存的中间思考产物（已自动转换为字符串）
            
        Returns:
            固定的返回字符串
        """
        # 只返回固定字符串
        # 注意：intermediate_product 已经在 validator 中转换为字符串
        return "中间结果已保存， 可以进行下一步Thought"

