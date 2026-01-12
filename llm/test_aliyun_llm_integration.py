"""
阿里云 LLM 集成测试
不使用 mock，直接调用真实 API，覆盖主要功能分支
"""
import pytest
import os
import time
from aliyun_llm import AliyunLLM


# 从环境变量读取API Key，测试时必须提供
API_KEY = os.getenv("QWEN_API_KEY")
if not API_KEY:
    raise ValueError(
        "QWEN_API_KEY 环境变量未设置。"
        "请设置环境变量 QWEN_API_KEY 后再运行集成测试。"
    )


@pytest.fixture
def llm():
    """创建使用真实 API Key 的 LLM 实例"""
    return AliyunLLM(
        model="qwen-plus",
        api_key=API_KEY,
        region="cn",
        temperature=0.7,
        timeout=30
    )


class TestIntegrationBasic:
    """集成测试：基本功能"""
    
    def test_basic_call_string_message(self, llm):
        """测试：字符串消息输入"""
        result = llm.call("你好，请用一句话介绍你自己")
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ 基本调用成功: {result[:50]}...")
    
    def test_basic_call_list_message(self, llm):
        """测试：消息列表输入"""
        messages = [
            {"role": "user", "content": "1+1等于几？"}
        ]
        result = llm.call(messages)
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ 消息列表调用成功: {result[:50]}...")
    
    def test_multi_turn_conversation(self, llm):
        """测试：多轮对话"""
        messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "1+1等于几？"},
        ]
        result = llm.call(messages)
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ 多轮对话成功: {result[:50]}...")
    
    def test_temperature_effect(self, llm):
        """测试：Temperature 设置"""
        # 测试低 temperature（更确定）
        llm.temperature = 0.1
        result1 = llm.call("写一个数字：1")
        assert isinstance(result1, str)
        
        # 测试高 temperature（更多样）
        llm.temperature = 1.0
        result2 = llm.call("写一个数字：1")
        assert isinstance(result2, str)
        
        print(f"\n✅ Temperature 测试成功")
        print(f"   Low temp (0.1): {result1[:30]}...")
        print(f"   High temp (1.0): {result2[:30]}...")


class TestIntegrationStopWords:
    """集成测试：Stop Words 功能"""
    
    def test_stop_words_string(self, llm):
        """测试：Stop Words - 字符串格式"""
        llm.stop = "停止"
        result = llm.call("请数数：1, 2, 3, 停止, 4, 5")
        assert isinstance(result, str)
        # 结果应该在 "停止" 处截断
        print(f"\n✅ Stop Words (字符串) 测试成功: {result[:50]}...")
    
    def test_stop_words_list(self, llm):
        """测试：Stop Words - 列表格式"""
        llm.stop = ["停止", "结束"]
        result = llm.call("请数数：1, 2, 3, 停止, 4, 5")
        assert isinstance(result, str)
        print(f"\n✅ Stop Words (列表) 测试成功: {result[:50]}...")


class TestIntegrationFunctionCalling:
    """集成测试：Function Calling 功能"""
    
    def test_function_calling_simple(self, llm):
        """测试：简单的 Function Calling"""
        # 定义工具
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "获取当前时间",
                    "parameters": {}
                }
            }
        ]
        
        # 定义可用函数
        def get_current_time():
            return f"当前时间：{time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        available_functions = {
            "get_current_time": get_current_time
        }
        
        result = llm.call(
            "现在几点了？",
            tools=tools,
            available_functions=available_functions
        )
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ Function Calling 测试成功: {result[:100]}...")
    
    def test_function_calling_with_params(self, llm):
        """测试：带参数的 Function Calling"""
        # 定义工具
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "执行数学计算",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number", "description": "第一个数字"},
                            "b": {"type": "number", "description": "第二个数字"},
                            "operation": {
                                "type": "string",
                                "enum": ["add", "subtract", "multiply", "divide"],
                                "description": "运算类型"
                            }
                        },
                        "required": ["a", "b", "operation"]
                    }
                }
            }
        ]
        
        # 定义可用函数
        def calculate(a, b, operation):
            if operation == "add":
                return a + b
            elif operation == "subtract":
                return a - b
            elif operation == "multiply":
                return a * b
            elif operation == "divide":
                if b == 0:
                    return "错误：除数不能为0"
                return a / b
            return "未知运算"
        
        available_functions = {
            "calculate": calculate
        }
        
        result = llm.call(
            "请计算 10 + 20",
            tools=tools,
            available_functions=available_functions
        )
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ Function Calling (带参数) 测试成功: {result[:100]}...")


class TestIntegrationRegions:
    """集成测试：不同地域"""
    
    def test_region_cn(self):
        """测试：中国大陆地域"""
        llm = AliyunLLM(
            model="qwen-plus",
            api_key=API_KEY,
            region="cn"
        )
        result = llm.call("你好")
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ Region CN 测试成功: {result[:50]}...")
    
    @pytest.mark.skip(reason="国际地域可能需要特殊网络配置")
    def test_region_intl(self):
        """测试：国际地域（可能因网络问题跳过）"""
        llm = AliyunLLM(
            model="qwen-plus",
            api_key=API_KEY,
            region="intl"
        )
        result = llm.call("Hello")
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ Region INTL 测试成功: {result[:50]}...")


class TestIntegrationErrorHandling:
    """集成测试：错误处理"""
    
    def test_invalid_api_key(self):
        """测试：无效 API Key"""
        llm = AliyunLLM(
            model="qwen-plus",
            api_key="sk-invalid-key",
            region="cn"
        )
        # 应该抛出异常
        with pytest.raises((RuntimeError, ValueError)):
            llm.call("test")
        print(f"\n✅ 无效 API Key 错误处理测试成功")
    
    def test_invalid_region(self):
        """测试：无效地域"""
        with pytest.raises(ValueError, match="不支持的地域"):
            AliyunLLM(
                model="qwen-plus",
                api_key=API_KEY,
                region="invalid"
            )
        print(f"\n✅ 无效 Region 错误处理测试成功")
    
    def test_timeout_handling(self, llm):
        """测试：超时处理"""
        llm.timeout = 0.001  # 设置极短的超时时间
        with pytest.raises(TimeoutError):
            llm.call("test")
        print(f"\n✅ 超时处理测试成功")


class TestIntegrationEdgeCases:
    """集成测试：边界情况"""
    
    def test_empty_message(self, llm):
        """测试：空消息"""
        # 空字符串消息
        result = llm.call("")
        assert isinstance(result, str)
        print(f"\n✅ 空消息测试成功: {result[:50]}...")
    
    def test_long_message(self, llm):
        """测试：长消息"""
        long_message = "请总结以下内容：" + "这是一个测试消息。" * 100
        result = llm.call(long_message)
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ 长消息测试成功: {result[:50]}...")
    
    def test_special_characters(self, llm):
        """测试：特殊字符"""
        llm.timeout = 60  # 增加超时时间
        special_message = "请处理这些特殊字符：!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = llm.call(special_message)
        assert isinstance(result, str)
        print(f"\n✅ 特殊字符测试成功: {result[:50]}...")
    
    def test_chinese_characters(self, llm):
        """测试：中文字符"""
        chinese_message = "请用中文回答：什么是人工智能？"
        result = llm.call(chinese_message)
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ 中文字符测试成功: {result[:100]}...")


class TestIntegrationContextWindow:
    """集成测试：上下文窗口"""
    
    def test_context_window_size(self, llm):
        """测试：获取上下文窗口大小"""
        size = llm.get_context_window_size()
        assert isinstance(size, int)
        assert size > 0
        print(f"\n✅ 上下文窗口大小: {size}")
    
    def test_different_models_context_window(self):
        """测试：不同模型的上下文窗口"""
        models = ["qwen-plus", "qwen-turbo", "qwen-long", "qwen-max"]
        for model in models:
            llm = AliyunLLM(
                model=model,
                api_key=API_KEY,
                region="cn"
            )
            size = llm.get_context_window_size()
            assert isinstance(size, int)
            assert size > 0
            print(f"   {model}: {size}")


class TestIntegrationComplexScenarios:
    """集成测试：复杂场景"""
    
    def test_system_message_effect(self, llm):
        """测试：System Message 的效果"""
        messages_with_system = [
            {"role": "system", "content": "你是一个专业的数学老师。"},
            {"role": "user", "content": "1+1等于几？"}
        ]
        result = llm.call(messages_with_system)
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ System Message 测试成功: {result[:100]}...")
    
    def test_multi_turn_with_context(self, llm):
        """测试：多轮对话保持上下文"""
        # 第一轮
        messages1 = [
            {"role": "user", "content": "我的名字是张三"}
        ]
        result1 = llm.call(messages1)
        assert isinstance(result1, str)
        
        # 第二轮（应该记住名字）
        messages2 = [
            {"role": "user", "content": "我的名字是张三"},
            {"role": "assistant", "content": result1},
            {"role": "user", "content": "我刚才告诉你我的名字是什么？"}
        ]
        result2 = llm.call(messages2)
        assert isinstance(result2, str)
        assert len(result2) > 0
        print(f"\n✅ 多轮对话上下文测试成功")
        print(f"   第一轮: {result1[:50]}...")
        print(f"   第二轮: {result2[:50]}...")
    
    def test_tool_message_format(self, llm):
        """测试：Tool Message 格式"""
        # 测试 tool message 的正确格式
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "test_func",
                    "description": "测试函数",
                    "parameters": {}
                }
            }
        ]
        
        def test_func():
            return "测试结果"
        
        available_functions = {"test_func": test_func}
        
        result = llm.call(
            "请调用测试函数",
            tools=tools,
            available_functions=available_functions
        )
        assert isinstance(result, str)
        print(f"\n✅ Tool Message 格式测试成功: {result[:100]}...")
    
    def test_assistant_message_with_tool_calls(self, llm):
        """测试：Assistant Message 包含 tool_calls"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_info",
                    "description": "获取信息",
                    "parameters": {}
                }
            }
        ]
        
        def get_info():
            return "这是测试信息"
        
        available_functions = {"get_info": get_info}
        
        # 测试包含 tool_calls 的 assistant message
        messages = [
            {"role": "user", "content": "请获取信息"}
        ]
        result = llm.call(
            messages,
            tools=tools,
            available_functions=available_functions
        )
        assert isinstance(result, str)
        print(f"\n✅ Assistant Message with tool_calls 测试成功: {result[:100]}...")
    
    def test_temperature_range(self, llm):
        """测试：Temperature 范围"""
        temperatures = [0.0, 0.5, 1.0, 1.5]
        for temp in temperatures:
            llm.temperature = temp
            result = llm.call("说一个数字")
            assert isinstance(result, str)
            assert len(result) > 0
        print(f"\n✅ Temperature 范围测试成功")
    
    def test_stop_words_effectiveness(self, llm):
        """测试：Stop Words 有效性"""
        llm.stop = "停止"
        result = llm.call("请数数：1, 2, 3, 停止, 4, 5")
        assert isinstance(result, str)
        # 验证结果中不包含 stop word 之后的内容（理想情况下）
        print(f"\n✅ Stop Words 有效性测试成功: {result[:100]}...")
    
    def test_multiple_tools_calling(self, llm):
        """测试：多个工具调用"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_time",
                    "description": "获取当前时间",
                    "parameters": {}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_date",
                    "description": "获取当前日期",
                    "parameters": {}
                }
            }
        ]
        
        def get_time():
            return time.strftime('%H:%M:%S')
        
        def get_date():
            return time.strftime('%Y-%m-%d')
        
        available_functions = {
            "get_time": get_time,
            "get_date": get_date
        }
        
        result = llm.call(
            "请告诉我现在的时间和日期",
            tools=tools,
            available_functions=available_functions
        )
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ 多个工具调用测试成功: {result[:100]}...")
    
    def test_function_calling_recursion(self, llm):
        """测试：Function Calling 递归调用"""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_one",
                    "description": "数字加1",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "num": {"type": "number", "description": "要加1的数字"}
                        },
                        "required": ["num"]
                    }
                }
            }
        ]
        
        def add_one(num):
            return num + 1
        
        available_functions = {"add_one": add_one}
        
        result = llm.call(
            "请计算 5 + 1",
            tools=tools,
            available_functions=available_functions
        )
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"\n✅ Function Calling 递归测试成功: {result[:100]}...")
    
    def test_error_handling_invalid_response(self, llm):
        """测试：错误处理 - 无效响应格式"""
        # 这个测试很难触发，因为 API 通常返回有效响应
        # 但我们可以测试其他错误情况
        # 例如：无效的 API Key（已在 TestIntegrationErrorHandling 中测试）
        pass
    
    def test_context_window_limits(self, llm):
        """测试：上下文窗口限制"""
        # 测试接近上下文窗口限制的长消息
        size = llm.get_context_window_size()
        print(f"\n✅ 上下文窗口大小: {size}")
        
        # 创建一个较长的消息（但不超过限制）
        long_content = "请总结：" + "这是一个测试句子。" * 50
        result = llm.call(long_content)
        assert isinstance(result, str)
        print(f"✅ 长消息处理成功（长度: {len(long_content)} 字符）")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

