"""
课程：02｜解构智能体：Agent 的解剖学与 ReAct 范式 示例代码
原生 Agent 实现（不使用 CrewAI 框架）

这是一个教学示例，展示 Agent 的核心工作原理和 ReAct 范式：
1. 循环调用 LLM，让 LLM 进行推理（Reasoning）
2. 解析 LLM 返回的 Action（工具名称和输入参数）
3. 执行工具（Acting）
4. 将工具结果作为 Observation 返回给 LLM
5. 重复上述步骤，直到得到 Final Answer

本示例帮助学员理解：
- Agent 的本质：一个不断调用 LLM 和执行工具的循环
- ReAct 范式：Reasoning（推理）→ Acting（行动）→ Observation（观察）的循环
- 工具调用机制：如何解析 LLM 的输出并执行相应的工具
- 对话历史管理：如何维护 LLM 的上下文，让 Agent 能够"记住"之前的操作

通过这个示例，学员可以深入理解 CrewAI 等框架的底层实现原理。
"""
from llm.aliyun_llm import AliyunLLM
import os
import json
from typing import Dict, Callable


class RawAgent:
    """
    原生 Agent 实现（不使用 CrewAI 框架）
    
    这是一个教学示例，展示 Agent 的核心工作流程：
    - 接收任务描述
    - 通过循环调用 LLM 和工具来完成任务
    - 返回最终答案
    
    Args:
        role: Agent 的角色描述
        goal: Agent 的目标
        backstory: Agent 的背景故事
        tools: 工具字典，key 是工具名称，value 是工具函数（Callable）
    """
    
    def __init__(self, role: str, goal: str, backstory: str, tools: Dict[str, Callable]):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools  # 工具字典：工具名 -> 工具函数

    def run(self, description: str, expected_output: str) -> str:
        """
        执行任务的主循环
        
        这是 Agent 的核心：一个 while 循环，不断调用 LLM 和执行工具，
        直到 LLM 返回 "Final Answer" 为止。
        
        Args:
            description: 任务描述
            expected_output: 期望的输出格式
            
        Returns:
            最终答案字符串
        """
        # 1. 生成系统提示词和用户提示词
        system_prompt = self.generate_system_prompt()
        user_prompt = self.generate_user_prompt(description, expected_output)
        
        # 2. 初始化消息列表（对话历史）
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # 3. 初始化 LLM
        llm = AliyunLLM(
            model="qwen-turbo",
            api_key=os.getenv("QWEN_API_KEY"),
            region="cn",  # 使用 region 参数，可选值: "cn", "intl", "finance"
        )
        
        # 4. 核心循环：不断调用 LLM，直到得到 Final Answer
        response = llm.call(messages, stop=["Observation:"])
        
        while "Final Answer:" not in response:
            # 4.1 解析 LLM 返回的 Action（工具名称和输入）
            tool_name = self.parse_tool_name(response)
            tool_input = self.parse_tool_input(response)
            
            # 4.2 执行工具，获取结果
            tool_result = self.execute_tool(tool_name, tool_input)
            
            # 4.3 将工具执行结果作为 Observation 添加到对话历史
            # 格式：之前的 response + "\nObservation:" + 工具结果
            content = response + "\nObservation:" + tool_result
            messages.append({"role": "assistant", "content": content})
            
            # 4.4 再次调用 LLM，传入包含 Observation 的完整对话历史
            response = llm.call(messages, stop=["Observation:"])
        
        # 5. 提取并返回最终答案
        final_answer = self.extract_final_answer(response)
        return final_answer

    def generate_system_prompt(self) -> str:
        """
        生成系统提示词
        
        从模板文件读取，并填充 Agent 的角色、目标、背景故事和可用工具信息。
        
        Returns:
            格式化后的系统提示词
        """
        # 读取提示词模板文件（相对于当前文件所在目录）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "agent_system_prompt.txt")
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # 构建工具信息字符串
        tools_map = ""  # 工具详细描述
        tools_name = ""  # 工具名称列表
        for name, tool_func in self.tools.items():
            # 获取工具的描述（如果有 docstring）
            tool_desc = tool_func.__doc__ or "无描述"
            tools_map += f"Tool Name: {name}\nTool Description: {tool_desc}\n\n"
            tools_name += f"{name}, "
        
        # 格式化模板，填充变量
        return template.format(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools_map=tools_map,
            tools_name=tools_name.rstrip(", ")  # 去掉最后的逗号和空格
        )

    def generate_user_prompt(self, description: str, expected_output: str) -> str:
        """
        生成用户提示词
        
        从模板文件读取，并填充任务描述和期望输出。
        
        Args:
            description: 任务描述
            expected_output: 期望的输出格式
            
        Returns:
            格式化后的用户提示词
        """
        # 读取提示词模板文件
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "agent_user_prompt.txt")
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        return template.format(description=description, expected_output=expected_output)

    def parse_tool_name(self, response: str) -> str:
        """
        从 LLM 响应中解析工具名称
        
        LLM 返回格式示例：
        ```
        Thought: 我需要搜索信息
        Action: baidu_search
        Action Input: {"query": "Python"}
        ```
        
        Args:
            response: LLM 的响应文本
            
        Returns:
            工具名称（去除首尾空格）
            
        Raises:
            ValueError: 如果响应中不包含 "Action:" 字段
        """
        if "Action: " not in response:
            raise ValueError(f"响应中未找到 Action 字段。响应内容：\n{response}")
        
        # 提取 "Action: " 之后到换行符之前的内容
        tool_name = response.split("Action: ")[1].split("\n")[0].strip()
        return tool_name

    def parse_tool_input(self, response: str) -> str:
        """
        从 LLM 响应中解析工具输入参数
        
        LLM 返回格式示例：
        ```
        Action Input: {"query": "Python"}
        ```
        
        Args:
            response: LLM 的响应文本
            
        Returns:
            工具输入参数字符串（JSON 格式）
            
        Raises:
            ValueError: 如果响应中不包含 "Action Input:" 字段
        """
        if "Action Input: " not in response:
            raise ValueError(f"响应中未找到 Action Input 字段。响应内容：\n{response}")
        
        # 提取 "Action Input: " 之后到换行符之前的内容
        tool_input = response.split("Action Input: ")[1].split("\n")[0].strip()
        return tool_input

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """
        执行工具
        
        这是 Agent 的关键步骤：根据工具名称找到对应的工具函数，
        解析输入参数（JSON 格式），然后调用工具函数。
        
        Args:
            tool_name: 工具名称
            tool_input: 工具输入参数（JSON 字符串格式）
            
        Returns:
            工具执行结果（字符串）
            
        Raises:
            ValueError: 如果工具不存在或参数解析失败
        """
        # 1. 检查工具是否存在
        if tool_name not in self.tools:
            return f"错误：工具 '{tool_name}' 不存在。可用工具：{list(self.tools.keys())}"
        
        # 2. 解析 JSON 格式的输入参数
        try:
            # 尝试解析 JSON
            if tool_input.strip():
                params = json.loads(tool_input)
            else:
                params = {}  # 空字符串表示无参数
        except json.JSONDecodeError as e:
            return f"错误：无法解析工具输入参数（JSON 格式错误）：{tool_input}。错误：{e}"
        
        # 3. 获取工具函数
        tool_func = self.tools[tool_name]
        
        # 4. 执行工具函数
        try:
            # 如果参数是字典，使用 ** 展开为关键字参数
            if isinstance(params, dict):
                result = tool_func(**params)
            else:
                # 如果参数不是字典，直接传递
                result = tool_func(params)
            
            # 将结果转换为字符串
            return str(result)
        except Exception as e:
            return f"错误：执行工具 '{tool_name}' 时发生异常：{str(e)}"

    def extract_final_answer(self, response: str) -> str:
        """
        从 LLM 响应中提取最终答案
        
        LLM 返回格式示例：
        ```
        Thought: 我现在知道最终答案了
        Final Answer: 这是最终答案的内容
        ```
        
        Args:
            response: LLM 的响应文本
            
        Returns:
            最终答案字符串
            
        Raises:
            ValueError: 如果响应中不包含 "Final Answer:" 字段
        """
        if "Final Answer:" not in response:
            raise ValueError(f"响应中未找到 Final Answer 字段。响应内容：\n{response}")
        
        # 提取 "Final Answer: " 之后的内容
        final_answer = response.split("Final Answer: ")[1].strip()
        return final_answer