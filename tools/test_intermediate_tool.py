"""
测试 IntermediateTool 的类型转换功能
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.intermediate_tool import IntermediateTool, IntermediateToolSchema


def test_string_input():
    """测试字符串输入"""
    print("测试1: 字符串输入")
    tool = IntermediateTool()
    schema = IntermediateToolSchema(intermediate_product="这是一个字符串")
    result = tool._run(schema.intermediate_product)
    print(f"  输入: '这是一个字符串'")
    print(f"  输出: {result}")
    assert isinstance(schema.intermediate_product, str)
    print("  ✅ 通过\n")


def test_list_input():
    """测试列表输入"""
    print("测试2: 列表输入")
    tool = IntermediateTool()
    schema = IntermediateToolSchema(intermediate_product=["item1", "item2", "item3"])
    result = tool._run(schema.intermediate_product)
    print(f"  输入: ['item1', 'item2', 'item3']")
    print(f"  转换后: {repr(schema.intermediate_product)}")
    print(f"  输出: {result}")
    assert isinstance(schema.intermediate_product, str)
    assert schema.intermediate_product == "item1\nitem2\nitem3"
    print("  ✅ 通过\n")


def test_dict_input():
    """测试字典输入"""
    print("测试3: 字典输入")
    tool = IntermediateTool()
    schema = IntermediateToolSchema(intermediate_product={"key1": "value1", "key2": "value2"})
    result = tool._run(schema.intermediate_product)
    print(f"  输入: {{'key1': 'value1', 'key2': 'value2'}}")
    print(f"  转换后: {repr(schema.intermediate_product[:50])}...")
    print(f"  输出: {result}")
    assert isinstance(schema.intermediate_product, str)
    assert "key1" in schema.intermediate_product
    assert "value1" in schema.intermediate_product
    print("  ✅ 通过\n")


def test_nested_list_input():
    """测试嵌套列表输入（模拟实际使用场景）"""
    print("测试4: 嵌套列表输入（实际场景）")
    tool = IntermediateTool()
    input_data = [
        "1. 黄金3秒开场：黑屏渐亮→台灯光斑落在墨绿杯沿，蒸汽缓缓升腾（配ASMR轻音效）",
        "2. 沉浸式体验：'指尖碰到杯壁那刻，紧绷的肩线自己松开了——不是杯子在暖手，是它替我按下了暂停键'",
        "3. 干货植入：'7mm加厚陶瓷底+手工金裂釉（非贴纸！）：冷热不烫手，每次握杯都像被稳稳托住'",
        "4. 结尾强引导：'评论区扣【接住】，送你《独居精神避难所》书桌布景清单PDF'"
    ]
    schema = IntermediateToolSchema(intermediate_product=input_data)
    result = tool._run(schema.intermediate_product)
    print(f"  输入: 列表（4个元素）")
    print(f"  转换后长度: {len(schema.intermediate_product)} 字符")
    print(f"  输出: {result}")
    assert isinstance(schema.intermediate_product, str)
    assert "\n" in schema.intermediate_product
    assert "黄金3秒开场" in schema.intermediate_product
    print("  ✅ 通过\n")


def test_mixed_content():
    """测试混合内容（包含中文、特殊字符等）"""
    print("测试5: 混合内容（中文、特殊字符）")
    tool = IntermediateTool()
    input_data = [
        "第一项：包含emoji ✨",
        "第二项：包含标点符号，。！？",
        "第三项：包含换行符\n和制表符\t"
    ]
    schema = IntermediateToolSchema(intermediate_product=input_data)
    result = tool._run(schema.intermediate_product)
    print(f"  输入: 包含中文、emoji、特殊字符的列表")
    print(f"  转换后: {repr(schema.intermediate_product[:100])}...")
    print(f"  输出: {result}")
    assert isinstance(schema.intermediate_product, str)
    assert "✨" in schema.intermediate_product
    print("  ✅ 通过\n")


if __name__ == "__main__":
    print("=" * 60)
    print("IntermediateTool 类型转换测试")
    print("=" * 60)
    print()
    
    try:
        test_string_input()
        test_list_input()
        test_dict_input()
        test_nested_list_input()
        test_mixed_content()
        
        print("=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
    except Exception as e:
        print("=" * 60)
        print(f"❌ 测试失败: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
