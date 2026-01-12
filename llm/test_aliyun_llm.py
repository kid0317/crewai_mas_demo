"""
阿里云 LLM 单元测试
使用 pytest 框架，目标 100% 代码覆盖率
"""
import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

import sys
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from aliyun_llm import AliyunLLM


# ==================== 测试辅助函数 ====================

def create_mock_response(status_code=200, json_data=None):
    """创建模拟的 HTTP 响应"""
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data or {
        "choices": [{
            "message": {
                "content": "测试响应"
            }
        }]
    }
    mock_response.raise_for_status = Mock()
    return mock_response


def create_tool_calls_response(tool_calls):
    """创建包含 tool_calls 的响应"""
    return {
        "choices": [{
            "message": {
                "content": None,
                "tool_calls": tool_calls
            }
        }]
    }


# ==================== 第一批：__init__ 方法测试 ====================

class TestInit:
    """测试 __init__ 方法"""
    
    @patch('aliyun_llm.os.getenv')
    def test_init_all_parameters(self, mock_getenv):
        """TC-001: 正常初始化 - 所有参数提供"""
        mock_getenv.return_value = None
        llm = AliyunLLM(
            model="qwen-plus",
            api_key="sk-test123",
            region="cn",
            temperature=0.7,
            timeout=60
        )
        assert llm.model == "qwen-plus"
        assert llm.api_key == "sk-test123"
        assert llm.region == "cn"
        assert llm.temperature == 0.7
        assert llm.timeout == 60
        assert "dashscope.aliyuncs.com" in llm.endpoint
    
    @patch('aliyun_llm.os.getenv')
    def test_init_minimal_parameters(self, mock_getenv):
        """TC-002: 正常初始化 - 最小参数"""
        mock_getenv.return_value = None
        llm = AliyunLLM(
            model="qwen-turbo",
            api_key="sk-test123"
        )
        assert llm.model == "qwen-turbo"
        assert llm.region == "cn"
        assert llm.temperature is None
        assert llm.timeout == 30
    
    @patch('aliyun_llm.os.getenv')
    def test_init_api_key_from_param(self, mock_getenv):
        """TC-003: API Key - 通过参数传入"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-param123")
        assert llm.api_key == "sk-param123"
        mock_getenv.assert_not_called()
    
    @patch('aliyun_llm.os.getenv')
    def test_init_api_key_from_qwen_env(self, mock_getenv):
        """TC-004: API Key - 从环境变量 QWEN_API_KEY 读取"""
        def getenv_side_effect(key):
            if key == "QWEN_API_KEY":
                return "sk-env-qwen"
            return None
        
        mock_getenv.side_effect = getenv_side_effect
        llm = AliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-env-qwen"
    
    @patch('aliyun_llm.os.getenv')
    def test_init_api_key_from_dashscope_env(self, mock_getenv):
        """TC-005: API Key - 从环境变量 DASHSCOPE_API_KEY 读取"""
        def getenv_side_effect(key):
            if key == "DASHSCOPE_API_KEY":
                return "sk-env-dashscope"
            return None
        
        mock_getenv.side_effect = getenv_side_effect
        llm = AliyunLLM(model="qwen-plus", api_key=None)
        assert llm.api_key == "sk-env-dashscope"
    
    @patch('aliyun_llm.os.getenv')
    def test_init_api_key_param_priority(self, mock_getenv):
        """TC-006: API Key - 优先使用参数，忽略环境变量"""
        def getenv_side_effect(key):
            if key == "QWEN_API_KEY":
                return "sk-env-qwen"
            elif key == "DASHSCOPE_API_KEY":
                return "sk-env-dashscope"
            return None
        
        mock_getenv.side_effect = getenv_side_effect
        llm = AliyunLLM(model="qwen-plus", api_key="sk-param-priority")
        assert llm.api_key == "sk-param-priority"
    
    @patch('aliyun_llm.os.getenv')
    def test_init_api_key_missing(self, mock_getenv):
        """TC-007: API Key - 缺失错误"""
        mock_getenv.return_value = None
        with pytest.raises(ValueError, match="API Key 未提供"):
            AliyunLLM(model="qwen-plus", api_key=None)
    
    @patch('aliyun_llm.os.getenv')
    def test_init_region_cn(self, mock_getenv):
        """TC-008: Region - 有效值 cn"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test", region="cn")
        assert "dashscope.aliyuncs.com" in llm.endpoint
    
    @patch('aliyun_llm.os.getenv')
    def test_init_region_intl(self, mock_getenv):
        """TC-009: Region - 有效值 intl"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test", region="intl")
        assert "dashscope-intl.aliyuncs.com" in llm.endpoint
    
    @patch('aliyun_llm.os.getenv')
    def test_init_region_finance(self, mock_getenv):
        """TC-010: Region - 有效值 finance"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test", region="finance")
        assert "dashscope-finance.aliyuncs.com" in llm.endpoint
    
    @patch('aliyun_llm.os.getenv')
    def test_init_region_invalid(self, mock_getenv):
        """TC-011: Region - 无效值"""
        mock_getenv.return_value = None
        with pytest.raises(ValueError, match="不支持的地域"):
            AliyunLLM(model="qwen-plus", api_key="sk-test", region="invalid")
    
    @patch('aliyun_llm.os.getenv')
    def test_init_temperature_none(self, mock_getenv):
        """TC-012: Temperature - None"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test", temperature=None)
        assert llm.temperature is None
    
    @patch('aliyun_llm.os.getenv')
    def test_init_temperature_value(self, mock_getenv):
        """TC-013: Temperature - 有效值"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test", temperature=0.8)
        assert llm.temperature == 0.8
    
    @patch('aliyun_llm.os.getenv')
    def test_init_timeout_default(self, mock_getenv):
        """TC-014: Timeout - 默认值"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test")
        assert llm.timeout == 30
    
    @patch('aliyun_llm.os.getenv')
    def test_init_timeout_custom(self, mock_getenv):
        """TC-015: Timeout - 自定义值"""
        mock_getenv.return_value = None
        llm = AliyunLLM(model="qwen-plus", api_key="sk-test", timeout=60)
        assert llm.timeout == 60


# ==================== 第二批：call 方法基础测试 ====================

class TestCallBasic:
    """测试 call 方法的基础功能"""
    
    @pytest.fixture
    def llm(self):
        """创建测试用的 LLM 实例"""
        with patch('aliyun_llm.os.getenv', return_value=None):
            return AliyunLLM(model="qwen-plus", api_key="sk-test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_string_message(self, mock_post, llm):
        """TC-016: 字符串消息输入"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        result = llm.call("你好")
        
        assert result == "测试响应"
        # 验证请求体包含转换后的消息
        call_args = mock_post.call_args
        assert call_args[1]['json']['messages'] == [{"role": "user", "content": "你好"}]
    
    @patch('aliyun_llm.requests.post')
    def test_call_list_message(self, mock_post, llm):
        """TC-017: 消息列表输入"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        messages = [{"role": "user", "content": "你好"}]
        result = llm.call(messages)
        
        assert result == "测试响应"
        call_args = mock_post.call_args
        assert call_args[1]['json']['messages'] == messages
    
    def test_call_invalid_message_not_dict(self, llm):
        """TC-018: 消息格式验证 - 非字典类型"""
        with pytest.raises(ValueError, match="必须是字典格式"):
            llm.call(["invalid", "message"])
    
    def test_call_invalid_message_missing_role(self, llm):
        """TC-019: 消息格式验证 - 缺少 role 字段"""
        with pytest.raises(ValueError, match="缺少 role 字段"):
            llm.call([{"content": "test"}])
    
    def test_call_invalid_message_invalid_role(self, llm):
        """TC-020: 消息格式验证 - 无效 role"""
        with pytest.raises(ValueError, match="无效的 role"):
            llm.call([{"role": "invalid", "content": "test"}])
    
    def test_call_invalid_message_user_missing_content(self, llm):
        """TC-021: 消息格式验证 - user 消息缺少 content"""
        with pytest.raises(ValueError, match="缺少 content 字段"):
            llm.call([{"role": "user"}])
    
    def test_call_invalid_message_tool_missing_tool_call_id(self, llm):
        """TC-022: 消息格式验证 - tool 消息缺少 tool_call_id"""
        with pytest.raises(ValueError, match="缺少 tool_call_id 字段"):
            llm.call([{"role": "tool", "content": "result"}])
    
    def test_call_invalid_message_tool_missing_content(self, llm):
        """TC-023: 消息格式验证 - tool 消息缺少 content"""
        with pytest.raises(ValueError, match="缺少 content 字段"):
            llm.call([{"role": "tool", "tool_call_id": "call_123"}])
    
    def test_call_valid_message_assistant_with_tool_calls(self, llm):
        """TC-024: 消息格式验证 - assistant 消息有 tool_calls 时 content 可为 None"""
        # 这个测试验证消息格式验证通过，不抛出错误
        messages = [{"role": "assistant", "content": None, "tool_calls": []}]
        # 由于没有实际调用 API，这里只验证不会在验证阶段抛出错误
        # 实际调用会在 API 请求时失败，但格式验证应该通过
        try:
            llm._validate_messages(messages)
        except ValueError:
            pytest.fail("有效的 assistant 消息不应该抛出错误")
    
    @patch('aliyun_llm.requests.post')
    def test_call_temperature_none_not_in_payload(self, mock_post, llm):
        """TC-025: Temperature - None 时不添加到 payload"""
        llm.temperature = None
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test")
        
        call_args = mock_post.call_args
        assert "temperature" not in call_args[1]['json']
    
    @patch('aliyun_llm.requests.post')
    def test_call_temperature_value_in_payload(self, mock_post, llm):
        """TC-026: Temperature - 有值时添加到 payload"""
        llm.temperature = 0.7
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test")
        
        call_args = mock_post.call_args
        assert call_args[1]['json']['temperature'] == 0.7
    
    @patch('aliyun_llm.requests.post')
    def test_call_stop_words_none_not_in_payload(self, mock_post, llm):
        """TC-027: Stop Words - None 时不添加"""
        llm.stop = None
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test")
        
        call_args = mock_post.call_args
        assert "stop" not in call_args[1]['json']
    
    @patch('aliyun_llm.requests.post')
    def test_call_stop_words_string_in_payload(self, mock_post, llm):
        """TC-028: Stop Words - 字符串格式"""
        llm.stop = "停止"
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test")
        
        call_args = mock_post.call_args
        # _prepare_stop_words 返回字符串，但根据代码逻辑，字符串会直接添加到 payload
        # 根据阿里云 API，stop 可以是字符串或列表
        assert call_args[1]['json']['stop'] == "停止"
    
    @patch('aliyun_llm.requests.post')
    def test_call_stop_words_list_string_in_payload(self, mock_post, llm):
        """TC-029: Stop Words - 列表格式（字符串）"""
        llm.stop = ["停止1", "停止2"]
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test")
        
        call_args = mock_post.call_args
        assert call_args[1]['json']['stop'] == ["停止1", "停止2"]
    
    @patch('aliyun_llm.requests.post')
    def test_call_stop_words_list_int_in_payload(self, mock_post, llm):
        """TC-030: Stop Words - 列表格式（整数 token_id）"""
        llm.stop = [123, 456]
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test")
        
        call_args = mock_post.call_args
        assert call_args[1]['json']['stop'] == [123, 456]
    
    def test_call_stop_words_mixed_types_error(self, llm):
        """TC-031: Stop Words - 混合类型错误"""
        llm.stop = ["停止", 123]
        with pytest.raises(ValueError, match="元素类型必须一致"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_tools_none_not_in_payload(self, mock_post, llm):
        """TC-032: Tools - None 时不添加"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test", tools=None)
        
        call_args = mock_post.call_args
        assert "tools" not in call_args[1]['json']
    
    @patch('aliyun_llm.requests.post')
    def test_call_tools_value_in_payload(self, mock_post, llm):
        """TC-033: Tools - 有值时添加"""
        tools = [{"type": "function", "function": {"name": "test", "description": "test"}}]
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        llm.call("test", tools=tools)
        
        call_args = mock_post.call_args
        assert call_args[1]['json']['tools'] == tools


# ==================== 第三批：call 方法高级功能测试 ====================

class TestCallAdvanced:
    """测试 call 方法的高级功能"""
    
    @pytest.fixture
    def llm(self):
        """创建测试用的 LLM 实例"""
        with patch('aliyun_llm.os.getenv', return_value=None):
            return AliyunLLM(model="qwen-plus", api_key="sk-test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_callbacks_none(self, mock_post, llm):
        """TC-034: Callbacks - None 时不调用"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        callback = Mock()
        llm.call("test", callbacks=None)
        
        callback.on_llm_start.assert_not_called()
        callback.on_llm_end.assert_not_called()
    
    @patch('aliyun_llm.requests.post')
    def test_call_callbacks_on_llm_start(self, mock_post, llm):
        """TC-035: Callbacks - 有 on_llm_start 时调用"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        callback = Mock()
        callback.on_llm_start = Mock()
        callback.on_llm_end = None
        
        llm.call("test", callbacks=[callback])
        
        callback.on_llm_start.assert_called_once()
    
    @patch('aliyun_llm.requests.post')
    def test_call_callbacks_on_llm_end(self, mock_post, llm):
        """TC-036: Callbacks - 有 on_llm_end 时调用"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        callback = Mock()
        callback.on_llm_start = None
        callback.on_llm_end = Mock()
        
        llm.call("test", callbacks=[callback])
        
        callback.on_llm_end.assert_called_once()
    
    @patch('aliyun_llm.requests.post')
    def test_call_callbacks_exception_ignored(self, mock_post, llm):
        """TC-037: Callbacks - 回调异常不影响主流程"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        callback = Mock()
        callback.on_llm_start = Mock(side_effect=Exception("Callback error"))
        callback.on_llm_end = Mock()
        
        # 不应该抛出异常
        result = llm.call("test", callbacks=[callback])
        assert result == "测试响应"
    
    @patch('aliyun_llm.requests.post')
    def test_call_max_iterations_zero(self, mock_post, llm):
        """TC-040: Max Iterations - 为 0 时抛出错误"""
        with pytest.raises(RuntimeError, match="达到最大迭代次数"):
            llm.call("test", max_iterations=0)
    
    @patch('aliyun_llm.requests.post')
    def test_call_max_iterations_negative(self, mock_post, llm):
        """TC-041: Max Iterations - 负数时抛出错误"""
        with pytest.raises(RuntimeError, match="达到最大迭代次数"):
            llm.call("test", max_iterations=-1)
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_success_normal_response(self, mock_post, llm):
        """TC-042: API 请求成功 - 正常响应"""
        mock_response = create_mock_response(json_data={
            "choices": [{
                "message": {
                    "content": "响应内容"
                }
            }]
        })
        mock_post.return_value = mock_response
        
        result = llm.call("test")
        assert result == "响应内容"
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_timeout(self, mock_post, llm):
        """TC-047: API 请求失败 - Timeout"""
        import requests
        mock_post.side_effect = requests.Timeout("Request timeout")
        
        with pytest.raises(TimeoutError, match="请求超时"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_request_exception(self, mock_post, llm):
        """TC-048: API 请求失败 - RequestException"""
        import requests
        mock_post.side_effect = requests.RequestException("Network error")
        
        with pytest.raises(RuntimeError, match="请求失败"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_response_missing_choices(self, mock_post, llm):
        """TC-050: 响应解析 - 缺少 choices 字段"""
        mock_response = create_mock_response(json_data={"error": "invalid"})
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="未找到 choices 字段"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_response_empty_choices(self, mock_post, llm):
        """TC-051: 响应解析 - choices 为空列表"""
        mock_response = create_mock_response(json_data={"choices": []})
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="未找到 choices 字段"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_response_missing_message(self, mock_post, llm):
        """TC-052: 响应解析 - 缺少 message 字段"""
        mock_response = create_mock_response(json_data={"choices": [{}]})
        mock_post.return_value = mock_response
        
        # 当 choices[0] 中没有 message 字段时，get("message", {}) 返回空字典
        # 然后检查 content 时发现为 None，会抛出 "响应中未找到 content 字段"
        with pytest.raises(ValueError, match="未找到 content 字段"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_response_json_decode_error(self, mock_post, llm):
        """TC-053: 响应解析 - JSON 解析错误"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="JSON 解析失败"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_available_functions_none_with_tool_calls(self, mock_post, llm):
        """TC-038: Available Functions - None 时不处理 tool_calls"""
        tool_calls = [{
            "id": "call_123",
            "function": {"name": "test", "arguments": "{}"}
        }]
        # 即使响应包含 tool_calls，但 available_functions 为 None，应该返回 content
        mock_response = create_mock_response(json_data={
            "choices": [{
                "message": {
                    "content": "正常响应",
                    "tool_calls": tool_calls
                }
            }]
        })
        mock_post.return_value = mock_response
        
        result = llm.call("test", available_functions=None)
        # 应该返回 content，不处理 tool_calls
        assert result == "正常响应"
    
    @patch('aliyun_llm.requests.post')
    def test_call_max_iterations_normal(self, mock_post, llm):
        """TC-039: Max Iterations - 正常值"""
        mock_response = create_mock_response()
        mock_post.return_value = mock_response
        
        result = llm.call("test", max_iterations=10)
        assert result == "测试响应"
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_success_with_tool_calls(self, mock_post, llm):
        """TC-043: API 请求成功 - 响应包含 tool_calls"""
        tool_calls = [{
            "id": "call_123",
            "function": {"name": "test", "arguments": "{}"}
        }]
        available_functions = {"test": lambda: "result"}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {"content": "最终响应"}
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions)
        assert result == "最终响应"
        assert mock_post.call_count == 2
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_content_none_with_tool_calls(self, mock_post, llm):
        """TC-044: API 请求成功 - content 为 None 且有 tool_calls"""
        tool_calls = [{
            "id": "call_123",
            "function": {"name": "test", "arguments": "{}"}
        }]
        available_functions = {"test": lambda: "result"}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {"content": "处理完成"}
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions)
        assert result == "处理完成"
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_content_none_without_tool_calls(self, mock_post, llm):
        """TC-045: API 请求成功 - content 为 None 且无 tool_calls"""
        mock_response = create_mock_response(json_data={
            "choices": [{
                "message": {
                    "content": None
                }
            }]
        })
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="未找到 content 字段"):
            llm.call("test")
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_tool_calls_not_handled(self, mock_post, llm):
        """TC-046: API 请求成功 - 响应包含 tool_calls 但未正确处理"""
        tool_calls = [{
            "id": "call_123",
            "function": {"name": "test", "arguments": "{}"}
        }]
        # available_functions 为 None，但响应包含 tool_calls 且 content 为 None
        mock_response = create_mock_response(json_data=create_tool_calls_response(tool_calls))
        mock_post.return_value = mock_response
        
        with pytest.raises(ValueError, match="包含 tool_calls 但未正确处理"):
            llm.call("test", available_functions=None)
    
    @patch('aliyun_llm.requests.post')
    def test_call_api_http_error(self, mock_post, llm):
        """TC-049: API 请求失败 - HTTP 错误状态码"""
        import requests
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response
        
        # 代码会将 HTTPError 转换为 RuntimeError
        with pytest.raises(RuntimeError, match="请求失败"):
            llm.call("test")


# ==================== 第四批：Function Calling 测试 ====================

class TestFunctionCalls:
    """测试 Function Calling 功能"""
    
    @pytest.fixture
    def llm(self):
        """创建测试用的 LLM 实例"""
        with patch('aliyun_llm.os.getenv', return_value=None):
            return AliyunLLM(model="qwen-plus", api_key="sk-test")
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_single_tool(self, mock_post, llm):
        """TC-054: 正常工具调用 - 单个工具"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "get_weather",
                "arguments": '{"city": "北京"}'
            }
        }]
        
        available_functions = {
            "get_weather": lambda city: f"{city}天气晴朗"
        }
        
        # 第一次调用返回 tool_calls，第二次返回正常响应
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {
                        "content": "北京天气晴朗"
                    }
                }]
            })
        ]
        
        result = llm.call("北京天气怎么样", available_functions=available_functions)
        assert result == "北京天气晴朗"
        assert mock_post.call_count == 2
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_missing_id(self, mock_post, llm):
        """TC-056: Tool Call - 缺少 id 字段"""
        tool_calls = [{
            "function": {
                "name": "get_weather",
                "arguments": "{}"
            }
        }]
        
        mock_post.return_value = create_mock_response(
            json_data=create_tool_calls_response(tool_calls)
        )
        
        available_functions = {"get_weather": lambda: "sunny"}
        
        with pytest.raises(ValueError, match="缺少 id 字段"):
            llm.call("test", available_functions=available_functions)
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_function_success(self, mock_post, llm):
        """TC-057: 函数存在 - 执行成功"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "add",
                "arguments": '{"a": 1, "b": 2}'
            }
        }]
        
        available_functions = {"add": lambda a, b: a + b}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {
                        "content": "结果是3"
                    }
                }]
            })
        ]
        
        result = llm.call("计算1+2", available_functions=available_functions)
        assert result == "结果是3"
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_function_failure(self, mock_post, llm):
        """TC-058: 函数存在 - 执行失败"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "divide",
                "arguments": '{"a": 1, "b": 0}'
            }
        }]
        
        def divide(a, b):
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        
        available_functions = {"divide": divide}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {
                        "content": "处理完成"
                    }
                }]
            })
        ]
        
        # 应该继续执行，不抛出异常
        result = llm.call("计算1/0", available_functions=available_functions)
        assert result == "处理完成"
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_function_not_found(self, mock_post, llm):
        """TC-059: 函数不存在"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "unknown_func",
                "arguments": "{}"
            }
        }]
        
        # 注意：available_functions 为空字典 {} 时，在 Python 中是 False
        # 所以不会进入 _handle_function_calls，会直接检查 content
        # 但如果 content 为 None 且有 tool_calls，会抛出错误
        # 为了测试函数不存在的情况，我们需要 available_functions 不为空，但函数名不匹配
        available_functions = {"other_func": lambda: "result"}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {
                        "content": "函数 unknown_func 不可用，已处理"
                    }
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions)
        assert result == "函数 unknown_func 不可用，已处理"
        # 验证调用了两次 API（第一次返回 tool_calls，第二次返回最终响应）
        assert mock_post.call_count == 2
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_invalid_json_args(self, mock_post, llm):
        """TC-062: 参数解析 - 无效 JSON"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "test",
                "arguments": "{invalid json}"
            }
        }]
        
        mock_post.return_value = create_mock_response(
            json_data=create_tool_calls_response(tool_calls)
        )
        
        available_functions = {"test": lambda: None}
        
        with pytest.raises(ValueError, match="无法解析函数参数"):
            llm.call("test", available_functions=available_functions)
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_multiple_tools(self, mock_post, llm):
        """TC-055: 正常工具调用 - 多个工具"""
        tool_calls = [
            {
                "id": "call_123",
                "function": {
                    "name": "get_time",
                    "arguments": "{}"
                }
            },
            {
                "id": "call_456",
                "function": {
                    "name": "get_weather",
                    "arguments": '{"city": "北京"}'
                }
            }
        ]
        
        available_functions = {
            "get_time": lambda: "2024-01-01 12:00:00",
            "get_weather": lambda city: f"{city}天气晴朗"
        }
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {
                        "content": "时间：2024-01-01 12:00:00，北京天气晴朗"
                    }
                }]
            })
        ]
        
        result = llm.call("查询时间和天气", available_functions=available_functions)
        assert result == "时间：2024-01-01 12:00:00，北京天气晴朗"
        assert mock_post.call_count == 2
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_args_string_format(self, mock_post, llm):
        """TC-060: 参数解析 - 字符串格式"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "test",
                "arguments": '{"key": "value"}'
            }
        }]
        
        available_functions = {"test": lambda key: f"Got {key}"}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {"content": "Got value"}
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions)
        assert result == "Got value"
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_args_dict_format(self, mock_post, llm):
        """TC-061: 参数解析 - 字典格式"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "test",
                "arguments": {"key": "value"}  # 字典格式，不是字符串
            }
        }]
        
        available_functions = {"test": lambda key: f"Got {key}"}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {"content": "Got value"}
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions)
        assert result == "Got value"
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_args_empty_string(self, mock_post, llm):
        """TC-063: 参数解析 - 空字符串"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "test",
                "arguments": ""  # 空字符串，应该解析为空字典
            }
        }]
        
        available_functions = {"test": lambda: "result"}
        
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {"content": "result"}
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions)
        assert result == "result"
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_max_iterations(self, mock_post, llm):
        """TC-064: 递归调用 - 达到最大迭代次数"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "test",
                "arguments": "{}"
            }
        }]
        
        # 每次都返回 tool_calls，导致无限递归
        mock_post.return_value = create_mock_response(
            json_data=create_tool_calls_response(tool_calls)
        )
        
        available_functions = {"test": lambda: "result"}
        
        with pytest.raises(RuntimeError, match="达到最大迭代次数"):
            llm.call("test", available_functions=available_functions, max_iterations=2)
    
    def test_handle_function_calls_max_iterations_zero(self, llm):
        """补充测试：_handle_function_calls 中 max_iterations 为 0"""
        tool_calls = [{
            "id": "call_123",
            "function": {"name": "test", "arguments": "{}"}
        }]
        available_functions = {"test": lambda: "result"}
        messages = []
        
        with pytest.raises(RuntimeError, match="达到最大迭代次数"):
            llm._handle_function_calls(tool_calls, messages, None, available_functions, max_iterations=0)
    
    @patch('aliyun_llm.requests.post')
    def test_handle_function_calls_normal_recursion(self, mock_post, llm):
        """TC-065: 递归调用 - 正常递归"""
        tool_calls = [{
            "id": "call_123",
            "function": {
                "name": "test",
                "arguments": "{}"
            }
        }]
        
        available_functions = {"test": lambda: "result"}
        
        # 第一次返回 tool_calls，第二次返回正常响应
        mock_post.side_effect = [
            create_mock_response(json_data=create_tool_calls_response(tool_calls)),
            create_mock_response(json_data={
                "choices": [{
                    "message": {"content": "最终结果"}
                }]
            })
        ]
        
        result = llm.call("test", available_functions=available_functions, max_iterations=5)
        assert result == "最终结果"
        assert mock_post.call_count == 2


# ==================== 第五批：辅助方法测试 ====================

class TestHelperMethods:
    """测试辅助方法"""
    
    @pytest.fixture
    def llm(self):
        """创建测试用的 LLM 实例"""
        with patch('aliyun_llm.os.getenv', return_value=None):
            return AliyunLLM(model="qwen-plus", api_key="sk-test")
    
    def test_supports_function_calling(self, llm):
        """TC-066: supports_function_calling 返回 True"""
        assert llm.supports_function_calling() is True
    
    def test_supports_stop_words(self, llm):
        """TC-067: supports_stop_words 返回 True"""
        assert llm.supports_stop_words() is True
    
    def test_validate_messages_valid_system(self, llm):
        """TC-068: 有效消息 - system"""
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        llm._validate_messages(messages)  # 不应该抛出异常
    
    def test_validate_messages_valid_user(self, llm):
        """TC-069: 有效消息 - user"""
        messages = [{"role": "user", "content": "Hello"}]
        llm._validate_messages(messages)
    
    def test_validate_messages_valid_assistant(self, llm):
        """TC-070: 有效消息 - assistant"""
        messages = [{"role": "assistant", "content": "Hi there!"}]
        llm._validate_messages(messages)
    
    def test_validate_messages_valid_assistant_with_tool_calls(self, llm):
        """TC-071: 有效消息 - assistant 有 tool_calls"""
        messages = [{"role": "assistant", "content": None, "tool_calls": []}]
        llm._validate_messages(messages)
    
    def test_validate_messages_valid_tool(self, llm):
        """TC-072: 有效消息 - tool"""
        messages = [{"role": "tool", "tool_call_id": "call_123", "content": "result"}]
        llm._validate_messages(messages)
    
    def test_validate_messages_invalid_not_dict(self, llm):
        """TC-073: 无效消息 - 非字典类型"""
        with pytest.raises(ValueError, match="必须是字典格式"):
            llm._validate_messages(["invalid"])
    
    def test_validate_messages_invalid_missing_role(self, llm):
        """TC-074: 无效消息 - 缺少 role"""
        with pytest.raises(ValueError, match="缺少 role 字段"):
            llm._validate_messages([{"content": "test"}])
    
    def test_validate_messages_invalid_role(self, llm):
        """TC-075: 无效消息 - 无效 role"""
        with pytest.raises(ValueError, match="无效的 role"):
            llm._validate_messages([{"role": "invalid_role", "content": "test"}])
    
    def test_validate_messages_invalid_user_missing_content(self, llm):
        """TC-076: 无效消息 - user 缺少 content"""
        with pytest.raises(ValueError, match="缺少 content 字段"):
            llm._validate_messages([{"role": "user"}])
    
    def test_validate_messages_invalid_assistant_missing_content(self, llm):
        """TC-077: 无效消息 - assistant 缺少 content 且无 tool_calls"""
        with pytest.raises(ValueError, match="缺少 content 字段且没有 tool_calls"):
            llm._validate_messages([{"role": "assistant"}])
    
    def test_validate_messages_invalid_tool_missing_tool_call_id(self, llm):
        """TC-078: 无效消息 - tool 缺少 tool_call_id"""
        with pytest.raises(ValueError, match="缺少 tool_call_id 字段"):
            llm._validate_messages([{"role": "tool", "content": "result"}])
    
    def test_validate_messages_invalid_tool_missing_content(self, llm):
        """TC-079: 无效消息 - tool 缺少 content"""
        with pytest.raises(ValueError, match="缺少 content 字段"):
            llm._validate_messages([{"role": "tool", "tool_call_id": "call_123"}])
    
    def test_validate_messages_partial_invalid(self, llm):
        """TC-080: 多消息验证 - 部分无效"""
        messages = [
            {"role": "user", "content": "valid"},
            {"role": "invalid", "content": "invalid"}
        ]
        with pytest.raises(ValueError, match="无效的 role"):
            llm._validate_messages(messages)
    
    def test_prepare_stop_words_none(self, llm):
        """TC-081: Stop Words - None"""
        assert llm._prepare_stop_words(None) is None
    
    def test_prepare_stop_words_empty_string(self, llm):
        """TC-082: Stop Words - 空字符串"""
        assert llm._prepare_stop_words("") is None
    
    def test_prepare_stop_words_string(self, llm):
        """TC-083: Stop Words - 非空字符串"""
        assert llm._prepare_stop_words("停止") == "停止"
    
    def test_prepare_stop_words_empty_list(self, llm):
        """TC-084: Stop Words - 空列表"""
        assert llm._prepare_stop_words([]) is None
    
    def test_prepare_stop_words_empty_list_after_check(self, llm):
        """补充测试：Stop Words - 空列表（覆盖 327 行）"""
        # 这个测试与 TC-084 相同，但确保覆盖了 327 行的 return None
        result = llm._prepare_stop_words([])
        assert result is None
    
    def test_prepare_stop_words_string_list(self, llm):
        """TC-085: Stop Words - 字符串列表"""
        assert llm._prepare_stop_words(["停止1", "停止2"]) == ["停止1", "停止2"]
    
    def test_prepare_stop_words_int_list(self, llm):
        """TC-086: Stop Words - 整数列表"""
        assert llm._prepare_stop_words([123, 456]) == [123, 456]
    
    def test_prepare_stop_words_mixed_types(self, llm):
        """TC-087: Stop Words - 混合类型错误"""
        with pytest.raises(ValueError, match="元素类型必须一致"):
            llm._prepare_stop_words(["停止", 123])
    
    def test_prepare_stop_words_mixed_types_multiple(self, llm):
        """TC-088: Stop Words - 混合类型错误（多个类型）"""
        with pytest.raises(ValueError, match="元素类型必须一致"):
            llm._prepare_stop_words(["停止", 123, 456.0])
    
    def test_prepare_stop_words_other_type(self, llm):
        """TC-089: Stop Words - 其他类型"""
        assert llm._prepare_stop_words({"key": "value"}) is None
    
    def test_get_context_window_size_long(self, llm):
        """TC-090: 模型名称包含 'long'"""
        llm.model = "qwen-long"
        assert llm.get_context_window_size() == 200000
    
    def test_get_context_window_size_max(self, llm):
        """TC-091: 模型名称包含 'max'"""
        llm.model = "qwen-max"
        assert llm.get_context_window_size() == 8192
    
    def test_get_context_window_size_plus(self, llm):
        """TC-092: 模型名称包含 'plus'"""
        llm.model = "qwen-plus"
        assert llm.get_context_window_size() == 8192
    
    def test_get_context_window_size_turbo(self, llm):
        """TC-093: 模型名称包含 'turbo'"""
        llm.model = "qwen-turbo"
        assert llm.get_context_window_size() == 8192
    
    def test_get_context_window_size_flash(self, llm):
        """TC-094: 模型名称包含 'flash'"""
        llm.model = "qwen-flash"
        assert llm.get_context_window_size() == 8192
    
    def test_get_context_window_size_case_insensitive(self, llm):
        """TC-095: 模型名称大小写不敏感"""
        llm.model = "QWEN-LONG"
        assert llm.get_context_window_size() == 200000
    
    def test_get_context_window_size_other(self, llm):
        """TC-096: 模型名称其他值"""
        llm.model = "qwen-other"
        assert llm.get_context_window_size() == 8192


# ==================== 第六批：集成测试（使用真实 API）====================

@pytest.mark.integration
class TestIntegration:
    """集成测试 - 使用真实 API（需要 API Key）"""
    
    @pytest.fixture
    def llm(self):
        """创建使用真实 API Key 的 LLM 实例"""
        api_key = os.getenv("QWEN_API_KEY")
        if not api_key:
            pytest.skip("QWEN_API_KEY 环境变量未设置，跳过集成测试")
        return AliyunLLM(model="qwen-plus", api_key=api_key, region="cn")
    
    def test_integration_basic_call(self, llm):
        """集成测试：基本调用"""
        result = llm.call("你好，请用一句话介绍你自己")
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"API 响应: {result}")
    
    def test_integration_multi_turn_conversation(self, llm):
        """集成测试：多轮对话"""
        messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "1+1等于几？"}
        ]
        result = llm.call(messages)
        assert isinstance(result, str)
        assert len(result) > 0
        print(f"多轮对话响应: {result}")
    
    def test_integration_with_temperature(self, llm):
        """集成测试：使用 temperature"""
        llm.temperature = 0.7
        result = llm.call("写一首关于春天的短诗")
        assert isinstance(result, str)
        print(f"Temperature 0.7 响应: {result}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=aliyun_llm", "--cov-report=html"])

