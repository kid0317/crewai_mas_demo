"""
课程：13｜自定义工具封装：构建 Tools 的五步标准SOP 示例代码
修复版本的 DirectoryReadTool

修复了原 CrewAI DirectoryReadTool 中当 directory 为 "." 时，
文件名中的点号被错误替换的问题。

问题说明：
- 原版本使用 replace() 方法处理路径，导致文件名中的点号被错误替换
- 本版本使用 os.path.relpath() 正确处理相对路径

修复方法：
- 使用 os.path.relpath() 计算相对路径
- 正确处理当前目录（"."）的情况
- 保持路径格式的一致性

学习要点：
- 工具修复：如何修复现有工具的问题
- 路径处理：如何正确处理文件路径
- 兼容性：如何保持与原有工具的兼容性
"""
import os
from typing import Any
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class FixedDirectoryReadToolSchema(BaseModel):
    """Input for FixedDirectoryReadTool."""


class DirectoryReadToolSchema(FixedDirectoryReadToolSchema):
    """Input for FixedDirectoryReadTool."""

    directory: str = Field(..., description="Mandatory directory to list content")


class FixedDirectoryReadTool(BaseTool):
    """
    修复版本的目录读取工具
    
    修复了原 DirectoryReadTool 中当 directory 为 "." 时，
    文件名中的点号被错误替换的问题。
    """
    name: str = "List files in directory"
    description: str = (
        "A tool that can be used to recursively list a directory's content."
    )
    args_schema: type[BaseModel] = DirectoryReadToolSchema
    directory: str | None = None

    def __init__(self, directory: str | None = None, **kwargs):
        super().__init__(**kwargs)
        if directory is not None:
            self.directory = directory
            self.description = f"A tool that can be used to list {directory}'s content."
            self.args_schema = FixedDirectoryReadToolSchema
            self._generate_description()

    def _run(
        self,
        **kwargs: Any,
    ) -> Any:
        directory: str | None = kwargs.get("directory", self.directory)
        if directory is None:
            raise ValueError("Directory must be provided.")

        # 规范化目录路径
        directory = os.path.normpath(directory)
        if directory.endswith("/"):
            directory = directory[:-1]
        
        # 获取目录的绝对路径，用于计算相对路径
        abs_directory = os.path.abspath(directory)
        
        # 使用 os.path.relpath 来正确处理相对路径
        # 这样可以避免 replace() 方法错误替换点号的问题
        files_list = []
        for root, dirs, files in os.walk(directory):
            for filename in files:
                # 获取完整文件路径
                full_path = os.path.join(root, filename)
                abs_full_path = os.path.abspath(full_path)
                
                # 使用 os.path.relpath 获取相对于 directory 的路径
                rel_path = os.path.relpath(abs_full_path, abs_directory)
                
                # 如果 directory 不是当前目录，需要加上目录前缀
                if directory != "." and directory != os.path.curdir:
                    # 确保路径格式统一使用 "/"
                    file_path = os.path.join(directory, rel_path).replace(os.path.sep, "/")
                else:
                    # 对于当前目录，直接使用相对路径
                    file_path = rel_path.replace(os.path.sep, "/")
                
                files_list.append(file_path)
        
        # 格式化输出
        files = "\n- ".join(files_list)
        return f"File paths: \n- {files}"

