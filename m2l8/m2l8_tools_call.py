"""
课程：13｜自定义工具封装：构建 Tools 的五步标准SOP 示例代码
工具调用 Hook 示例

演示如何使用 CrewAI 的 Hook 机制拦截和修改工具调用，实现：
1. 工具调用前的拦截（before_tool_call）
2. 上下文信息的使用（user_id、task_id）
3. 文件路径的安全校验和重定向
4. 多租户工作空间隔离

本示例展示了：
- Hook 机制：如何在工具调用前后执行自定义逻辑
- 上下文管理：如何使用上下文变量获取用户信息
- 安全控制：如何防止路径穿越攻击
- 多租户隔离：如何为不同用户创建独立的工作空间

学习要点：
- Hook 装饰器：@before_tool_call 和 @after_tool_call 的使用
- 上下文变量：如何在 Hook 中使用 contextvars
- 安全实践：如何防止路径穿越等安全漏洞
- 多租户设计：如何实现用户数据隔离
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径，以便能够导入项目模块
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from crewai import Agent, Task, Crew
from llm import aliyun_llm
from crewai_tools import ScrapeWebsiteTool, FileWriterTool, FileReadTool
from crewai.hooks import before_tool_call, after_tool_call
from m2l8_context import user_id, task_id

# 工作空间基础路径：所有用户的工作空间都基于此路径
WORKSPACE_BASE_PATH = Path("./workspace").resolve()


# ==============================================================================
# Hook 定义：文件路径安全校验和重定向
# ==============================================================================
# @before_tool_call：在工具调用前执行，可以修改工具输入或阻止工具调用
# 本 Hook 实现了：
# 1. 检查 user_id 是否存在（多租户必需）
# 2. 为每个用户创建独立的工作空间目录
# 3. 校验文件路径，防止路径穿越攻击
# 4. 将文件路径重定向到用户的工作空间

@before_tool_call
def file_path_hook(context):
    tools_list = ["File Writer Tool", "Read a file's content"]

    if context.tool_name in tools_list:
        print(f"工具调用：{context.tool_name}")
        print(f"工具输入：{context.tool_input}")
        # 检查 user_id 是否存在
        uid = user_id.get()
        if uid is None :
            print(f"缺少必要的上下文信息：user_id={uid}")
            context.tool_result = f"缺少必要的上下文信息：user_id={uid}"
            return False
        
        # 使用 Path 对象正确拼接路径
        base_path = WORKSPACE_BASE_PATH / uid
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)
        
        original_file_path = ""
        if context.tool_name == "Read a file's content":
            original_file_path = context.tool_input.get('file_path', '')
        elif context.tool_name == "File Writer Tool":
            original_file_path = context.tool_input.get('filename', '')
        if not original_file_path:
            print(f"文件路径不能为空")
            context.tool_result = "文件路径不能为空"
            return False
        
        # 对于路径进行校验，防止通过..等目录穿越攻击导致目录穿越
        # 获取原始文件路径的绝对路径
        original_file_path_abs = Path(original_file_path).resolve()
        base_path_abs = base_path.resolve()
        
        # 如果原始文件路径的绝对路径已经在工作空间目录下，直接使用
        try:
            # 使用 Path 的 relative_to 方法检查路径是否在 base_path 下
            original_file_path_abs.relative_to(base_path_abs)
            # 如果成功，说明路径在工作空间内
            if context.tool_name == "Read a file's content":
                context.tool_input['file_path'] = str(original_file_path_abs)
            elif context.tool_name == "File Writer Tool":
                context.tool_input['filename'] = str(original_file_path_abs)
            
            print(f"校验后的工具输入：{context.tool_input}")
            return None
        except ValueError:
            # 如果不在工作空间内，尝试拼接工作空间目录和原始文件路径
            new_file_path = base_path / original_file_path
            new_file_path_abs = new_file_path.resolve()
            
            # 检查拼接后的路径是否在工作空间内（防止目录穿越攻击）
            try:
                new_file_path_abs.relative_to(base_path_abs)
                # 如果成功，使用拼接后的路径
                if context.tool_name == "Read a file's content":
                    context.tool_input['file_path'] = str(new_file_path_abs)
                elif context.tool_name == "File Writer Tool":
                    context.tool_input['filename'] = str(new_file_path_abs)
                
                print(f"校验后的工具输入：{context.tool_input}")
            except ValueError:
                # 路径不在工作空间内，拒绝访问
                context.tool_result = f"非法的路径：{original_file_path}（路径超出工作空间范围）"
                print(f"非法的路径：{original_file_path}（路径超出工作空间范围）")
                return False
    return None  # 返回 None 表示继续执行工具调用


# ==============================================================================
# Agent 定义：定时任务管理专家
# ==============================================================================
# 本 Agent 展示了如何使用文件操作工具管理定时任务
# 通过 Hook 机制，所有文件操作都会自动重定向到用户的工作空间

crontab_manager_agent = Agent(
    role = "定时任务管理专家",
    goal = "根据用户需求，记录和维护定时任务情况",
    backstory = f"""
    你是一位定时任务记录专家，擅长记录和管理需要长期执行的定时任务。

    你十分熟悉的掌握以下能力：
    Crontab 是一种通过特定的语法定义时间规则来自动执行命令或脚本。其语法由5个时间字段（分、时、日、月、周）和1个命令字段组成，支持*（任意）、,（枚举）、-（范围）和*/n（间隔）等特殊字符。 
    核心语法格式：
    ```
    # 分 时 日 月 周 命令
    *  *  *  *  *  command
    ```
    其中时间字段说明 
    字段	含义	范围	特殊字符
    M	分钟 (Minute)	0-59	*, -, ,, /
    H	小时 (Hour)	0-23	*, -, ,, /
    D	日期 (Day of Month)	1-31	*, -, ,, /
    m	月份 (Month)	1-12	*, -, ,, /
    d	星期 (Day of Week)	0-7	0和7均为星期日

    特殊操作符详解：
    * (星号)：代表“每”的含义。例如，在月字段中代表每个月。
    , (逗号)：分隔多个不连续的数值。例如，周字段为 1,3,5 表示周一、周三、周五。
    - (减号)：代表连续的范围。例如，时字段为 9-17 表示上午9点到下午5点。
    / (斜杠)：代表每隔多少个单位执行一次。例如，分字段为 */10 表示每隔10分钟。

    常用示例：
    每分钟执行：* * * * * command
    每5分钟执行：*/5 * * * * command
    每小时第0分执行：0 * * * * command
    每天凌晨2点执行：0 2 * * * command
    每周一上午8:30执行：30 8 * * 1 command
    每月1号凌晨0点执行：0 0 1 * * command

    你通常的工作方法包括：
    1、你会根据用户的需求，生成符合crontab语法的定时任务，并写入到CRONTAB.md文件中，如果文件不存在则创建一个。
    其中CRONTAB.md文件的格式为：一行一个的定时任务，每行定时任务的格式符合crontab语法，其中command字段用json格式表式；
    示例： * * * * * {{"task_name":"任务名称", "task_description"："任务描述", "expected_output"："预期输出"}}
    2、当用户询问或者想要更改、删除定时任务时，你会读取CRONTAB.md文件，如果文件不存在则表示没有定时任务，根据用户需求，回答用户的问题或者调整CRONTAB.md文件中的定时任务。
    3、当你回答用户问题和描述任务情况时，你要尽量使用文字描述，回答的语句对用户友好。你也可以用markdown表格形式描述任务情况。

    注意：
    你不会去具体执行定时任务，你只负责记录和维护定时任务情况。
    """,
    tools = [FileWriterTool(), FileReadTool()],
    verbose = True,
    allow_delegation = False,
    llm = aliyun_llm.AliyunLLM(
        model = "qwen-plus",
        api_key = os.getenv("QWEN_API_KEY"),
        region = "cn",
    ),
)

# ==============================================================================
# 设置上下文变量（模拟多租户场景）
# ==============================================================================
# 在实际应用中，user_id 应该从请求中获取（如 JWT token、session 等）
# 这里使用固定值模拟，实际使用时需要从请求上下文中获取

user_id.set("1234567890")


# ==============================================================================
# Task 定义：定时任务管理任务
# ==============================================================================

base_task = Task(
    description = "根据用户的需求，完成对定时任务的记录和维护。用户的输入为：{user_input}",
    expected_output = "满足用户需求后，对用户的友好答复",
    agent = crontab_manager_agent,
)
# ==============================================================================
# Crew 定义：定时任务管理工作流
# ==============================================================================

crew = Crew(
    agents=[crontab_manager_agent],
    tasks=[base_task],
    verbose=True,
)


# ==============================================================================
# 执行任务：多轮对话示例
# ==============================================================================
# 本示例展示了多轮对话的场景：
# 1. 第一轮：创建定时任务
# 2. 第二轮：查询定时任务列表
# 3. 第三轮：修改定时任务
# 通过 user_id 上下文变量，确保每轮对话都在同一个用户的工作空间中操作

result = crew.kickoff(inputs={"user_input": "帮我创建一个周一到周五每天早上9点的任务，查询阿里港股的股价信息，以及一周内阿里相关的最新资讯，发送到我的qq。"})
print(result)

result = crew.kickoff(inputs={"user_input": "查一下我现在的定时任务"})
print(result)

result = crew.kickoff(inputs={"user_input": "帮我把查询阿里股价的任务改到9点半"})
print(result)