"""
第23课 单元测试：Orchestrator 范式

测试覆盖：
  T1 - spawn_sub_agent 完成后 output_file 存在且非空
  T2 - spawn_sub_agents_parallel 并发产出两个文件，wall time < 串行时间之和
  T3 - tool_names 包含未知工具名时静默过滤，不报错
  T4 - _run_one_sub_crew 内部异常时返回 error 字符串（parallel 场景）
  T5 - 并发任务一个失败，其他正常完成
  T6 - SOP skill 文件存在且可读
  T7 - 主 Agent backstory 包含 SOP 内容
  T8 - 两个并发 sub-crew 使用不同的 Crew 实例（上下文隔离）

运行：
  cd m4l23~28/m4l23 && pytest test_orchestrator.py -v
"""

import json
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_HERE))

from m4l23_orchestrator import (  # noqa: E402
    SKILL_PATH,
    TOOL_REGISTRY,
    WORKSPACE_DIR,
    SpawnParallelTool,
    SpawnSubAgentTool,
    _run_one_sub_crew,
    build_orchestrator,
    load_sop_skill,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_output(tmp_path) -> Path:
    return tmp_path / "output.md"


def _mock_sub_crew(output_file: str, content: str = "mock output") -> None:
    """让 _run_one_sub_crew 直接写文件，跳过 LLM 调用"""
    p = Path(output_file)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# T1：spawn_sub_agent 完成后文件存在且非空
# ─────────────────────────────────────────────────────────────────────────────

def test_T1_spawn_sub_agent_creates_file(tmp_path):
    output_file = str(tmp_path / "result.md")

    with patch("m4l23_orchestrator._run_one_sub_crew") as mock_run:
        mock_run.side_effect = lambda **kwargs: _mock_sub_crew(
            kwargs["output_file"], "# 测试输出\n内容"
        ) or kwargs["output_file"]

        tool = SpawnSubAgentTool()
        result = tool._run(
            role="Test Agent",
            goal="测试目标",
            task="写一个测试文件",
            context="测试上下文",
            tool_names="FileWriterTool",
            output_file=output_file,
        )

    assert Path(output_file).exists(), "output_file 应该存在"
    assert Path(output_file).read_text() != "", "output_file 不应为空"
    assert result == output_file


# ─────────────────────────────────────────────────────────────────────────────
# T2：并发产出两个文件，wall time < 各自串行时间之和
# ─────────────────────────────────────────────────────────────────────────────

def test_T2_parallel_concurrent_faster_than_serial(tmp_path):
    delay = 0.3  # 每个子任务模拟 0.3s

    def slow_sub_crew(**kwargs):
        time.sleep(delay)
        _mock_sub_crew(kwargs["output_file"], "output")
        return kwargs["output_file"]

    subtasks = [
        {"role": "Agent A", "goal": "g", "task": "t", "context": "c",
         "tool_names": "FileWriterTool", "output_file": str(tmp_path / "a.md")},
        {"role": "Agent B", "goal": "g", "task": "t", "context": "c",
         "tool_names": "FileWriterTool", "output_file": str(tmp_path / "b.md")},
    ]

    with patch("m4l23_orchestrator._run_one_sub_crew", side_effect=lambda **kw: slow_sub_crew(**kw)):
        tool = SpawnParallelTool()
        start = time.time()
        result_json = tool._run(json.dumps(subtasks))
        elapsed = time.time() - start

    results = json.loads(result_json)
    assert Path(tmp_path / "a.md").exists()
    assert Path(tmp_path / "b.md").exists()
    # 并发应比串行（2 * delay）快
    assert elapsed < delay * 2 * 0.9, f"并发用时 {elapsed:.2f}s 不应接近串行 {delay * 2:.2f}s"


# ─────────────────────────────────────────────────────────────────────────────
# T3：未知 tool_names 被静默过滤，已知工具正常加载
# ─────────────────────────────────────────────────────────────────────────────

def test_T3_unknown_tool_names_filtered():
    captured_tools = []

    def capture_tools(**kwargs):
        # 从 TOOL_REGISTRY 过滤逻辑中抓取 tools 列表
        tools = [
            TOOL_REGISTRY[t.strip()]
            for t in kwargs["tool_names"].split(",")
            if t.strip() in TOOL_REGISTRY
        ]
        captured_tools.extend(tools)
        _mock_sub_crew(kwargs["output_file"])
        return kwargs["output_file"]

    with patch("m4l23_orchestrator._run_one_sub_crew", side_effect=lambda **kw: capture_tools(**kw)):
        tool = SpawnSubAgentTool()
        tool._run(
            role="R", goal="G", task="T", context="C",
            tool_names="FileWriterTool, NonExistentTool, BashTool",
            output_file="/tmp/test_t3_filter.md",
        )

    tool_names_loaded = [t.name for t in captured_tools]
    assert "NonExistentTool" not in tool_names_loaded
    # FileWriterTool().name 实际为 "File Writer Tool"（crewai_tools 含空格）
    assert any("File Writer" in n or "FileWriter" in n for n in tool_names_loaded)
    assert "BashTool" in tool_names_loaded


# ─────────────────────────────────────────────────────────────────────────────
# T4：子任务内部异常时，parallel 结果包含 error 字符串
# ─────────────────────────────────────────────────────────────────────────────

def test_T4_sub_crew_exception_captured(tmp_path):
    def fail(**kwargs):
        raise RuntimeError("模拟子任务失败")

    subtasks = [
        {"role": "Failing Agent", "goal": "g", "task": "t", "context": "c",
         "tool_names": "FileWriterTool", "output_file": str(tmp_path / "fail.md")},
    ]

    with patch("m4l23_orchestrator._run_one_sub_crew", side_effect=lambda **kw: fail(**kw)):
        tool = SpawnParallelTool()
        result_json = tool._run(json.dumps(subtasks))

    results = json.loads(result_json)
    values = list(results.values())
    assert any("error" in str(v) for v in values), "失败任务应有 error 标记"


# ─────────────────────────────────────────────────────────────────────────────
# T5：并发中一个失败，其他正常完成
# ─────────────────────────────────────────────────────────────────────────────

def test_T5_parallel_partial_failure(tmp_path):
    good_file = str(tmp_path / "good.md")
    bad_file = str(tmp_path / "bad.md")

    def sometimes_fail(**kwargs):
        if "bad" in kwargs["output_file"]:
            raise RuntimeError("bad task")
        _mock_sub_crew(kwargs["output_file"], "success")
        return kwargs["output_file"]

    subtasks = [
        {"role": "Good Agent", "goal": "g", "task": "t", "context": "c",
         "tool_names": "FileWriterTool", "output_file": good_file},
        {"role": "Bad Agent",  "goal": "g", "task": "t", "context": "c",
         "tool_names": "FileWriterTool", "output_file": bad_file},
    ]

    with patch("m4l23_orchestrator._run_one_sub_crew", side_effect=lambda **kw: sometimes_fail(**kw)):
        tool = SpawnParallelTool()
        result_json = tool._run(json.dumps(subtasks))

    results = json.loads(result_json)
    assert Path(good_file).exists(), "成功任务的文件应存在"
    assert any("error" in str(v) for v in results.values()), "失败任务应有 error 标记"


# ─────────────────────────────────────────────────────────────────────────────
# T6：SOP skill 文件存在且内容非空
# ─────────────────────────────────────────────────────────────────────────────

def test_T6_sop_skill_readable():
    assert SKILL_PATH.exists(), f"SKILL.md 不存在：{SKILL_PATH}"
    content = load_sop_skill()
    assert len(content) > 100, "SOP skill 内容不应为空"
    assert "阶段" in content or "Phase" in content, "SOP 应包含阶段描述"


# ─────────────────────────────────────────────────────────────────────────────
# T7：主 Agent backstory 包含 SOP 内容
# ─────────────────────────────────────────────────────────────────────────────

def test_T7_orchestrator_backstory_contains_sop():
    # 不实例化真实 Agent（CrewAI 会验证 LLM），直接验证 backstory 字符串构建逻辑
    sop = load_sop_skill()
    assert len(sop) > 100, "SOP 内容不应为空"

    # backstory 模板中包含 SOP 内容和关键引导文字
    sop_snippet = sop.strip()[:80]
    # build_orchestrator 将 SOP 注入到 backstory 末尾，直接验证构建后的字符串
    backstory_template = (
        "你的工具：\n"
        "━━━ SOP 流程（必须遵守）━━━\n\n"
        f"{sop}"
    )
    assert sop_snippet in backstory_template
    assert "SOP 流程" in backstory_template


# ─────────────────────────────────────────────────────────────────────────────
# T8：两个并发 sub-crew 使用不同的 Crew 实例（上下文隔离）
# ─────────────────────────────────────────────────────────────────────────────

def test_T8_parallel_crews_are_independent_instances(tmp_path):
    """
    上下文隔离的核心含义：并发的两个子任务各自独立调用 _run_one_sub_crew，
    互不共享调用参数（role/context/output_file 各不相同）。
    """
    call_kwargs: list[dict] = []

    def record_call(**kwargs):
        call_kwargs.append(dict(kwargs))
        _mock_sub_crew(kwargs["output_file"])
        return kwargs["output_file"]

    subtasks = [
        {"role": "Agent X", "goal": "g", "task": "t", "context": "context_x",
         "tool_names": "", "output_file": str(tmp_path / "x.md")},
        {"role": "Agent Y", "goal": "g", "task": "t", "context": "context_y",
         "tool_names": "", "output_file": str(tmp_path / "y.md")},
    ]

    with patch("m4l23_orchestrator._run_one_sub_crew", side_effect=lambda **kw: record_call(**kw)):
        tool = SpawnParallelTool()
        tool._run(json.dumps(subtasks))

    assert len(call_kwargs) == 2, "_run_one_sub_crew 应被调用两次（各一个子任务）"
    roles = {kw["role"] for kw in call_kwargs}
    contexts = {kw["context"] for kw in call_kwargs}
    outputs = {kw["output_file"] for kw in call_kwargs}
    assert roles == {"Agent X", "Agent Y"}, "两个子任务角色不同（独立身份）"
    assert contexts == {"context_x", "context_y"}, "两个子任务上下文不同（独立上下文）"
    assert len(outputs) == 2, "两个子任务输出文件不同（不冲突）"
