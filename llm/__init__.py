"""
课程：06｜工欲善其器：课程学习的基础代码环境准备
LLM 模块

提供自定义 LLM 实现，支持阿里云通义千问等国内大模型接口。

主要组件：
- AliyunLLM：阿里云通义千问 LLM 实现
"""
from . import aliyun_llm
from .aliyun_llm import AliyunLLM

__all__ = ['AliyunLLM', 'aliyun_llm']

