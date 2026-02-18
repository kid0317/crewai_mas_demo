"""
百度搜索工具单元测试
"""
import os
import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from pydantic import ValidationError
import requests

from baidu_search import BaiduSearchTool, BaiduSearchInput


class TestBaiduSearchInput:
    """测试 BaiduSearchInput 参数验证"""
    
    def test_query_empty_string(self):
        """TC-001: query为空字符串"""
        with pytest.raises(ValidationError) as exc_info:
            BaiduSearchInput(query="")
        assert "查询内容不能为空" in str(exc_info.value)
    
    def test_query_none(self):
        """TC-002: query为None"""
        with pytest.raises(ValidationError):
            BaiduSearchInput(query=None)
    
    def test_query_whitespace_only(self):
        """TC-003: query只包含空白字符"""
        with pytest.raises(ValidationError) as exc_info:
            BaiduSearchInput(query="   ")
        assert "查询内容不能为空" in str(exc_info.value)
    
    def test_query_newlines_only(self):
        """TC-004: query只包含换行符"""
        with pytest.raises(ValidationError):
            BaiduSearchInput(query="\n\r\f")
    
    def test_query_with_whitespace(self):
        """TC-005: query前后有空白字符"""
        result = BaiduSearchInput(query="  北京天气  ")
        assert result.query == "北京天气"
    
    def test_query_normal(self):
        """TC-006: query为正常字符串"""
        result = BaiduSearchInput(query="北京有哪些旅游景区")
        assert result.query == "北京有哪些旅游景区"
    
    def test_sites_none(self):
        """TC-007: sites为None"""
        result = BaiduSearchInput(query="测试", sites=None)
        assert result.sites is None
    
    def test_sites_empty_list(self):
        """TC-008: sites为空列表"""
        result = BaiduSearchInput(query="测试", sites=[])
        assert result.sites == []
    
    def test_sites_20_sites(self):
        """TC-009: sites包含20个站点（边界值）"""
        sites = [f"site{i}.com" for i in range(20)]
        result = BaiduSearchInput(query="测试", sites=sites)
        assert len(result.sites) == 20
    
    def test_sites_21_sites(self):
        """TC-010: sites包含21个站点（超出限制）"""
        sites = [f"site{i}.com" for i in range(21)]
        with pytest.raises(ValidationError) as exc_info:
            BaiduSearchInput(query="测试", sites=sites)
        assert "最多支持20个站点" in str(exc_info.value)
        assert "21" in str(exc_info.value)
    
    def test_sites_one_site(self):
        """TC-011: sites包含1个站点"""
        result = BaiduSearchInput(query="测试", sites=["www.weather.com.cn"])
        assert result.sites == ["www.weather.com.cn"]
    
    def test_top_k_negative(self):
        """TC-012: top_k为负数"""
        with pytest.raises(ValidationError) as exc_info:
            BaiduSearchInput(query="测试", top_k=-1)
        assert "top_k必须大于等于0" in str(exc_info.value)
        assert "-1" in str(exc_info.value)
    
    def test_top_k_zero(self):
        """TC-013: top_k为0（边界值）"""
        result = BaiduSearchInput(query="测试", top_k=0)
        assert result.top_k == 0
    
    def test_top_k_positive(self):
        """TC-014: top_k为正整数"""
        result = BaiduSearchInput(query="测试", top_k=10)
        assert result.top_k == 10
    
    def test_top_k_over_50(self):
        """TC-015: top_k超过50（验证在_run方法中，不在输入验证中）"""
        # 注意：根据实际实现，top_k的最大值验证在_run方法中根据resource_type进行
        # 输入验证中不检查最大值，所以这里只验证可以接受大于50的值
        result = BaiduSearchInput(query="测试", top_k=51)
        assert result.top_k == 51
    
    def test_top_k_50(self):
        """TC-016: top_k为50（最大值边界）"""
        result = BaiduSearchInput(query="测试", top_k=50)
        assert result.top_k == 50
    
    def test_recency_filter_valid(self):
        """TC-017: search_recency_filter有效值（在_run方法中，不在输入验证中）"""
        # 注意：search_recency_filter是_run方法的参数，不在BaiduSearchInput中
        # 这里跳过这个测试，因为BaiduSearchInput中没有这个字段
        pass
    
    def test_recency_filter_none(self):
        """TC-018: search_recency_filter为None（在_run方法中，不在输入验证中）"""
        # 注意：search_recency_filter是_run方法的参数，不在BaiduSearchInput中
        # 这里跳过这个测试，因为BaiduSearchInput中没有这个字段
        pass


class TestBaiduSearchTool:
    """测试 BaiduSearchTool 功能"""
    
    @pytest.fixture
    def tool(self):
        """创建工具实例"""
        return BaiduSearchTool()
    
    @pytest.fixture
    def mock_response_success(self):
        """Mock成功响应"""
        response = Mock()
        response.json.return_value = {
            "references": [
                {
                    "id": 1,
                    "title": "测试标题",
                    "url": "https://example.com",
                    "content": "测试内容",
                    "date": "2025-01-01",
                    "type": "web"
                }
            ],
            "request_id": "test-123"
        }
        response.raise_for_status = Mock()
        return response
    
    @pytest.fixture
    def mock_response_empty(self):
        """Mock空结果响应"""
        response = Mock()
        response.json.return_value = {
            "references": [],
            "request_id": "test-123"
        }
        response.raise_for_status = Mock()
        return response
    
    def test_api_key_missing_no_env(self, tool):
        """TC-019: API Key环境变量不存在"""
        with patch.dict(os.environ, {}, clear=True):
            result = tool._run(query="测试")
            assert "缺少API认证密钥" in result
            assert "BAIDU_API_KEY" in result
    
    def test_api_key_from_env(self, tool, mock_response_success):
        """TC-020: 通过环境变量提供api_key"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "env_api_key_456"}):
            with patch('requests.post', return_value=mock_response_success):
                result = tool._run(query="测试")
                assert "找到" in result or "测试标题" in result
    
    def test_api_key_in_headers(self, tool, mock_response_success):
        """TC-021: 验证请求头中包含API Key"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key_123"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试")
                call_args = mock_post.call_args
                headers = call_args[1]['headers']
                assert "Bearer test_key_123" in headers['X-Appbuilder-Authorization']
    
    def test_resource_type_web_default(self, tool, mock_response_success):
        """TC-022: resource_type固定为web, top_k=20（默认值）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['resource_type_filter'][0]['type'] == 'web'
                assert payload['resource_type_filter'][0]['top_k'] == 20
    
    def test_top_k_custom(self, tool, mock_response_success):
        """TC-023: 自定义top_k值"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", top_k=10)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['resource_type_filter'][0]['top_k'] == 10
    
    def test_top_k_max(self, tool, mock_response_success):
        """TC-024: top_k=50（最大值）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", top_k=50)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['resource_type_filter'][0]['top_k'] == 50
    
    def test_messages_format(self, tool, mock_response_success):
        """TC-025: 验证messages格式"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="北京天气")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['messages'][0]['content'] == "北京天气"
                assert payload['messages'][0]['role'] == "user"
    
    def test_search_source_fixed(self, tool, mock_response_success):
        """TC-026: 验证search_source固定值"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_source'] == "baidu_search_v2"
    
    def test_recency_filter_week(self, tool, mock_response_success):
        """TC-027: search_recency_filter=week"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", search_recency_filter="week")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_recency_filter'] == "week"
    
    def test_recency_filter_month(self, tool, mock_response_success):
        """TC-028: search_recency_filter=month"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", search_recency_filter="month")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_recency_filter'] == "month"
    
    def test_recency_filter_semiyear(self, tool, mock_response_success):
        """TC-029: search_recency_filter=semiyear"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", search_recency_filter="semiyear")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_recency_filter'] == "semiyear"
    
    def test_recency_filter_year(self, tool, mock_response_success):
        """TC-030: search_recency_filter=year"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", search_recency_filter="year")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_recency_filter'] == "year"
    
    def test_recency_filter_none(self, tool, mock_response_success):
        """TC-031: search_recency_filter=None（不添加）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", search_recency_filter=None)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert 'search_recency_filter' not in payload
    
    def test_sites_single(self, tool, mock_response_success):
        """TC-032: sites为单个站点"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", sites=["www.weather.com.cn"])
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_filter']['match']['site'] == ["www.weather.com.cn"]
    
    def test_sites_multiple(self, tool, mock_response_success):
        """TC-033: sites为多个站点"""
        sites = ["site1.com", "site2.com", "site3.com"]
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", sites=sites)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_filter']['match']['site'] == sites
    
    def test_sites_none(self, tool, mock_response_success):
        """TC-034: sites为None（不添加search_filter）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", sites=None)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert 'search_filter' not in payload
    
    def test_headers_format(self, tool, mock_response_success):
        """TC-035: 验证请求头格式"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key_123"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试")
                call_args = mock_post.call_args
                headers = call_args[1]['headers']
                assert headers['X-Appbuilder-Authorization'] == "Bearer test_key_123"
                assert headers['Content-Type'] == "application/json"
    
    def test_success_single_result(self, tool):
        """TC-036: 单个网页结果"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [
                {
                    "id": 1,
                    "title": "测试标题",
                    "url": "https://example.com",
                    "content": "测试内容",
                    "date": "2025-01-01",
                    "type": "web"
                }
            ],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "找到" in result
                assert "测试标题" in result
                assert "https://example.com" in result
    
    def test_success_multiple_results(self, tool):
        """TC-037: 多个网页结果"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [
                {"id": 1, "title": "标题1", "url": "url1", "content": "内容1"},
                {"id": 2, "title": "标题2", "url": "url2", "content": "内容2"},
                {"id": 3, "title": "标题3", "url": "url3", "content": "内容3"}
            ],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "找到 3 条搜索结果" in result
                assert "标题1" in result
                assert "标题2" in result
                assert "标题3" in result
    
    def test_success_basic_fields(self, tool):
        """TC-038: 结果包含基本字段"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "url": "https://example.com",
                "content": "内容摘要"
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "标题" in result
                assert "https://example.com" in result
                assert "内容摘要" in result
    
    def test_missing_fields(self, tool):
        """TC-039: 结果字段缺失（部分字段为None或不存在）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题"
                # 缺少url, content等字段
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "标题" in result
                # 缺失字段不应该导致错误
    
    def test_empty_references(self, tool):
        """TC-040: references为空列表"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试关键词")
                assert "未找到相关搜索结果" in result or "未找到相关结果" in result
                assert "测试关键词" in result
    
    def test_no_references_field(self, tool):
        """TC-041: references字段不存在"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试关键词")
                assert "未找到相关搜索结果" in result or "未找到相关结果" in result
    
    def test_error_code_400(self, tool):
        """TC-042: 错误码400（参数错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400",
            "message": "请求参数错误",
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "错误" in result
                assert "400" in result
                assert "请求参数错误" in result
    
    def test_error_code_500(self, tool):
        """TC-043: 错误码500（服务器错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "500",
            "message": "服务器内部错误"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "500" in result
                assert "服务器内部错误" in result
    
    def test_error_code_501(self, tool):
        """TC-044: 错误码501（调用超时）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "501",
            "message": "调用模型服务超时"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "501" in result
    
    def test_error_code_502(self, tool):
        """TC-045: 错误码502（响应超时）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "502",
            "message": "模型流式输出超时"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "502" in result
    
    def test_error_code_216003(self, tool):
        """TC-046: 错误码216003（认证失败）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "216003",
            "message": "Authentication error",
            "requestId": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "216003" in result
                assert "API Key认证失败" in result
    
    def test_error_code_unknown(self, tool):
        """TC-047: 未知错误码"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "9999",
            "message": "未知错误"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "9999" in result
                assert "未知错误" in result
    
    def test_error_code_zero(self, tool):
        """TC-048: 错误码为0（不是错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "references": [{"id": 1, "title": "标题", "url": "url", "content": "内容"}],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "找到" in result or "标题" in result
    
    def test_error_code_empty_string(self, tool):
        """TC-049: 错误码为空字符串（不是错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "",
            "references": [{"id": 1, "title": "标题", "url": "url", "content": "内容"}],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "找到" in result or "标题" in result
    
    def test_no_code_field(self, tool):
        """TC-050: code字段不存在（成功响应）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{"id": 1, "title": "标题", "url": "url", "content": "内容"}],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "找到" in result or "标题" in result
    
    def test_request_id_camelcase(self, tool):
        """TC-051: requestId字段（驼峰命名）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400",
            "requestId": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "test-123" in result
    
    def test_request_id_snakecase(self, tool):
        """TC-052: request_id字段（下划线命名）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400",
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "test-123" in result
    
    def test_no_message_field(self, tool):
        """TC-053: message字段缺失"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400"
        }
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "未知错误" in result
    
    def test_timeout_exception(self, tool):
        """TC-054: 请求超时异常"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=requests.exceptions.Timeout()):
                result = tool._run(query="测试")
                assert "请求超时" in result
    
    def test_http_error_401(self, tool):
        """TC-055: HTTP 401错误（未授权）"""
        mock_response = Mock()
        mock_response.status_code = 401
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=error):
                result = tool._run(query="测试")
                assert "HTTP请求错误" in result
                assert "401" in result
    
    def test_http_error_403(self, tool):
        """TC-056: HTTP 403错误（禁止访问）"""
        mock_response = Mock()
        mock_response.status_code = 403
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=error):
                result = tool._run(query="测试")
                assert "403" in result
    
    def test_http_error_500(self, tool):
        """TC-057: HTTP 500错误（服务器错误）"""
        mock_response = Mock()
        mock_response.status_code = 500
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=error):
                result = tool._run(query="测试")
                assert "500" in result
    
    def test_http_error_no_response(self, tool):
        """TC-058: HTTPError但response为None"""
        error = requests.exceptions.HTTPError()
        error.response = None
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=error):
                result = tool._run(query="测试")
                assert "未知" in result or "HTTP请求错误" in result
    
    def test_connection_error(self, tool):
        """TC-059: ConnectionError异常"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=requests.exceptions.ConnectionError()):
                result = tool._run(query="测试")
                assert "网络请求异常" in result
                assert "ConnectionError" in result
    
    def test_other_request_exception(self, tool):
        """TC-060: 其他RequestException子类异常"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=requests.exceptions.TooManyRedirects()):
                result = tool._run(query="测试")
                assert "网络请求异常" in result
                assert "TooManyRedirects" in result
    
    def test_json_decode_error(self, tool):
        """TC-061: 响应不是有效JSON"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response):
                result = tool._run(query="测试")
                assert "响应解析错误" in result
    
    def test_unknown_exception(self, tool):
        """TC-062: 其他未预期的异常"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', side_effect=ValueError("Unexpected error")):
                result = tool._run(query="测试")
                assert "发生未预期的错误" in result
                assert "ValueError" in result
    
    def test_full_parameters(self, tool, mock_response_success):
        """TC-063: 所有参数都提供的完整请求"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(
                    query="北京天气",
                    top_k=30,
                    search_recency_filter="week",
                    sites=["www.weather.com.cn"]
                )
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['search_recency_filter'] == "week"
                assert 'search_filter' in payload
                assert payload['search_filter']['match']['site'] == ["www.weather.com.cn"]
    
    def test_minimal_parameters(self, tool, mock_response_success):
        """TC-064: 最小参数请求（只有query）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                # 验证使用默认值
                assert payload['resource_type_filter'][0]['type'] == 'web'
                assert payload['resource_type_filter'][0]['top_k'] == 20
    
    def test_top_k_minimum(self, tool, mock_response_success):
        """TC-065: top_k=1（最小值）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", top_k=1)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['resource_type_filter'][0]['top_k'] == 1
    
    def test_top_k_max_web(self, tool, mock_response_success):
        """TC-066: top_k=50（web类型最大值）"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", top_k=50)
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['resource_type_filter'][0]['top_k'] == 50
    
    def test_query_special_chars(self, tool, mock_response_success):
        """TC-067: query包含特殊字符"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试&查询#关键词")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert payload['messages'][0]['content'] == "测试&查询#关键词"
    
    def test_query_emoji(self, tool, mock_response_success):
        """TC-068: query包含emoji"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "test_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试😀搜索")
                call_args = mock_post.call_args
                payload = call_args[1]['json']
                assert "😀" in payload['messages'][0]['content']


class TestBaiduSearchToolAttributes:
    """测试工具类属性"""
    
    def test_tool_name(self):
        """TC-069: 验证工具名称"""
        tool = BaiduSearchTool()
        assert tool.name == "百度搜索"
    
    def test_tool_description(self):
        """TC-070: 验证工具描述"""
        tool = BaiduSearchTool()
        assert "百度搜索引擎" in tool.description or "百度搜索" in tool.description
    
    def test_args_schema(self):
        """TC-071: 验证args_schema"""
        tool = BaiduSearchTool()
        assert tool.args_schema == BaiduSearchInput

