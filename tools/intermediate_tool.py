"""
Intermediate Tool

用于在 agent 执行中保存中间的思考产物。
"""
from typing import Any

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class IntermediateToolSchema(BaseModel):
    """Input for IntermediateTool."""

    intermediate_product: str = Field(..., description="中间思考产物，需要保存的内容")


class IntermediateTool(BaseTool):
    """
    中间结果保存工具
    
    用于在 agent 执行过程中保存中间的思考产物，
    以便后续步骤可以继续使用。
    """
    name: str = "Save_Intermediate_Product_Tool"
    description: str = (
        "A tool that can be used to save intermediate thinking products "
        "during agent execution."
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
            intermediate_product: 需要保存的中间思考产物
            
        Returns:
            固定的返回字符串
        """
        # 只返回固定字符串
        return "中间结果已保存， 可以进行下一步Thought"

