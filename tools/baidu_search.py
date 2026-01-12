"""
百度搜索工具 - 基于百度千帆搜索 API 的 CrewAI 工具
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
        description="搜索查询内容，即用户要搜索的问题或关键词。不能为空，不能只包含空白字符。"
    )
    api_key: Optional[str] = Field(
        None, 
        description="百度千帆 AppBuilder API Key，用于API鉴权。如果不提供，将从环境变量 BAIDU_API_KEY 中读取。"
    )
    resource_type: Optional[Literal["web", "video", "image", "aladdin"]] = Field(
        "web",
        description="主要搜索的资源类型: web(网页,最大top_k=50), video(视频,最大top_k=10), image(图片,最大top_k=30), aladdin(阿拉丁,最大top_k=5)。默认为web。"
    )
    top_k: Optional[int] = Field(
        20,
        description="返回的搜索结果数量。web类型最大50, video类型最大10, image类型最大30, aladdin类型最大5。默认为20。"
    )
    enable_video: Optional[bool] = Field(
        False,
        description="是否同时搜索视频类型。如果为True，会在主要资源类型基础上额外搜索视频，最多返回10条视频结果。"
    )
    enable_image: Optional[bool] = Field(
        False,
        description="是否同时搜索图片类型。如果为True，会在主要资源类型基础上额外搜索图片，最多返回30条图片结果。"
    )
    enable_aladdin: Optional[bool] = Field(
        False,
        description="是否同时搜索阿拉丁类型。如果为True，会在主要资源类型基础上额外搜索阿拉丁，最多返回5条阿拉丁结果。注意：阿拉丁不支持站点和时效过滤。"
    )
    edition: Optional[Literal["standard", "lite"]] = Field(
        "standard",
        description="搜索版本: standard(完整版本，效果更好但时延较长), lite(精简版本，时延更短但效果略弱)。默认为standard。"
    )
    search_recency_filter: Optional[Literal["week", "month", "semiyear", "year"]] = Field(
        None,
        description="根据网页发布时间进行筛选: week(最近7天), month(最近30天), semiyear(最近180天), year(最近365天)。"
        "此参数仅对网页类型有效，视频、图片等类型不受影响。"
    )
    sites: Optional[List[str]] = Field(
        None,
        description="指定搜索的站点列表，仅在设置的站点中进行内容搜索。最多支持20个站点。"
        "示例: ['www.weather.com.cn', 'news.baidu.com']。注意：阿拉丁类型不支持站点过滤。"
    )
    block_websites: Optional[List[str]] = Field(
        None,
        description="需要屏蔽的站点列表，会过滤掉该站点及其子站点的搜索结果。"
        "示例: ['tieba.baidu.com']。使用此参数可能会增加请求时延。"
    )
    page_time_gte: Optional[str] = Field(
        None,
        description="网页发布时间范围查询-起始时间（大于等于）。格式: 'now/d', 'now-1w/d', 'now-1M/d', 'now-1y/d'等。"
        "必须与page_time_lte同时使用才生效。仅对网页类型有效。"
    )
    page_time_lte: Optional[str] = Field(
        None,
        description="网页发布时间范围查询-结束时间（小于等于）。格式: 'now/d', 'now-1w/d', 'now-1M/d', 'now-1y/d'等。"
        "必须与page_time_gte同时使用才生效。仅对网页类型有效。"
    )
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """验证查询内容不为空"""
        if not v or not v.strip():
            raise ValueError(
                "参数验证失败：查询内容不能为空。"
                "请提供有效的搜索关键词或问题。"
            )
        return v.strip()
    
    @field_validator('sites')
    @classmethod
    def validate_sites(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """验证站点数量"""
        if v and len(v) > 20:
            raise ValueError(
                "参数验证失败：站点列表最多支持20个站点。"
                f"当前提供了{len(v)}个站点，请减少到20个以内。"
            )
        return v
    
    @field_validator('top_k')
    @classmethod
    def validate_top_k(cls, v: int) -> int:
        """验证top_k范围"""
        if v < 0:
            raise ValueError(
                "参数验证失败：top_k必须大于等于0。"
                f"当前值：{v}，请提供非负整数。"
            )
        # 注意：最大值的验证在_run方法中根据resource_type进行
        return v


class BaiduSearchTool(BaseTool):
    """
    百度搜索工具
    
    使用百度千帆搜索 API 进行网络搜索，支持网页、视频、图片、阿拉丁等多种资源类型的搜索。
    需要百度千帆 API Key 进行鉴权。
    """
    name: str = "百度搜索"
    description: str = (
        "使用百度搜索引擎查找相关信息。"
        "支持搜索网页、视频、图片、阿拉丁等多种类型的内容。"
        "可以按时间范围、指定站点等条件筛选搜索结果。"
        "返回结果包含标题、链接、内容摘要、相关性评分、权威性评分等详细信息。"
        "需要提供百度千帆 AppBuilder API Key（可通过api_key参数或BAIDU_API_KEY环境变量提供）。"
    )
    args_schema: Type[BaseModel] = BaiduSearchInput

    def _run(
        self,
        query: str,
        api_key: Optional[str] = None,
        resource_type: str = "web",
        top_k: int = 20,
        enable_video: bool = False,
        enable_image: bool = False,
        enable_aladdin: bool = False,
        edition: str = "standard",
        search_recency_filter: Optional[str] = None,
        sites: Optional[List[str]] = None,
        block_websites: Optional[List[str]] = None,
        page_time_gte: Optional[str] = None,
        page_time_lte: Optional[str] = None,
    ) -> str:
        """
        执行百度搜索
        
        Args:
            query: 搜索查询内容
            api_key: 百度千帆 API Key，如果不提供则从环境变量读取
            resource_type: 主要搜索的资源类型
            top_k: 主要资源类型的返回数量
            enable_video: 是否同时搜索视频
            enable_image: 是否同时搜索图片
            enable_aladdin: 是否同时搜索阿拉丁
            edition: 搜索版本，standard/lite
            search_recency_filter: 时间筛选，week/month/semiyear/year
            sites: 指定搜索站点列表
            block_websites: 屏蔽站点列表
            page_time_gte: 发布时间范围查询起始时间
            page_time_lte: 发布时间范围查询结束时间
            
        Returns:
            格式化的搜索结果字符串，包含标题、链接、内容、评分等详细信息
        """

        # 获取 API Key
        api_key = os.getenv("BAIDU_API_KEY")
        # 记录搜索开始
        logger.info("=" * 80)
        logger.info("开始执行百度搜索")
        logger.info(f"搜索关键词: {query}")
        logger.info(f"资源类型: {resource_type}, top_k: {top_k}")
        
        # 记录额外资源类型
        extra_types = []
        if enable_video:
            extra_types.append("video")
        if enable_image:
            extra_types.append("image")
        if enable_aladdin:
            extra_types.append("aladdin")
        if extra_types:
            logger.info(f"额外资源类型: {', '.join(extra_types)}")
        
        # 记录过滤条件
        filters = []
        if search_recency_filter:
            filters.append(f"时间筛选: {search_recency_filter}")
        if sites:
            filters.append(f"指定站点: {', '.join(sites[:3])}{'...' if len(sites) > 3 else ''}")
        if block_websites:
            filters.append(f"屏蔽站点: {', '.join(block_websites[:3])}{'...' if len(block_websites) > 3 else ''}")
        if page_time_gte and page_time_lte:
            filters.append(f"时间范围: {page_time_gte} ~ {page_time_lte}")
        if filters:
            logger.info(f"过滤条件: {'; '.join(filters)}")
        
        
        if not api_key:
            error_msg = (
                "搜索失败：缺少API认证密钥。\n"
                "原因：未提供百度千帆 AppBuilder API Key。\n"
                "解决方案：\n"
                "1. 通过 api_key 参数传入API Key\n"
                "2. 或设置环境变量 BAIDU_API_KEY\n"
                "提示：API Key可从百度智能云千帆控制台获取。"
            )
            logger.error("API Key缺失，搜索失败")
            return error_msg
        
        # 验证并设置资源类型配置
        max_top_k_map = {
            "web": 50,
            "video": 10,
            "image": 30,
            "aladdin": 5
        }
        
        # 验证主要资源类型的top_k
        max_k = max_top_k_map.get(resource_type, 50)
        original_top_k = top_k
        if top_k > max_k:
            logger.warning(f"top_k={top_k} 超出 {resource_type} 类型最大值 {max_k}，自动修正为 {max_k}")
            top_k = max_k
        
        # 构建资源类型过滤器列表
        resource_type_filter = [
            {"type": resource_type, "top_k": top_k}
        ]
        
        # 添加额外的资源类型
        if enable_video:
            resource_type_filter.append({"type": "video", "top_k": 10})
        if enable_image:
            resource_type_filter.append({"type": "image", "top_k": 30})
        if enable_aladdin:
            resource_type_filter.append({"type": "aladdin", "top_k": 5})
        
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
            "edition": edition
        }
        
        # 添加时间筛选
        if search_recency_filter:
            payload["search_recency_filter"] = search_recency_filter
        
        # 构建search_filter
        search_filter = {}
        
        # 添加站点过滤
        if sites:
            search_filter["match"] = {"site": sites}
        
        # 添加时间范围查询
        if page_time_gte or page_time_lte:
            if page_time_gte and page_time_lte:
                if "range" not in search_filter:
                    search_filter["range"] = {}
                search_filter["range"]["page_time"] = {}
                if page_time_gte:
                    search_filter["range"]["page_time"]["gte"] = page_time_gte
                if page_time_lte:
                    search_filter["range"]["page_time"]["lte"] = page_time_lte
            else:
                error_msg = (
                    "搜索失败：时间范围查询参数不完整。\n"
                    "原因：page_time_gte 和 page_time_lte 必须同时提供才能使用时间范围查询。\n"
                    "解决方案：同时提供两个参数，例如：\n"
                    "- page_time_gte: 'now-1w/d' (起始时间)\n"
                    "- page_time_lte: 'now/d' (结束时间)\n"
                    "提示：此功能仅对网页类型搜索结果有效。"
                )
                logger.error("时间范围查询参数不完整")
                return error_msg
        
        # 如果有search_filter，添加到payload
        if search_filter:
            payload["search_filter"] = search_filter
        
        # 添加屏蔽站点
        if block_websites:
            payload["block_websites"] = block_websites
        
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
                    "400": "请求参数错误，请检查输入的参数是否正确",
                    "500": "服务器内部错误，请稍后重试",
                    "501": "服务调用超时，请稍后重试",
                    "502": "服务响应超时，请稍后重试",
                    "216003": "API Key认证失败，请检查API Key是否正确或是否已过期",
                }
                
                error_hint = error_descriptions.get(str(error_code), "")
                if error_hint:
                    error_hint = f"\n提示：{error_hint}"
                
                error_result = (
                    f"搜索失败：API返回错误。\n"
                    f"错误信息：{error_msg}\n"
                    f"错误码：{error_code}\n"
                    f"请求ID：{request_id}"
                    f"{error_hint}"
                )
                logger.error(f"API返回错误: 错误码={error_code}, 错误信息={error_msg}")
                return error_result
            
            # 格式化搜索结果
            references = result.get("references", [])
            if not references:
                no_result_msg = (
                    f"搜索完成，但未找到相关结果。\n"
                    f"搜索关键词：{query}\n"
                    f"建议：\n"
                    f"1. 尝试使用不同的关键词或更通用的搜索词\n"
                    f"2. 检查是否使用了过于严格的过滤条件（如站点限制、时间范围等）\n"
                    f"3. 尝试调整资源类型（如启用视频、图片等类型）"
                )
                logger.warning(f"搜索完成，但未找到相关结果 (关键词: {query})")
                return no_result_msg
            
            # 按类型分组统计
            type_counts = {}
            for ref in references:
                ref_type = ref.get("type", "unknown")
                type_counts[ref_type] = type_counts.get(ref_type, 0) + 1
            
            # 记录搜索结果统计
            logger.info(f"搜索成功！找到 {len(references)} 条结果")
            if len(type_counts) > 1:
                type_summary = ", ".join([f"{k}:{v}条" for k, v in type_counts.items()])
                logger.info(f"结果类型分布: {type_summary}")
            else:
                logger.info(f"结果类型: {list(type_counts.keys())[0] if type_counts else 'unknown'}")
            
            # 构建结果字符串
            results = []
            results.append(f"找到 {len(references)} 条搜索结果")
            if len(type_counts) > 1:
                type_summary = ", ".join([f"{k}:{v}条" for k, v in type_counts.items()])
                results.append(f"类型分布: {type_summary}")
            results.append("")
            
            for ref in references:
                ref_id = ref.get("id", "?")
                title = ref.get("title", "无标题")
                url = ref.get("url", "")
                content = ref.get("content", "")
                date = ref.get("date", "")
                ref_type = ref.get("type", "unknown")
                website = ref.get("website", "")
                web_anchor = ref.get("web_anchor", "")
                rerank_score = ref.get("rerank_score")
                authority_score = ref.get("authority_score")
                
                result_text = f"[{ref_id}] {title}"
                if url:
                    result_text += f"\n  链接: {url}"
                if website:
                    result_text += f"\n  站点: {website}"
                if web_anchor:
                    result_text += f"\n  锚文本: {web_anchor}"
                if date:
                    result_text += f"\n  日期: {date}"
                result_text += f"\n  类型: {ref_type}"
                
                # 添加评分信息
                if rerank_score is not None:
                    result_text += f"\n  相关性评分: {rerank_score:.3f}"
                if authority_score is not None:
                    result_text += f"\n  权威性评分: {authority_score:.3f}"
                
                # 添加图片/视频信息
                if ref.get("image"):
                    img = ref["image"]
                    result_text += f"\n  图片: {img.get('url', '')} ({img.get('width', '')}x{img.get('height', '')})"
                if ref.get("video"):
                    video = ref["video"]
                    result_text += f"\n  视频: {video.get('url', '')} (时长: {video.get('duration', '')}秒)"
                
                # 添加内容预览
                if content:
                    # 限制内容长度，显示前800字符
                    content_preview = content[:800] + "..." if len(content) > 800 else content
                    result_text += f"\n  内容摘要: {content_preview}"
                
                results.append(result_text)
                results.append("")  # 空行分隔
            
            final_result = "\n".join(results)
            logger.info("搜索结果格式化完成")
            logger.info("=" * 80)
            return final_result
            
        except requests.exceptions.Timeout:
            error_msg = (
                "搜索失败：请求超时。\n"
                "原因：服务器响应时间超过30秒。\n"
                "解决方案：\n"
                "1. 检查网络连接是否正常\n"
                "2. 稍后重试搜索请求\n"
                "3. 如果问题持续，可能是服务器繁忙，建议稍后再试"
            )
            logger.error("请求超时: 服务器响应时间超过30秒")
            logger.info("=" * 80)
            return error_msg
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "未知"
            error_msg = (
                f"搜索失败：HTTP请求错误。\n"
                f"状态码：{status_code}\n"
                f"错误详情：{str(e)}\n"
                f"解决方案：\n"
                f"1. 检查API Key是否正确\n"
                f"2. 检查网络连接\n"
                f"3. 如果状态码为401/403，请检查API Key权限\n"
                f"4. 如果状态码为429，表示请求过于频繁，请稍后重试"
            )
            logger.error(f"HTTP请求错误: 状态码={status_code}, 错误={str(e)}")
            logger.info("=" * 80)
            return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = (
                f"搜索失败：网络请求异常。\n"
                f"错误类型：{type(e).__name__}\n"
                f"错误详情：{str(e)}\n"
                f"解决方案：\n"
                f"1. 检查网络连接是否正常\n"
                f"2. 检查API端点是否可访问\n"
                f"3. 稍后重试"
            )
            logger.error(f"网络请求异常: {type(e).__name__} - {str(e)}")
            logger.info("=" * 80)
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = (
                "搜索失败：响应解析错误。\n"
                "原因：服务器返回的响应不是有效的JSON格式。\n"
                f"错误详情：{str(e)}\n"
                "解决方案：\n"
                "1. 可能是服务器临时故障，请稍后重试\n"
                "2. 如果问题持续，请联系技术支持"
            )
            logger.error(f"JSON解析错误: {str(e)}")
            logger.info("=" * 80)
            return error_msg
        except Exception as e:
            error_msg = (
                f"搜索失败：发生未预期的错误。\n"
                f"错误类型：{type(e).__name__}\n"
                f"错误详情：{str(e)}\n"
                f"解决方案：请检查输入参数是否正确，或联系技术支持"
            )
            logger.exception(f"未预期的错误: {type(e).__name__} - {str(e)}")
            logger.info("=" * 80)
            return error_msg

