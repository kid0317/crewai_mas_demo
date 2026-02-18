"""
测试 AliyunLLM 多模态消息支持
验证修复后的实现是否符合官方示例格式
"""
import os
import base64
from pathlib import Path
from llm.aliyun_llm import AliyunLLM


def encode_image(image_path: str) -> str:
    """编码函数：将本地文件转换为 Base64 编码的字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def test_multimodal_message():
    """测试多模态消息格式（按照官方示例）"""
    
    # 准备图片（使用项目中的测试图片）
    image_path = Path(__file__).parent.parent / "tools" / "20260129172715_135_6.jpg"
    
    if not image_path.exists():
        print(f"❌ 测试图片不存在: {image_path}")
        return
    
    # 编码图片
    base64_image = encode_image(str(image_path))
    print(f"✅ 图片编码完成，Base64 长度: {len(base64_image)}")
    
    # 创建 LLM 实例
    llm = AliyunLLM(
        model="qwen3-vl-plus",
        api_key=os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY"),
        region="cn",
    )
    
    # 按照官方示例格式构建消息
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    # 注意：根据图片格式选择正确的 MIME 类型
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}, 
                },
                {"type": "text", "text": "图中描绘的是什么景象?请详细描述。"},
            ],
        }
    ]
    
    print("\n" + "=" * 80)
    print("测试多模态消息格式")
    print("=" * 80)
    print(f"\n消息格式:")
    import json
    print(json.dumps(messages, ensure_ascii=False, indent=2))
    print("\n" + "=" * 80)
    
    try:
        # 调用 LLM
        print("\n发送请求到阿里云 API...")
        response = llm.call(messages)
        
        print("\n" + "=" * 80)
        print("✅ 请求成功！")
        print("=" * 80)
        print(f"\n响应内容:\n{response}")
        
    except Exception as e:
        print(f"\n❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()


def test_message_validation():
    """测试消息验证功能"""
    llm = AliyunLLM(
        model="qwen-plus",
        api_key=os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY"),
        region="cn",
    )
    
    print("\n" + "=" * 80)
    print("测试消息验证")
    print("=" * 80)
    
    # 测试 1: 有效的多模态消息
    valid_multimodal = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Hello"},
                {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
            ]
        }
    ]
    try:
        llm._validate_messages(valid_multimodal)
        print("✅ 测试 1 通过：有效的多模态消息")
    except Exception as e:
        print(f"❌ 测试 1 失败：{e}")
    
    # 测试 2: 无效的多模态消息（缺少 type）
    invalid_multimodal = [
        {
            "role": "user",
            "content": [
                {"text": "Hello"},  # 缺少 type
            ]
        }
    ]
    try:
        llm._validate_messages(invalid_multimodal)
        print("❌ 测试 2 失败：应该检测到缺少 type 字段")
    except ValueError as e:
        print(f"✅ 测试 2 通过：正确检测到错误 - {e}")
    
    # 测试 3: 无效的多模态消息（image_url 格式错误）
    invalid_image_url = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": "invalid"}  # 应该是字典
            ]
        }
    ]
    try:
        llm._validate_messages(invalid_image_url)
        print("❌ 测试 3 失败：应该检测到 image_url 格式错误")
    except ValueError as e:
        print(f"✅ 测试 3 通过：正确检测到错误 - {e}")


if __name__ == "__main__":
    print("=" * 80)
    print("AliyunLLM 多模态消息支持测试")
    print("=" * 80)
    
    # 测试消息验证
    test_message_validation()
    
    # 测试实际 API 调用（需要 API Key）
    api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        print("\n" + "=" * 80)
        print("检测到 API Key，开始测试实际 API 调用...")
        print("=" * 80)
        test_multimodal_message()
    else:
        print("\n⚠️  未检测到 API Key，跳过实际 API 调用测试")
        print("   设置环境变量 QWEN_API_KEY 或 DASHSCOPE_API_KEY 以启用 API 测试")
