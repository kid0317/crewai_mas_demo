"""
课程：06｜工欲善其器：课程学习的基础代码环境准备 示例代码
LLM 配置示例（OpenAI 兼容接口）

演示如何使用 CrewAI 的 LLM 类配置大模型接口。
本示例展示了如何配置 OpenAI 兼容的 API 接口（如 DeepSeek、Kimi 等）。

注意：本课程主要使用阿里云通义千问，此文件仅作为 LLM 配置的参考示例。
实际项目中请使用 llm/aliyun_llm.py 中的 AliyunLLM 实现。
"""

from crewai import LLM, Agent, Task
import os

# ==============================================================================
# LLM 配置示例
# ==============================================================================
# 使用 CrewAI 的 LLM 类配置 OpenAI 兼容接口
# 适用于：DeepSeek、Kimi、OpenAI 等支持 OpenAI 格式的 API

llm = LLM(
    model="qwen-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),  # API 基础地址
)

# ==============================================================================
# LLM 直接调用示例
# ==============================================================================
# 演示如何直接调用 LLM，不通过 Agent

prompt = "What is the capital of France?"
response = llm.call([{"role": "user", "content": prompt}])
print(response)


# ==============================================================================
# Agent 使用 LLM 示例
# ==============================================================================
# 演示如何将配置好的 LLM 传递给 Agent

agent = Agent(
    role="Assistant",
    goal="Answer the question",
    backstory="You are a helpful assistant that can answer questions.",
    llm=llm,
    verbose=True,
)

task = Task(
    description="Answer the question",
    expected_output="The capital of France is Paris.",
    agent=agent,
)

result = agent.execute_task(task)
print(result)