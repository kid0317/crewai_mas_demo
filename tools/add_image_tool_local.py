"""
课程：10｜多模态模型：让你的Agent拥有"眼睛" 核心工具
AddImageToolLocal：本地图片加载工具

参数与描述仿照 CrewAI 的 AddImageTool，在工具内部读取本地文件，之后进行压缩，
并转为 Base64 Data URL 后返回，返回格式与 AddImageTool 一致，便于多模态 LLM 使用。

功能特点：
- 本地文件读取：直接读取本地图片文件
- 自动压缩：压缩大图片，减少传输量
- Base64 编码：转换为多模态模型可处理的格式
- 格式兼容：与 CrewAI 的 AddImageTool 格式一致

使用场景：
- Agent 需要分析本地图片时
- 多模态 Agent 处理本地图片时
- 需要将本地图片传递给多模态模型时

学习要点：
- 多模态工具：如何设计支持图片的工具
- 文件处理：如何读取和处理本地文件
- Base64 编码：如何将二进制数据转换为文本格式
- 工具兼容：如何保持与标准工具的兼容性
"""
import base64
import io
from typing import Any
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from PIL import Image

class AddImageToolLocalSchema(BaseModel):
    """与 CrewAI AddImageTool 的 schema 保持一致。"""
    image_url: str = Field(
        ...,
        description="The URL or path of the image to add",
    )
def _compress_image(raw: bytes) -> bytes:
    """
    压缩图片分辨率在4K(3840x2160)以下，并保持图片原始比例
    """
    try:
        image = Image.open(io.BytesIO(raw))
        if image.width > 3840 or image.height > 2160:
            image.thumbnail((3840, 2160))
        return image.tobytes()
    except Exception as e:
        print(f"AddImageToolLocal: error={e}")
        return None


def _local_path_to_base64_data_and_compress_url(image_url: str) -> str | None:
    """
    若 image_url 为本地文件路径，则读取并转为 data URL；否则返回 错误信息: 图片文件不存在: {image_url}。
    """
    print(f"AddImageToolLocal: image_url={image_url}")
    path = Path(image_url).expanduser().resolve()
    print(f"AddImageToolLocal: path={path}")
    if not path.is_file():
        print(f"AddImageToolLocal: path is not a file")
        return f"图片文件不存在: {image_url}"
    raw = path.read_bytes()
    print(f"AddImageToolLocal: raw={len(raw)}")
    # 压缩图片
    #raw = _compress_image(raw)
    print(f"AddImageToolLocal: raw={len(raw)}")
    b64 = base64.b64encode(raw).decode("utf-8")
    print(f"AddImageToolLocal: b64={len(b64)}")
    suffix = path.suffix.lower()
    mime = "image/jpeg"
    if suffix == ".png":
        mime = "image/png"
    elif suffix == ".gif":
        mime = "image/gif"
    elif suffix == ".webp":
        mime = "image/webp"
    elif suffix == ".bmp":
        mime = "image/bmp"
    return f"data:{mime};base64,{b64}"


class AddImageToolLocal(BaseTool):
    """将本地图片加入上下文的工具：读取本地文件并转为 Base64 后返回，格式与 AddImageTool 一致。"""

    name: str = "Add image to content Local"
    description: str = (
        "Load a local image file from the given path, compress it if necessary, "
        "and convert it to a base64 data URL format that can be processed by multimodal models. "
        "The tool only handles file loading and encoding - image analysis happens after the image is loaded."
    )
    args_schema: type[BaseModel] = AddImageToolLocalSchema

    def _run(
        self,
        image_url: str,
        **kwargs: Any,
    ) -> str:
        url = image_url.strip()

        # 已是 data URL 或 http(s) URL 则直接使用
        if url.startswith("http://") or url.startswith("https://"):
            final_url = url
        else:
            data_url = _local_path_to_base64_data_and_compress_url(url)
            final_url = data_url if data_url is not None else url

        return final_url
