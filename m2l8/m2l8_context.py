"""
课程：13｜自定义工具封装：构建 Tools 的五步标准SOP 示例代码
API 请求级上下文管理

演示如何使用 Python 的 contextvars 模块管理 API 请求级的上下文信息。
这在多租户、多用户场景中非常重要，可以确保每个请求的上下文信息隔离。

本示例定义了三个上下文变量：
- user_id：用户ID，用于标识当前请求的用户
- request_id：请求ID，用于追踪请求链路
- task_id：任务ID，用于标识当前执行的任务

使用场景：
- 多租户系统：每个用户的数据隔离
- 请求追踪：通过 request_id 追踪请求链路
- 任务管理：通过 task_id 管理任务状态

学习要点：
- ContextVar：Python 的上下文变量，线程安全，支持异步
- 上下文隔离：如何确保不同请求的上下文信息不互相干扰
- Hook 集成：如何在 CrewAI 的 Hook 中使用上下文变量
"""

# 定义 API 请求级的上下文变量
# 使用 contextvars 模块，确保每个请求的上下文信息隔离
from contextvars import ContextVar
from typing import Optional

# 用户ID上下文变量：标识当前请求的用户
user_id = ContextVar[Optional[str]]("user_id", default=None)

# 请求ID上下文变量：用于追踪请求链路
request_id = ContextVar[Optional[str]]("request_id", default=None)

# 任务ID上下文变量：标识当前执行的任务
task_id = ContextVar[Optional[str]]("task_id", default=None)
