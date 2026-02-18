"""
课程：13｜自定义工具封装：构建 Tools 的五步标准SOP 示例代码
百度搜索工具 - 基于百度千帆搜索 API 的 CrewAI 工具

演示如何按照五步标准 SOP 封装自定义工具：
1. 定义输入 Schema（BaiduSearchInput）
2. 实现工具类（继承 BaseTool）
3. 实现 _run 方法（核心逻辑）
4. 错误处理和日志记录
5. 格式化输出结果

本工具展示了：
- 工具封装：如何将 API 封装为 CrewAI 工具
- 参数验证：如何使用 Pydantic 验证输入参数
- 错误处理：如何处理各种异常情况
- 日志记录：如何记录工具调用过程
- 结果格式化：如何格式化工具输出，便于 Agent 理解

学习要点：
- BaseTool 基类：如何继承并实现自定义工具
- Pydantic Schema：如何定义和验证工具输入
- 错误处理：如何优雅地处理工具执行错误
- 工具描述：如何编写清晰的工具描述，帮助 Agent 理解工具用途
"""
import os
import json
import logging
from typing import Type, Optional, List, Dict, Any, Literal
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, field_validator

# 配置日志
logger = logging.getLogger(__name__)
# 避免重复添加handler
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    # 防止日志向上传播，避免重复输出
    logger.propagate = False


class BaiduSearchInput(BaseModel):
    """百度搜索工具的输入参数模式"""
    query: str = Field(
        ..., 
        description="搜索查询内容，即用户要搜索的问题或关键词，不能为空，不能只包含空白字符，通常由一个或几个词组成"
    )
    top_k: Optional[int] = Field(
        20,
        description="返回的搜索结果数量，默认20，在精确信息搜索时推荐5以下，广泛调研时10以上。"
    )
    recency_filter: Optional[Literal["week", "month", "semiyear", "year"]] = Field(
        None,
        description="根据网页发布时间进行筛选，可选值week(最近7天)、month(最近30天)、semiyear(最近180天)、year(最近365天)，通常根据用户需求的时效性要求来选择，常识性的问题不使用，资讯类的可能比较短。"
    )
    sites: Optional[List[str]] = Field(
        None,
        description="指定搜索的站点列表，最多支持20个站点，默认None，仅在设置的站点中进行内容搜索，示例['www.weather.com.cn', 'news.baidu.com']，通常根据需求指定权威站点，如词条类的通常是百度百科，股票类的通常是东方财富网，开源项目等通常是GitHub等。"
    )
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """验证查询内容不为空"""
        if not v or not v.strip():
            raise ValueError(
                "错误：查询内容不能为空。"
                "原因：输入的查询参数为空或只包含空白字符。"
                "解决提示：请提供有效的搜索关键词或问题。"
            )
        return v.strip()
    
    @field_validator('sites')
    @classmethod
    def validate_sites(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """验证站点数量"""
        if v and len(v) > 20:
            raise ValueError(
                f"错误：站点列表数量超出限制。"
                f"原因：当前提供了{len(v)}个站点，但最多只支持20个站点。"
                f"解决提示：请将站点列表减少到20个以内，例如只保留最关键的权威站点。"
            )
        return v
    
    @field_validator('top_k')
    @classmethod
    def validate_top_k(cls, v: int) -> int:
        """验证top_k范围"""
        if v < 0:
            raise ValueError(
                f"错误：top_k参数值无效。"
                f"原因：当前值{v}小于0，top_k必须大于等于0。"
                f"解决提示：请提供非负整数，推荐值：精确信息搜索时5以下，广泛调研时10以上，默认20。"
            )
        if v > 50:
            raise ValueError(
                f"错误：top_k参数值超出限制。"
                f"原因：当前值{v}大于50，web类型最大支持50条结果。"
                f"解决提示：请将top_k调整为50以内"
            )
        return v


class BaiduSearchTool(BaseTool):
    """
    百度搜索工具
    
    使用百度千帆搜索 API 进行网络搜索，支持网页、视频、图片、阿拉丁等多种资源类型的搜索。
    需要百度千帆 API Key 进行鉴权。
    """
    name: str = "搜索网络信息"
    description: str = (
        "使用百度搜索引擎查找相关信息，可以按时间范围、指定站点等条件筛选搜索结果。"
        "获得包含标题、链接、内容摘要等详细信息的搜索结果。"
        "触发时机：当需要查找网络上的最新信息、特定网站内容、或按时间筛选搜索结果时使用，例如查找'Python最新版本特性'、'最近一周的AI新闻'、'特定网站的技术文档'等场景。"
        "适用边界：主要搜索一些通用公开的信息，当有其他专业工具能更精确查找内部或专业知识时，不使用该工具。"
    )
    args_schema: Type[BaseModel] = BaiduSearchInput

    def _run(
        self,
        query: str,
        top_k: int = 20,
        recency_filter: Optional[str] = None,
        sites: Optional[List[str]] = None,
    ) -> str:
        """
        执行百度搜索
        
        Args:
            query: 搜索查询内容
            top_k: 主要资源类型的返回数量
            recency_filter: 时间筛选，week/month/semiyear/year
            sites: 指定搜索站点列表
            
        Returns:
            格式化的搜索结果字符串，包含标题、链接、内容、评分等详细信息
        """

        # 获取 API Key
        api_key = os.getenv("BAIDU_API_KEY")
        if not api_key:
            error_msg = (
                "错误：缺少API认证密钥。\n"
                "原因：未提供百度千帆 AppBuilder API Key，环境变量BAIDU_API_KEY未设置。\n"
                "解决提示：联系管理员设置环境变量BAIDU_API_KEY，或检查系统环境变量配置是否正确。\n"
            )
            logger.error("API Key缺失，搜索失败")
            return error_msg
        # 记录搜索开始
        logger.info("=" * 80)
        logger.info("开始执行百度搜索")
        logger.info(f"搜索关键词: {query}，top_k: {top_k}，时间筛选: {recency_filter}，站点: {sites}")
        
        # 构建资源类型过滤器列表
        resource_type_filter = [
            {"type": "web", "top_k": top_k}
        ]
        
        # 构建请求体
        payload = {
            "messages": [
                {
                    "content": query,
                    "role": "user"
                }
            ],
            "search_source": "baidu_search_v2",
            "resource_type_filter": resource_type_filter,
        }
        
        # 添加时间筛选
        if recency_filter:
            payload["search_recency_filter"] = recency_filter
        
        # 构建search_filter
        search_filter = {}
        
        # 添加站点过滤
        if sites:
            search_filter["match"] = {"site": sites}
        
        # 如果有search_filter，添加到payload
        if search_filter:
            payload["search_filter"] = search_filter
        
        # API 端点
        url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
        
        # 请求头 - 根据文档，使用 X-Appbuilder-Authorization
        headers = {
            "X-Appbuilder-Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 记录请求详情（隐藏敏感信息）
        safe_payload = payload.copy()
        safe_payload_for_log = json.dumps(safe_payload, ensure_ascii=False, indent=2)
        logger.info("发送搜索请求:")
        logger.info(f"URL: {url}")
        logger.info(f"请求体:\n{safe_payload_for_log}")
        
        try:
            # 发送请求
            logger.info("正在等待API响应...")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            logger.info(f"API响应状态码: {response.status_code}")
            
            # 解析响应
            result = response.json()
            
            # 记录响应摘要
            request_id = result.get("request_id") or result.get("requestId", "未知")
            logger.info(f"请求ID: {request_id}")
            
            # 检查错误 - 兼容两种错误格式
            # 如果存在code字段且不为0/None/空字符串，则认为是错误
            error_code = result.get("code")
            if error_code is not None and error_code != 0 and error_code != "":
                error_msg = result.get("message", "未知错误")
                
                # 根据错误码提供更友好的错误信息
                error_descriptions = {
                    "400": "请求参数错误，请检查输入的参数是否正确，确认参数格式和取值范围是否符合API要求",
                    "500": "服务器内部错误，可能是服务器临时故障，请稍后重试或尝试其它工具",
                    "501": "服务调用超时，可能是服务器处理时间过长，请稍后重试或减少请求复杂度",
                    "502": "服务响应超时，可能是服务器响应时间过长，请稍后重试或尝试其它工具",
                    "216003": "API Key认证失败，请检查API Key是否正确、是否已过期或是否有足够的权限",
                }
                
                error_hint = error_descriptions.get(str(error_code), "请检查请求参数是否正确，或稍后重试")
                
                error_result = (
                    f"错误：API返回错误。\n"
                    f"原因：百度搜索API返回错误码{error_code}，错误信息：{error_msg}，请求ID：{request_id}。\n"
                    f"解决提示：{error_hint}\n"
                )
                logger.error(f"API返回错误: 错误码={error_code}, 错误信息={error_msg}")
                return error_result
            
            # 格式化搜索结果
            references = result.get("references", [])
            if not references:
                no_result_msg = (
                    f"错误：未找到相关搜索结果。\n"
                    f"原因：使用关键词'{query}'进行搜索，但未找到匹配的结果，可能是关键词过于具体、过滤条件过于严格或资源类型限制。\n"
                    f"解决提示：1)尝试使用不同的关键词或更通用的搜索词；2)检查是否使用了过于严格的过滤条件(如站点限制、时间范围等)，适当放宽条件。\n"
                )
                logger.warning(f"搜索完成，但未找到相关结果 (关键词: {query})")
                return no_result_msg
            
            
            # 记录搜索结果统计
            logger.info(f"搜索成功！找到 {len(references)} 条结果")
            # 构建结果字符串
            results = []
            results.append(f"找到 {len(references)} 条搜索结果")
            results.append("")
            
            for ref in references:
                ref_id = ref.get("id", "?")
                title = ref.get("title", "无标题")
                url = ref.get("url", "")
                content = ref.get("content", "")
                
                result_text = f"结果{ref_id}: [ {title} ] ( {url} ) \n  内容摘要: {content} \n"
                
                results.append(result_text)
                results.append("")  # 空行分隔
            
            final_result = "\n".join(results)
            logger.info("搜索结果格式化完成")
            logger.info("=" * 80)
            return final_result
            
        except requests.exceptions.Timeout:
            error_msg = (
                "错误：请求超时。\n"
                "原因：服务器响应时间超过30秒，可能是网络延迟、服务器繁忙或请求处理时间过长。\n"
                "解决提示：1)稍后重试搜索请求；2)如果问题持续，可能是服务器繁忙，建议稍后再试或联系技术支持。\n"
            )
            logger.error("请求超时: 服务器响应时间超过30秒")
            logger.info("=" * 80)
            return error_msg
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "未知"
            error_msg = (
                f"错误：HTTP请求错误。\n"
                f"原因：HTTP请求失败，状态码{status_code}，错误详情：{str(e)}。\n"
                f"解决提示：出现请求错误，请尝试重试，反复出现请尝试其它工具"
            )
            logger.error(f"HTTP请求错误: 状态码={status_code}, 错误={str(e)}")
            logger.info("=" * 80)
            return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = (
                f"错误：网络请求异常。\n"
                f"原因：网络请求过程中发生异常，错误类型：{type(e).__name__}，错误详情：{str(e)}。\n"
                f"解决提示：请尝试重试，反复出现请尝试其它工具\n"
            )
            logger.error(f"网络请求异常: {type(e).__name__} - {str(e)}")
            logger.info("=" * 80)
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = (
                "错误：响应解析错误。\n"
                f"原因：服务器返回的响应不是有效的JSON格式，错误详情：{str(e)}。\n"
                "解决提示：1)可能是服务器临时故障，请稍后重试；2)如果问题持续，请请尝试其它工具。\n"
            )
            logger.error(f"JSON解析错误: {str(e)}")
            logger.info("=" * 80)
            return error_msg
        except Exception as e:
            error_msg = (
                f"错误：发生未预期的错误。\n"
                f"原因：程序执行过程中发生未预期的异常，错误类型：{type(e).__name__}，错误详情：{str(e)}。\n"
                f"解决提示：请检查输入参数是否正确，稍后重试，如果问题持续，请请尝试其它工具。\n"
            )
            logger.exception(f"未预期的错误: {type(e).__name__} - {str(e)}")
            logger.info("=" * 80)
            return error_msg

