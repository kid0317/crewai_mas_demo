"""
百度搜索工具集成测试
使用真实API Key进行端到端测试，覆盖主要功能分支
"""
import os
import pytest
from baidu_search import BaiduSearchTool


# 从环境变量读取API Key，测试时必须提供
API_KEY = os.getenv("BAIDU_API_KEY")
if not API_KEY:
    raise ValueError(
        "BAIDU_API_KEY 环境变量未设置。"
        "请设置环境变量 BAIDU_API_KEY 后再运行集成测试。"
    )


@pytest.fixture
def tool():
    """创建工具实例"""
    return BaiduSearchTool()


@pytest.mark.integration
class TestBaiduSearchIntegration:
    """集成测试 - 使用真实API"""
    
    def test_basic_web_search(self, tool):
        """测试基本网页搜索"""
        result = tool._run(
            query="北京有哪些旅游景区"
        )
        
        # 验证返回结果
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        
        # 验证结果格式
        assert "找到" in result or "搜索结果" in result or "未找到" in result
        
        # 不应该包含错误信息
        assert "缺少API认证密钥" not in result
        assert "错误" not in result or "未找到相关搜索结果" in result
    
    def test_search_with_top_k(self, tool):
        """测试指定返回数量"""
        result = tool._run(
            query="Python编程教程",
            top_k=5
        )
        
        assert result is not None
        assert isinstance(result, str)
        # 验证结果格式正确
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_search_with_time_filter(self, tool):
        """测试时间筛选"""
        result = tool._run(
            query="最新科技新闻",
            search_recency_filter="week"
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_search_with_sites_filter(self, tool):
        """测试站点过滤"""
        result = tool._run(
            query="天气",
            sites=["www.weather.com.cn"]
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_complex_query(self, tool):
        """测试复杂查询（所有参数组合）"""
        result = tool._run(
            query="人工智能最新进展",
            top_k=10,
            search_recency_filter="month",
            sites=["www.baidu.com"]
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_empty_query_handling(self, tool):
        """测试空查询处理（应该被参数验证拦截）"""
        # 这个测试验证参数验证是否工作
        # 空查询应该在参数验证阶段被拦截
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            from baidu_search import BaiduSearchInput
            BaiduSearchInput(query="")
    
    def test_invalid_api_key(self, tool):
        """测试无效API Key"""
        # 临时设置无效的API Key
        original_key = os.environ.get("BAIDU_API_KEY")
        try:
            os.environ["BAIDU_API_KEY"] = "invalid_api_key_12345"
            
            result = tool._run(query="测试")
            
            # 应该返回错误信息
            assert result is not None
            assert isinstance(result, str)
            # 可能返回认证错误或参数错误
            assert "错误" in result or "认证" in result
        finally:
            # 恢复环境变量
            if original_key:
                os.environ["BAIDU_API_KEY"] = original_key
    
    def test_missing_api_key(self, tool):
        """测试缺失API Key"""
        # 临时清除环境变量
        original_key = os.environ.get("BAIDU_API_KEY")
        try:
            if "BAIDU_API_KEY" in os.environ:
                del os.environ["BAIDU_API_KEY"]
            
            result = tool._run(query="测试")
            
            # 应该返回API Key缺失错误
            assert "缺少API认证密钥" in result
        finally:
            # 恢复环境变量
            if original_key:
                os.environ["BAIDU_API_KEY"] = original_key
    
    def test_result_formatting(self, tool):
        """测试结果格式化"""
        result = tool._run(
            query="Python编程",
            top_k=3
        )
        
        assert result is not None
        assert isinstance(result, str)
        
        # 如果找到结果，验证格式
        if "找到" in result and "条搜索结果" in result:
            # 验证包含基本字段
            lines = result.split('\n')
            assert len(lines) > 0
    
    def test_chinese_query(self, tool):
        """测试中文查询"""
        result = tool._run(
            query="北京天气怎么样"
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_english_query(self, tool):
        """测试英文查询"""
        result = tool._run(
            query="Python programming tutorial"
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_mixed_query(self, tool):
        """测试中英文混合查询"""
        result = tool._run(
            query="Python编程教程"
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_special_characters_query(self, tool):
        """测试特殊字符查询"""
        result = tool._run(
            query="Python & 机器学习"
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_long_query(self, tool):
        """测试长查询"""
        long_query = "如何学习" * 10
        result = tool._run(
            query=long_query
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_top_k_boundary_max(self, tool):
        """测试top_k边界值（最大值）"""
        result = tool._run(
            query="Python",
            top_k=50  # web类型最大值
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert "找到" in result or "搜索结果" in result or "未找到" in result
    
    def test_no_results_scenario(self, tool):
        """测试无结果场景（使用不太可能匹配的查询）"""
        result = tool._run(
            query="这是一个非常不可能匹配的查询字符串1234567890abcdefghijklmnopqrstuvwxyz"
        )
        
        assert result is not None
        assert isinstance(result, str)
        # 应该返回"未找到相关结果"或类似消息
        assert "未找到" in result or "搜索结果" in result or "找到 0" in result

