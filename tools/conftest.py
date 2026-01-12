"""
pytest配置文件 - 注册自定义标记
"""
import pytest


def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line(
        "markers", "integration: 集成测试，需要真实 API Key"
    )

