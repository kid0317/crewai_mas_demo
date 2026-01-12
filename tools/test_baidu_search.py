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
        """TC-015: 未提供api_key且环境变量不存在"""
        with patch.dict(os.environ, {}, clear=True):
            result = tool._run(query="测试", api_key=None)
            assert "缺少API认证密钥" in result
            assert "解决方案" in result
    
    def test_api_key_empty_string(self, tool):
        """TC-016: api_key参数为空字符串"""
        with patch.dict(os.environ, {}, clear=True):
            result = tool._run(query="测试", api_key="")
            assert "缺少API认证密钥" in result
    
    def test_api_key_from_param(self, tool, mock_response_success):
        """TC-017: 通过参数提供api_key"""
        with patch('requests.post', return_value=mock_response_success):
            result = tool._run(query="测试", api_key="test_api_key_123")
            assert "找到" in result or "测试标题" in result
    
    def test_api_key_from_env(self, tool, mock_response_success):
        """TC-018: 通过环境变量提供api_key"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "env_api_key_456"}):
            with patch('requests.post', return_value=mock_response_success):
                result = tool._run(query="测试", api_key=None)
                assert "找到" in result or "测试标题" in result
    
    def test_api_key_param_overrides_env(self, tool, mock_response_success):
        """TC-019: 参数和环境变量都存在，优先使用参数"""
        with patch.dict(os.environ, {"BAIDU_API_KEY": "env_key"}):
            with patch('requests.post', return_value=mock_response_success) as mock_post:
                tool._run(query="测试", api_key="param_key")
                # 验证请求头中使用了param_key
                call_args = mock_post.call_args
                headers = call_args[1]['headers']
                assert "Bearer param_key" in headers['X-Appbuilder-Authorization']
    
    def test_resource_type_web_default(self, tool, mock_response_success):
        """TC-020: resource_type=web, top_k=20（默认值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['type'] == 'web'
            assert payload['resource_type_filter'][0]['top_k'] == 20
    
    def test_top_k_exceeds_max_web(self, tool, mock_response_success):
        """TC-021: resource_type=web, top_k=60（超出最大值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="web", top_k=60)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 50
    
    def test_top_k_exceeds_max_video(self, tool, mock_response_success):
        """TC-022: resource_type=video, top_k=15（超出最大值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="video", top_k=15)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 10
    
    def test_top_k_exceeds_max_image(self, tool, mock_response_success):
        """TC-023: resource_type=image, top_k=50（超出最大值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="image", top_k=50)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 30
    
    def test_top_k_exceeds_max_aladdin(self, tool, mock_response_success):
        """TC-024: resource_type=aladdin, top_k=10（超出最大值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="aladdin", top_k=10)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 5
    
    def test_resource_type_unknown(self, tool, mock_response_success):
        """TC-025: resource_type为未知值（使用默认值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="unknown", top_k=100)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            # 未知类型应该使用默认最大值50
            assert payload['resource_type_filter'][0]['top_k'] == 50
    
    def test_enable_video(self, tool, mock_response_success):
        """TC-027: 启用video类型"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", enable_video=True)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            types = [rt['type'] for rt in payload['resource_type_filter']]
            assert 'web' in types
            assert 'video' in types
    
    def test_enable_image(self, tool, mock_response_success):
        """TC-028: 启用image类型"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", enable_image=True)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            types = [rt['type'] for rt in payload['resource_type_filter']]
            assert 'web' in types
            assert 'image' in types
    
    def test_enable_aladdin(self, tool, mock_response_success):
        """TC-029: 启用aladdin类型"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", enable_aladdin=True)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            types = [rt['type'] for rt in payload['resource_type_filter']]
            assert 'web' in types
            assert 'aladdin' in types
    
    def test_enable_video_and_image(self, tool, mock_response_success):
        """TC-030: 同时启用video和image"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", enable_video=True, enable_image=True)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            types = [rt['type'] for rt in payload['resource_type_filter']]
            assert 'web' in types
            assert 'video' in types
            assert 'image' in types
    
    def test_enable_all_types(self, tool, mock_response_success):
        """TC-031: 同时启用所有类型"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", 
                     enable_video=True, enable_image=True, enable_aladdin=True)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            types = [rt['type'] for rt in payload['resource_type_filter']]
            assert len(types) == 4
            assert 'web' in types
            assert 'video' in types
            assert 'image' in types
            assert 'aladdin' in types
    
    def test_messages_format(self, tool, mock_response_success):
        """TC-033: 验证messages格式"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="北京天气", api_key="test_key")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['messages'][0]['content'] == "北京天气"
            assert payload['messages'][0]['role'] == "user"
    
    def test_search_source_fixed(self, tool, mock_response_success):
        """TC-034: 验证search_source固定值"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_source'] == "baidu_search_v2"
    
    def test_edition_standard(self, tool, mock_response_success):
        """TC-035: edition=standard（默认值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", edition="standard")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['edition'] == "standard"
    
    def test_edition_lite(self, tool, mock_response_success):
        """TC-036: edition=lite"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", edition="lite")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['edition'] == "lite"
    
    def test_search_recency_filter_week(self, tool, mock_response_success):
        """TC-037: search_recency_filter=week"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", search_recency_filter="week")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_recency_filter'] == "week"
    
    def test_search_recency_filter_month(self, tool, mock_response_success):
        """TC-038: search_recency_filter=month"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", search_recency_filter="month")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_recency_filter'] == "month"
    
    def test_search_recency_filter_semiyear(self, tool, mock_response_success):
        """TC-039: search_recency_filter=semiyear"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", search_recency_filter="semiyear")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_recency_filter'] == "semiyear"
    
    def test_search_recency_filter_year(self, tool, mock_response_success):
        """TC-040: search_recency_filter=year"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", search_recency_filter="year")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_recency_filter'] == "year"
    
    def test_search_recency_filter_none(self, tool, mock_response_success):
        """TC-041: search_recency_filter=None（不添加）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", search_recency_filter=None)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert 'search_recency_filter' not in payload
    
    def test_sites_single(self, tool, mock_response_success):
        """TC-042: sites为单个站点"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", sites=["www.weather.com.cn"])
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_filter']['match']['site'] == ["www.weather.com.cn"]
    
    def test_sites_multiple(self, tool, mock_response_success):
        """TC-043: sites为多个站点"""
        sites = ["site1.com", "site2.com", "site3.com"]
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", sites=sites)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_filter']['match']['site'] == sites
    
    def test_sites_none(self, tool, mock_response_success):
        """TC-044: sites为None（不添加search_filter）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", sites=None)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert 'search_filter' not in payload
    
    def test_page_time_both_provided(self, tool, mock_response_success):
        """TC-045: page_time_gte和page_time_lte都提供"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", 
                     page_time_gte="now-1w/d", page_time_lte="now/d")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['search_filter']['range']['page_time']['gte'] == "now-1w/d"
            assert payload['search_filter']['range']['page_time']['lte'] == "now/d"
    
    def test_page_time_only_gte(self, tool):
        """TC-046: 只提供page_time_gte"""
        result = tool._run(query="测试", api_key="test_key", 
                          page_time_gte="now-1w/d", page_time_lte=None)
        assert "时间范围查询参数不完整" in result
        assert "必须同时提供" in result
    
    def test_page_time_only_lte(self, tool):
        """TC-047: 只提供page_time_lte"""
        result = tool._run(query="测试", api_key="test_key", 
                          page_time_gte=None, page_time_lte="now/d")
        assert "时间范围查询参数不完整" in result
    
    def test_page_time_both_none(self, tool, mock_response_success):
        """TC-048: page_time_gte和page_time_lte都为None"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", 
                     page_time_gte=None, page_time_lte=None)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            if 'search_filter' in payload:
                assert 'range' not in payload['search_filter']
    
    def test_sites_and_page_time(self, tool, mock_response_success):
        """TC-049: 同时有sites和page_time范围查询"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", 
                     sites=["site.com"], 
                     page_time_gte="now-1w/d", page_time_lte="now/d")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert 'match' in payload['search_filter']
            assert 'range' in payload['search_filter']
    
    def test_block_websites_single(self, tool, mock_response_success):
        """TC-050: block_websites为单个站点"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", block_websites=["tieba.baidu.com"])
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['block_websites'] == ["tieba.baidu.com"]
    
    def test_block_websites_multiple(self, tool, mock_response_success):
        """TC-051: block_websites为多个站点"""
        sites = ["site1.com", "site2.com"]
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", block_websites=sites)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['block_websites'] == sites
    
    def test_block_websites_none(self, tool, mock_response_success):
        """TC-052: block_websites为None（不添加）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", block_websites=None)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert 'block_websites' not in payload
    
    def test_headers_format(self, tool, mock_response_success):
        """TC-053: 验证请求头格式"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key_123")
            call_args = mock_post.call_args
            headers = call_args[1]['headers']
            assert headers['X-Appbuilder-Authorization'] == "Bearer test_key_123"
            assert headers['Content-Type'] == "application/json"
    
    def test_success_single_result(self, tool):
        """TC-054: 单个网页结果"""
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
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "找到" in result
            assert "测试标题" in result
            assert "https://example.com" in result
    
    def test_success_multiple_results(self, tool):
        """TC-055: 多个网页结果"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [
                {"id": 1, "title": "标题1", "url": "url1", "type": "web"},
                {"id": 2, "title": "标题2", "url": "url2", "type": "web"},
                {"id": 3, "title": "标题3", "url": "url3", "type": "web"}
            ],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "找到 3 条搜索结果" in result
            assert "标题1" in result
            assert "标题2" in result
            assert "标题3" in result
    
    def test_success_all_fields(self, tool):
        """TC-056: 结果包含所有字段（完整字段）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "url": "https://example.com",
                "website": "example.com",
                "web_anchor": "锚文本",
                "content": "内容",
                "date": "2025-01-01",
                "type": "web",
                "rerank_score": 0.95,
                "authority_score": 0.88
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "站点: example.com" in result
            assert "锚文本: 锚文本" in result
            assert "相关性评分: 0.950" in result
            assert "权威性评分: 0.880" in result
    
    def test_success_with_image(self, tool):
        """TC-057: 结果包含图片信息"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "type": "image",
                "image": {
                    "url": "https://example.com/img.jpg",
                    "width": "800",
                    "height": "600"
                }
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "图片:" in result
            assert "800x600" in result
    
    def test_success_with_video(self, tool):
        """TC-058: 结果包含视频信息"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "type": "video",
                "video": {
                    "url": "https://example.com/video.mp4",
                    "duration": "120"
                }
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "视频:" in result
            assert "120秒" in result
    
    def test_content_truncate_over_800(self, tool):
        """TC-059: 内容超过800字符的截断"""
        long_content = "a" * 1000
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "content": long_content,
                "type": "web"
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert len([line for line in result.split('\n') if '内容摘要:' in line][0]) < len(long_content) + 50
            assert "..." in result
    
    def test_content_exactly_800(self, tool):
        """TC-060: 内容正好800字符（边界值）"""
        content_800 = "a" * 800
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "content": content_800,
                "type": "web"
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            # 应该完整显示，不加"..."
            assert content_800 in result
    
    def test_content_under_800(self, tool):
        """TC-061: 内容少于800字符"""
        short_content = "短内容"
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "content": short_content,
                "type": "web"
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert short_content in result
    
    def test_multiple_types_results(self, tool):
        """TC-062: 多类型结果（web + video）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [
                {"id": 1, "title": "网页1", "type": "web"},
                {"id": 2, "title": "视频1", "type": "video"}
            ],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "类型分布:" in result
            assert "web:" in result
            assert "video:" in result
    
    def test_single_type_results(self, tool):
        """TC-063: 单类型结果（只有web）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [
                {"id": 1, "title": "网页1", "type": "web"},
                {"id": 2, "title": "网页2", "type": "web"}
            ],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            # 单类型不应该显示类型分布
            assert "类型分布:" not in result
    
    def test_missing_fields(self, tool):
        """TC-064: 结果字段缺失（部分字段为None或不存在）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "type": "web"
                # 缺少url, date, website等字段
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "标题" in result
            # 缺失字段不应该导致错误
    
    def test_rerank_score_none(self, tool):
        """TC-065: rerank_score为None"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "type": "web",
                "rerank_score": None
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "相关性评分:" not in result
    
    def test_authority_score_none(self, tool):
        """TC-066: authority_score为None"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{
                "id": 1,
                "title": "标题",
                "type": "web",
                "authority_score": None
            }],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "权威性评分:" not in result
    
    def test_empty_references(self, tool):
        """TC-067: references为空列表"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试关键词", api_key="test_key")
            assert "未找到相关结果" in result
            assert "测试关键词" in result
            assert "建议：" in result  # 使用中文冒号
    
    def test_no_references_field(self, tool):
        """TC-068: references字段不存在"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试关键词", api_key="test_key")
            assert "未找到相关结果" in result
    
    def test_error_code_400(self, tool):
        """TC-069: 错误码400（参数错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400",
            "message": "请求参数错误",
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "搜索失败" in result
            assert "400" in result
            assert "请求参数错误" in result
            assert "提示：" in result
    
    def test_error_code_500(self, tool):
        """TC-070: 错误码500（服务器错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "500",
            "message": "服务器内部错误"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "500" in result
            assert "服务器内部错误" in result
    
    def test_error_code_501(self, tool):
        """TC-071: 错误码501（调用超时）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "501",
            "message": "调用模型服务超时"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "501" in result
    
    def test_error_code_502(self, tool):
        """TC-072: 错误码502（响应超时）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "502",
            "message": "模型流式输出超时"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "502" in result
    
    def test_error_code_216003(self, tool):
        """TC-073: 错误码216003（认证失败）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "216003",
            "message": "Authentication error",
            "requestId": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "216003" in result
            assert "API Key认证失败" in result
    
    def test_error_code_unknown(self, tool):
        """TC-074: 未知错误码"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "9999",
            "message": "未知错误"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "9999" in result
            assert "未知错误" in result
    
    def test_error_code_zero(self, tool):
        """TC-075: 错误码为0（不是错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "references": [{"id": 1, "title": "标题", "type": "web"}],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "找到" in result or "标题" in result
    
    def test_error_code_empty_string(self, tool):
        """TC-076: 错误码为空字符串（不是错误）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "",
            "references": [{"id": 1, "title": "标题", "type": "web"}],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "找到" in result or "标题" in result
    
    def test_no_code_field(self, tool):
        """TC-077: code字段不存在（成功响应）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "references": [{"id": 1, "title": "标题", "type": "web"}],
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "找到" in result or "标题" in result
    
    def test_request_id_camelcase(self, tool):
        """TC-078: requestId字段（驼峰命名）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400",
            "requestId": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "test-123" in result
    
    def test_request_id_snakecase(self, tool):
        """TC-079: request_id字段（下划线命名）"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400",
            "request_id": "test-123"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "test-123" in result
    
    def test_no_message_field(self, tool):
        """TC-080: message字段缺失"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": "400"
        }
        mock_response.raise_for_status = Mock()
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "未知错误" in result
    
    def test_timeout_exception(self, tool):
        """TC-081: 请求超时异常"""
        with patch('requests.post', side_effect=requests.exceptions.Timeout()):
            result = tool._run(query="测试", api_key="test_key")
            assert "请求超时" in result
            assert "解决方案：" in result  # 使用中文冒号
    
    def test_http_error_401(self, tool):
        """TC-082: HTTP 401错误（未授权）"""
        mock_response = Mock()
        mock_response.status_code = 401
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch('requests.post', side_effect=error):
            result = tool._run(query="测试", api_key="test_key")
            assert "HTTP请求错误" in result
            assert "401" in result
    
    def test_http_error_403(self, tool):
        """TC-083: HTTP 403错误（禁止访问）"""
        mock_response = Mock()
        mock_response.status_code = 403
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch('requests.post', side_effect=error):
            result = tool._run(query="测试", api_key="test_key")
            assert "403" in result
    
    def test_http_error_429(self, tool):
        """TC-084: HTTP 429错误（请求过多）"""
        mock_response = Mock()
        mock_response.status_code = 429
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch('requests.post', side_effect=error):
            result = tool._run(query="测试", api_key="test_key")
            assert "429" in result
            assert "请求过于频繁" in result
    
    def test_http_error_500(self, tool):
        """TC-085: HTTP 500错误（服务器错误）"""
        mock_response = Mock()
        mock_response.status_code = 500
        error = requests.exceptions.HTTPError(response=mock_response)
        
        with patch('requests.post', side_effect=error):
            result = tool._run(query="测试", api_key="test_key")
            assert "500" in result
    
    def test_http_error_no_response(self, tool):
        """TC-086: HTTPError但response为None"""
        error = requests.exceptions.HTTPError()
        error.response = None
        
        with patch('requests.post', side_effect=error):
            result = tool._run(query="测试", api_key="test_key")
            assert "未知" in result or "HTTP请求错误" in result
    
    def test_connection_error(self, tool):
        """TC-087: ConnectionError异常"""
        with patch('requests.post', side_effect=requests.exceptions.ConnectionError()):
            result = tool._run(query="测试", api_key="test_key")
            assert "网络请求异常" in result
            assert "ConnectionError" in result
    
    def test_other_request_exception(self, tool):
        """TC-088: 其他RequestException子类异常"""
        with patch('requests.post', side_effect=requests.exceptions.TooManyRedirects()):
            result = tool._run(query="测试", api_key="test_key")
            assert "网络请求异常" in result
            assert "TooManyRedirects" in result
    
    def test_json_decode_error(self, tool):
        """TC-089: 响应不是有效JSON"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        
        with patch('requests.post', return_value=mock_response):
            result = tool._run(query="测试", api_key="test_key")
            assert "响应解析错误" in result
            assert "解决方案：" in result  # 使用中文冒号
    
    def test_unknown_exception(self, tool):
        """TC-090: 其他未预期的异常"""
        with patch('requests.post', side_effect=ValueError("Unexpected error")):
            result = tool._run(query="测试", api_key="test_key")
            assert "发生未预期的错误" in result
            assert "ValueError" in result
    
    def test_full_parameters(self, tool, mock_response_success):
        """TC-091: 所有参数都提供的完整请求"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(
                query="北京天气",
                api_key="test_key",
                resource_type="web",
                top_k=30,
                enable_video=True,
                enable_image=True,
                edition="lite",
                search_recency_filter="week",
                sites=["www.weather.com.cn"],
                block_websites=["tieba.baidu.com"],
                page_time_gte="now-1w/d",
                page_time_lte="now/d"
            )
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['edition'] == "lite"
            assert payload['search_recency_filter'] == "week"
            assert 'search_filter' in payload
            assert 'block_websites' in payload
    
    def test_minimal_parameters(self, tool, mock_response_success):
        """TC-092: 最小参数请求（只有query和api_key）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            # 验证使用默认值
            assert payload['resource_type_filter'][0]['type'] == 'web'
            assert payload['resource_type_filter'][0]['top_k'] == 20
            assert payload['edition'] == 'standard'
    
    def test_top_k_minimum(self, tool, mock_response_success):
        """TC-093: top_k=1（最小值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", top_k=1)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 1
    
    def test_top_k_max_web(self, tool, mock_response_success):
        """TC-094: top_k=50（web类型最大值）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="web", top_k=50)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 50
    
    def test_top_k_over_max_web(self, tool, mock_response_success):
        """TC-095: top_k=51（web类型超出边界）"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试", api_key="test_key", resource_type="web", top_k=51)
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['resource_type_filter'][0]['top_k'] == 50
    
    def test_query_special_chars(self, tool, mock_response_success):
        """TC-099: query包含特殊字符"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试&查询#关键词", api_key="test_key")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert payload['messages'][0]['content'] == "测试&查询#关键词"
    
    def test_query_emoji(self, tool, mock_response_success):
        """TC-100: query包含emoji"""
        with patch('requests.post', return_value=mock_response_success) as mock_post:
            tool._run(query="测试😀搜索", api_key="test_key")
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            assert "😀" in payload['messages'][0]['content']


class TestBaiduSearchToolAttributes:
    """测试工具类属性"""
    
    def test_tool_name(self):
        """TC-102: 验证工具名称"""
        tool = BaiduSearchTool()
        assert tool.name == "百度搜索"
    
    def test_tool_description(self):
        """TC-103: 验证工具描述"""
        tool = BaiduSearchTool()
        assert "百度搜索引擎" in tool.description
        assert "API Key" in tool.description
    
    def test_args_schema(self):
        """TC-104: 验证args_schema"""
        tool = BaiduSearchTool()
        assert tool.args_schema == BaiduSearchInput

