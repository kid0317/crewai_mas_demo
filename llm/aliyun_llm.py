"""
阿里云通义千问 LLM 实现
基于 CrewAI BaseLLM 抽象类实现
"""
from crewai import BaseLLM
from typing import Any, Dict, List, Optional, Union
import requests
import json
import os
import logging


class AliyunLLM(BaseLLM):
    """阿里云通义千问 LLM 实现类"""
    
    # 支持的端点配置
    ENDPOINTS = {
        "cn": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "intl": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions",
        "finance": "https://dashscope-finance.aliyuncs.com/compatible-mode/v1/chat/completions"
    }
    
    # 类级别的 logger（所有实例共享）
    _logger = None
    
    @classmethod
    def _get_logger(cls):
        """获取或创建 logger 实例"""
        if cls._logger is None:
            cls._logger = logging.getLogger(cls.__name__)
            # 如果 logger 还没有 handler，添加一个
            # 检查是否已经有 handler（避免重复添加）
            if not cls._logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                handler.setFormatter(formatter)
                cls._logger.addHandler(handler)
                cls._logger.setLevel(logging.INFO)
            # 防止日志传播到根 logger（避免重复输出）
            cls._logger.propagate = False
        return cls._logger
    
    @property
    def logger(self):
        """获取 logger 实例"""
        return self._get_logger()
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        region: str = "cn",
        temperature: Optional[float] = None,
        timeout: int = 600,
    ):
        """
        初始化阿里云 LLM
        
        Args:
            model: 模型名称，如 "qwen-plus", "qwen-turbo" 等
            api_key: API Key，如果不提供则从环境变量 QWEN_API_KEY 或 DASHSCOPE_API_KEY 读取
            region: 地域选择，"cn"（中国大陆）、"intl"（国际）或 "finance"（金融云）
            temperature: 采样温度，控制生成文本的多样性
            timeout: 请求超时时间（秒），默认600秒（10分钟），适用于复杂任务和长文本生成
        """
        # IMPORTANT: 必须调用父类构造函数
        super().__init__(model=model, temperature=temperature)
        
        # 初始化 logger
        self._get_logger()
        
        # 获取 API Key（支持多个环境变量名）
        self.api_key = api_key or os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 未提供。请通过 api_key 参数传入或设置环境变量 QWEN_API_KEY 或 DASHSCOPE_API_KEY"
            )
        
        # 设置端点
        if region not in self.ENDPOINTS:
            raise ValueError(f"不支持的地域: {region}。支持的地域: {list(self.ENDPOINTS.keys())}")
        self.endpoint = self.ENDPOINTS[region]
        self.region = region
        
        # 设置超时时间
        self.timeout = timeout
    
    def call(
        self,
        messages: Union[str, List[Dict[str, str]]],
        tools: Optional[List[dict]] = None,
        callbacks: Optional[List[Any]] = None,
        available_functions: Optional[Dict[str, Any]] = None,
        max_iterations: int = 10,
        **kwargs: Any,  # 接受额外的参数（如 from_task 等），以兼容 CrewAI 不同版本
    ) -> Union[str, Any]:
        """
        调用阿里云 LLM API
        
        Args:
            messages: 消息列表或单个字符串
            tools: 工具定义列表（用于 Function Calling）
            callbacks: 回调函数列表
            available_functions: 可用的函数映射
            max_iterations: 最大迭代次数（用于防止 Function Calling 无限递归）
            **kwargs: 额外的参数（如 from_task 等），用于兼容 CrewAI 不同版本
            
        Returns:
            LLM 返回的文本内容
        """
        # 检查迭代次数限制
        if max_iterations <= 0:
            raise RuntimeError("Function calling 达到最大迭代次数，可能存在无限循环")
        
        # 转换字符串为消息格式
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        
        # 验证消息格式
        self._validate_messages(messages)
        
        # 准备请求体
        payload = {
            "model": self.model,
            "messages": messages,
        }
        
        # 添加 temperature（如果设置了）
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        
        # 添加 stop words（如果支持）
        if self.stop and self.supports_stop_words():
            stop_value = self._prepare_stop_words(self.stop)
            if stop_value:
                payload["stop"] = stop_value
        
        # 添加 tools（如果支持 Function Calling）
        if tools and self.supports_function_calling():
            payload["tools"] = tools
        
        # 调用回调函数（如果提供）
        if callbacks:
            for callback in callbacks:
                if hasattr(callback, 'on_llm_start'):
                    try:
                        callback.on_llm_start(messages)
                    except Exception:
                        pass  # 忽略回调错误，不影响主流程
        
        # 打印请求 payload（阅读友好格式）
        self.logger.info("=" * 80)
        self.logger.info("发送 LLM API 请求")
        self.logger.info("-" * 80)
        self.logger.info(f"Endpoint: {self.endpoint}")
        self.logger.info(f"Model: {self.model}")
        self.logger.info("Request Payload:")
        try:
            # 格式化 JSON，使用缩进和中文编码
            payload_str = json.dumps(payload, ensure_ascii=False, indent=2)
            # 逐行打印，每行前面加上缩进
            for line in payload_str.split('\n'):
                self.logger.info(f"  {line}")
        except Exception as e:
            self.logger.warning(f"无法格式化 payload: {e}")
            self.logger.info(f"  {payload}")
        self.logger.info("-" * 80)
        
        # 发送 API 请求
        try:
            response = requests.post(
                self.endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 打印响应 result（阅读友好格式）
            self.logger.info("收到 LLM API 响应")
            self.logger.info("-" * 80)
            self.logger.info("Response Result:")
            try:
                # 格式化 JSON，使用缩进和中文编码
                result_str = json.dumps(result, ensure_ascii=False, indent=2)
                # 逐行打印，每行前面加上缩进
                for line in result_str.split('\n'):
                    self.logger.info(f"  {line}")
            except Exception as e:
                self.logger.warning(f"无法格式化 result: {e}")
                self.logger.info(f"  {result}")
            self.logger.info("-" * 80)
            self.logger.info("=" * 80)
            
            # 调用回调函数（如果提供）
            if callbacks:
                for callback in callbacks:
                    if hasattr(callback, 'on_llm_end'):
                        try:
                            callback.on_llm_end(result)
                        except Exception:
                            pass  # 忽略回调错误，不影响主流程
            
            # 检查是否有工具调用
            if "choices" in result and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                
                # 处理工具调用
                if "tool_calls" in message and available_functions:
                    return self._handle_function_calls(
                        message["tool_calls"],
                        messages,
                        tools,
                        available_functions,
                        max_iterations - 1
                    )
                
                # 返回文本内容
                content = message.get("content")
                # 当有 tool_calls 时，content 可能为 None，这是正常的
                if content is None:
                    if "tool_calls" in message:
                        raise ValueError("响应包含 tool_calls 但未正确处理")
                    raise ValueError("响应中未找到 content 字段")
                return content
            else:
                raise ValueError("响应中未找到 choices 字段")
                
        except requests.Timeout:
            raise TimeoutError(f"LLM 请求超时（{self.timeout}秒）")
        except requests.RequestException as e:
            raise RuntimeError(f"LLM 请求失败: {str(e)}")
        except (KeyError, IndexError) as e:
            raise ValueError(f"响应格式错误: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"响应 JSON 解析失败: {str(e)}")
    
    def _handle_function_calls(
        self,
        tool_calls: List[dict],
        messages: List[Dict[str, str]],
        tools: Optional[List[dict]],
        available_functions: Dict[str, Any],
        max_iterations: int = 10
    ) -> str:
        """
        处理 Function Calling
        
        Args:
            tool_calls: 工具调用列表
            messages: 消息历史
            tools: 工具定义
            available_functions: 可用的函数映射
            max_iterations: 最大迭代次数（用于防止无限递归）
            
        Returns:
            函数调用后的最终响应
        """
        # 检查迭代次数限制
        if max_iterations <= 0:
            raise RuntimeError("Function calling 达到最大迭代次数，可能存在无限循环")
        
        # 添加助手消息（包含工具调用）
        assistant_message = {
            "role": "assistant",
            "content": None,  # 当有 tool_calls 时，content 可以为 None
            "tool_calls": tool_calls
        }
        messages.append(assistant_message)
        
        # 执行每个工具调用
        for tool_call in tool_calls:
            function_info = tool_call.get("function", {})
            function_name = function_info.get("name")
            tool_call_id = tool_call.get("id")
            
            if not tool_call_id:
                raise ValueError(f"tool_call 缺少 id 字段: {tool_call}")
            
            if function_name in available_functions:
                # 解析函数参数
                try:
                    arguments_str = function_info.get("arguments", "{}")
                    if isinstance(arguments_str, str):
                        # 空字符串解析为空字典
                        if arguments_str.strip() == "":
                            function_args = {}
                        else:
                            function_args = json.loads(arguments_str)
                    else:
                        function_args = arguments_str
                except json.JSONDecodeError as e:
                    raise ValueError(f"无法解析函数参数: {arguments_str}, 错误: {e}")
                
                # 执行函数
                try:
                    function_result = available_functions[function_name](**function_args)
                except Exception as e:
                    function_result = f"函数执行错误: {str(e)}"
                
                # 添加工具响应消息（符合阿里云 API 规范：不包含 name 字段）
                tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": str(function_result)
                }
                messages.append(tool_message)
            else:
                # 函数不存在，添加错误消息
                tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": f"函数 {function_name} 不可用"
                }
                messages.append(tool_message)
        
        # 再次调用 LLM，传入完整的消息历史和递减的迭代次数
        # 注意：递归调用时不传递 kwargs，避免参数冲突
        return self.call(messages, tools, None, available_functions, max_iterations - 1)
    
    def supports_function_calling(self) -> bool:
        """
        是否支持 Function Calling
        
        Returns:
            True，阿里云通义千问支持 Function Calling
        """
        return True
    
    def supports_stop_words(self) -> bool:
        """
        是否支持停止词
        
        Returns:
            True，阿里云通义千问支持 stop 参数
        """
        return True
    
    def _validate_messages(self, messages: List[Dict[str, str]]) -> None:
        """
        验证消息格式
        
        Args:
            messages: 消息列表
            
        Raises:
            ValueError: 如果消息格式无效
        """
        valid_roles = {"system", "user", "assistant", "tool"}
        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"消息 {i} 必须是字典格式: {msg}")
            if "role" not in msg:
                raise ValueError(f"消息 {i} 缺少 role 字段: {msg}")
            if msg["role"] not in valid_roles:
                raise ValueError(f"消息 {i} 包含无效的 role: {msg['role']}，有效值: {valid_roles}")
            # tool 消息需要 tool_call_id，其他消息需要 content
            if msg["role"] == "tool":
                if "tool_call_id" not in msg:
                    raise ValueError(f"tool 消息 {i} 缺少 tool_call_id 字段: {msg}")
                if "content" not in msg:
                    raise ValueError(f"tool 消息 {i} 缺少 content 字段: {msg}")
            elif "content" not in msg and msg.get("tool_calls") is None:
                # assistant 消息在有 tool_calls 时 content 可以为 None
                raise ValueError(f"消息 {i} 缺少 content 字段且没有 tool_calls: {msg}")
    
    def _prepare_stop_words(self, stop: Union[str, List[Union[str, int]]]) -> Optional[Union[str, List[Union[str, int]]]]:
        """
        准备 stop words，验证格式
        
        Args:
            stop: 停止词（字符串或列表）
            
        Returns:
            格式化后的停止词，如果格式无效则返回 None
            
        Raises:
            ValueError: 如果 stop 格式无效
        """
        if not stop:
            return None
        
        if isinstance(stop, str):
            return stop
        
        if isinstance(stop, list):
            if not stop:
                return None
            # 验证列表中的元素类型一致
            stop_types = {type(item) for item in stop}
            if len(stop_types) > 1:
                raise ValueError(
                    "stop 数组中的元素类型必须一致，不能混合字符串和 token_id。"
                    f"当前类型: {stop_types}"
                )
            return stop
        
        return None
    
    def get_context_window_size(self) -> int:
        """
        获取上下文窗口大小
        
        Returns:
            上下文窗口大小（Token 数）
            注意：不同模型有不同的上下文窗口，这里返回一个通用值
        """
        # 根据模型名称返回不同的上下文窗口大小
        if "long" in self.model.lower():
            return 200000  # qwen-long 支持超长上下文
        elif "max" in self.model.lower():
            return 8192
        elif "plus" in self.model.lower():
            return 8192
        elif "turbo" in self.model.lower() or "flash" in self.model.lower():
            return 8192
        else:
            return 8192  # 默认值


# 使用示例
if __name__ == "__main__":
    # 创建阿里云 LLM 实例
    llm = AliyunLLM(
        model="qwen-plus",
        # api_key 参数可选，会从环境变量 QWEN_API_KEY 或 DASHSCOPE_API_KEY 读取
        # 或直接传入 "sk-xxx"
        region="cn",  # 或 "intl", "finance"
        temperature=0.7
    )
    
    # 测试基本调用
    response = llm.call("你好，请介绍一下你自己")
    print("响应:", response)
    
    # 测试多轮对话
    messages = [
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": "1+1等于几？"}
    ]
    response = llm.call(messages)
    print("多轮对话响应:", response)

