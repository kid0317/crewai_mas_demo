"""
第23课·Orchestrator范式：任务层的主 Agent + 子 Agent

核心演示：
  - 主 Agent 读取 SOP skill，根据需求自主决定何时/何种子 Agent
  - spawn_sub_agent：动态创建单个子 Agent（role/task/context 运行时决定）
  - spawn_sub_agents_parallel：并发启动多个独立子 Agent
  - 文件引用传递：结果写文件，传路径而非内容
  - reject + retry：主 Agent 验收不通过时重新 spawn 修复子 Agent

运行方式：
  cd m4l23 && python3 m4l23_orchestrator.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Type

from crewai import Agent, Crew, Task
from crewai.tools import BaseTool
from crewai_tools import FileReadTool, FileWriterTool
from pydantic import BaseModel, Field

# ── 路径与项目根 sys.path ──────────────────────────────────────────────────────
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent                 # crewai_mas_demo 根目录
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from llm.aliyun_llm import AliyunLLM        # noqa: E402

# ── 常量 ──────────────────────────────────────────────────────────────────────
WORKSPACE_DIR    = _HERE / "workspace"
SKILL_PATH       = _PROJECT_ROOT / "skills" / "software-dev-sop" / "SKILL.md"
REQUIREMENTS_FILE = WORKSPACE_DIR / "requirements.md"


# ─────────────────────────────────────────────────────────────────────────────
# LLM 工厂
# ─────────────────────────────────────────────────────────────────────────────

def _llm() -> AliyunLLM:
    return AliyunLLM(model="qwen-plus", region="cn", temperature=0.7)


# ─────────────────────────────────────────────────────────────────────────────
# BashTool（crewai_tools 未内置，手动实现）
# ─────────────────────────────────────────────────────────────────────────────

class _BashInput(BaseModel):
    command: str = Field(description="需要执行的 Shell 命令")


class BashTool(BaseTool):
    name: str = "BashTool"
    description: str = (
        "在 workspace 目录下执行 Shell 命令，返回 stdout + stderr。"
        "适用于：运行 pytest、查看目录结构、执行 curl 等。"
    )
    args_schema: Type[BaseModel] = _BashInput

    def _run(self, command: str) -> str:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=str(WORKSPACE_DIR),
            timeout=60,
        )
        output = (result.stdout + result.stderr).strip()
        return output or "(no output)"


# ─────────────────────────────────────────────────────────────────────────────
# TOOL_REGISTRY：预定义工具池
# 工具池在代码中预定义；哪个子 Agent 用哪些，由主 Agent 在 spawn 时传 tool_names 决定
# ─────────────────────────────────────────────────────────────────────────────

TOOL_REGISTRY: dict[str, Any] = {
    "FileReadTool":   FileReadTool(),
    "FileWriterTool": FileWriterTool(),
    "BashTool":       BashTool(),
}


# ─────────────────────────────────────────────────────────────────────────────
# 核心：动态 sub-crew 运行器
# 每次调用都实例化全新的 Agent / Task / Crew，不共享任何状态（上下文隔离）
# ─────────────────────────────────────────────────────────────────────────────

def _run_one_sub_crew(
    role: str,
    goal: str,
    task: str,
    context: str,
    tool_names: str,
    output_file: str,
) -> str:
    """
    动态实例化一个独立 sub-crew 并运行。

    role / goal / task / context 全部由调用方（主 Agent）在运行时决定，
    这里没有任何预定义的角色类——这是 Orchestrator 范式和工作流的核心区别。
    """
    # 从工具池中按名称取工具，未知名称静默跳过
    tools = [
        TOOL_REGISTRY[t.strip()]
        for t in tool_names.split(",")
        if t.strip() in TOOL_REGISTRY
    ]

    # 确保输出目录存在
    output_path = Path(output_file)
    if not output_path.is_absolute():
        output_path = WORKSPACE_DIR / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    agent = Agent(
        role=role,
        goal=goal,
        backstory=context,
        tools=tools,
        llm=_llm(),
        verbose=True,
    )
    task_obj = Task(
        description=task,
        expected_output=f"将结果写入 {output_path}，返回该文件的绝对路径字符串",
        agent=agent,
        output_file=str(output_path),
    )
    Crew(agents=[agent], tasks=[task_obj], verbose=True).kickoff()
    return str(output_path)


# ─────────────────────────────────────────────────────────────────────────────
# spawn_sub_agent Tool
# ─────────────────────────────────────────────────────────────────────────────

class _SpawnSingleInput(BaseModel):
    role: str = Field(description="子 Agent 的角色名（你在运行时决定，如 'Frontend Developer'）")
    goal: str = Field(description="子 Agent 的目标（一句话）")
    task: str = Field(description="详细任务描述，包含所有子 Agent 需要知道的信息")
    context: str = Field(
        description="子 Agent 需要的完整上下文（显式传入，不依赖隐式共享）"
    )
    tool_names: str = Field(
        description="逗号分隔的工具名，可选：FileReadTool, FileWriterTool, BashTool"
    )
    output_file: str = Field(
        description="结果写入的文件路径（相对 workspace/ 或绝对路径）"
    )


class SpawnSubAgentTool(BaseTool):
    name: str = "spawn_sub_agent"
    description: str = (
        "动态创建并运行一个子 Agent（串行，等待完成后返回）。"
        "role / goal / task / context 由你在运行时决定，没有预定义的角色限制。"
        "子 Agent 在完全独立的上下文中运行（不知道你做过什么），"
        "完成后将结果写入 output_file，返回文件路径。"
        "适用于：需要串行执行的单个子任务，或与其他任务有依赖关系的任务。"
    )
    args_schema: Type[BaseModel] = _SpawnSingleInput

    def _run(
        self,
        role: str,
        goal: str,
        task: str,
        context: str,
        tool_names: str,
        output_file: str,
    ) -> str:
        print(f"\n[sub-agent: {role}] 启动 (独立上下文)")
        result = _run_one_sub_crew(
            role=role,
            goal=goal,
            task=task,
            context=context,
            tool_names=tool_names,
            output_file=output_file,
        )
        print(f"[sub-agent: {role}] 完成 → {result}")
        return result


# ─────────────────────────────────────────────────────────────────────────────
# spawn_sub_agents_parallel Tool
# ─────────────────────────────────────────────────────────────────────────────

class _SpawnParallelInput(BaseModel):
    subtasks_json: str = Field(
        description=(
            "JSON 数组，每项格式与 spawn_sub_agent 参数相同："
            "[{role, goal, task, context, tool_names, output_file}, ...]。"
            "你决定数组中放什么、放多少个。"
            "前提：各任务的输入不依赖对方输出，且输出目录不重叠。"
        )
    )


class SpawnParallelTool(BaseTool):
    name: str = "spawn_sub_agents_parallel"
    description: str = (
        "并发启动多个互相独立的子 Agent（所有任务同时运行）。"
        "输入：JSON 数组，每项与 spawn_sub_agent 参数相同。"
        "全部完成后返回结果 JSON：{output_file: 'done' | 'error: ...'} 。"
        "适用于：多个任务互相独立、没有先后依赖、可以并发执行的场景。"
        "注意：并发任务不能写同一个文件（会冲突）。"
    )
    args_schema: Type[BaseModel] = _SpawnParallelInput

    def _run(self, subtasks_json: str) -> str:
        subtasks: list[dict] = json.loads(subtasks_json)
        results: dict[str, str] = {}

        print(f"\n[并发启动] {len(subtasks)} 个子 Agent 同时运行...")
        for st in subtasks:
            print(f"  [{st['role']}] 启动 (独立上下文)")

        with ThreadPoolExecutor(max_workers=len(subtasks)) as executor:
            futures = {
                executor.submit(
                    _run_one_sub_crew,
                    role=st["role"],
                    goal=st["goal"],
                    task=st["task"],
                    context=st["context"],
                    tool_names=st["tool_names"],
                    output_file=st["output_file"],
                ): st["output_file"]
                for st in subtasks
            }
            for future in as_completed(futures):
                output_file = futures[future]
                try:
                    results[output_file] = future.result()
                    print(f"  [完成] → {output_file}")
                except Exception as e:
                    results[output_file] = f"error: {e}"
                    print(f"  [失败] {output_file}: {e}")

        return json.dumps(results, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# SOP Skill 加载
# ─────────────────────────────────────────────────────────────────────────────

def load_sop_skill() -> str:
    """读取 software-dev-sop SKILL.md，注入到主 Agent backstory"""
    if SKILL_PATH.exists():
        return SKILL_PATH.read_text(encoding="utf-8")
    return f"(SOP skill 未找到，期望路径：{SKILL_PATH})"


# ─────────────────────────────────────────────────────────────────────────────
# 主 Agent（Orchestrator）
# ─────────────────────────────────────────────────────────────────────────────

def build_orchestrator() -> tuple[Agent, Task]:
    sop_content = load_sop_skill()

    orchestrator = Agent(
        role="Software Development Orchestrator",
        goal=(
            "接收软件需求文档，按 SOP **一次性连续跑完**各阶段，协调子 Agent 完成设计、实现、测试与交付；"
            "不中断、不向用户提问；遇问题按 SOP 自行重试与修复。"
            "你只做拆解、派单、验收与重试，不执笔任何文档或代码。"
        ),
        backstory=(
            "你是一名有 10 年全栈经验的技术负责人，擅长把模糊需求拆解成清晰可执行的子任务。\n"
            "你的工作方式：\n"
            "1. 架构/接口/代码/报告一律由子 Agent 产出——你只读需求、spawn、用 FileReadTool 验收\n"
            "2. 给子 Agent 派任务时，总是显式传递它需要的全部信息，"
            "绝不假设它能'感知'你做过什么\n"
            "3. 独立的任务用并发子 Agent；有依赖关系的严格串行\n"
            "4. 始终按照下方 SOP 流程推进，不跳过任何阶段\n"
            "5. **一次跑完全程**：不向用户提问或求确认；遇阻自行 spawn 修复/重试，按 SOP 解决\n\n"
            "你的工具：\n"
            "- spawn_sub_agent：开一个子 Agent 执行单个任务（串行）\n"
            "- spawn_sub_agents_parallel：同时开多个互相独立的子 Agent（并发）\n"
            "- FileReadTool：读取文件内容（读需求文档、验收子 Agent 输出）\n\n"
            "━━━ SOP 流程（必须遵守）━━━\n\n"
            f"{sop_content}"
        ),
        tools=[SpawnSubAgentTool(), SpawnParallelTool(), FileReadTool()],
        llm=_llm(),
        verbose=True,
    )

    main_task = Task(
        description=(
            f"读取需求文档 {REQUIREMENTS_FILE}，按照 SOP 完成完整交付（你只协调，不执笔）：\n\n"
            "1. 阶段 1：spawn 子 Agent 产出 A（architecture.md）与 B（api_spec.md），你用 FileReadTool 分别验收\n"
            "2. 阶段 2～5：按 SOP 协调子 Agent：mock/单测 → 前后端开发 → 代码审查+测试 → 修复循环\n"
            "3. 阶段 6：spawn 子 Agent 写 workspace/delivery_report.md（仅路径引用，不复制代码），你再读取确认\n\n"
            "关键约束：\n"
            "- **一次性做完整个 SOP**，中间不要停、不要向用户提问或等待确认；有问题按 SOP 自己解决（重试、修复子 Agent）\n"
            "- spawn 子 Agent 时必须显式传递完整上下文（文件内容，不只是路径）\n"
            f"- 所有产出文件放在 {WORKSPACE_DIR}/ 下\n"
            "- 子 Agent 完成后必须用 FileReadTool 读取输出文件确认内容\n"
        ),
        expected_output=(
            "workspace/delivery_report.md 的绝对路径，"
            "文件存在且包含各模块文件路径引用"
        ),
        agent=orchestrator,
        output_file=str(WORKSPACE_DIR / "delivery_report.md"),
    )

    return orchestrator, main_task


# ─────────────────────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────────────────────

def run() -> Any:
    # 避免 CrewAI 首次运行后弹出「是否查看 execution traces」阻塞或打断自动化流程
    os.environ.setdefault("CREWAI_TESTING", "true")

    print("=" * 60)
    print("第23课·Orchestrator范式 演示")
    print(f"需求文档 : {REQUIREMENTS_FILE}")
    print(f"SOP Skill: {SKILL_PATH}")
    print("=" * 60)

    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

    if not REQUIREMENTS_FILE.exists():
        print(f"\n[错误] 需求文档不存在: {REQUIREMENTS_FILE}")
        print("请先创建 workspace/requirements.md")
        return None

    orchestrator, main_task = build_orchestrator()
    crew = Crew(
        agents=[orchestrator],
        tasks=[main_task],
        verbose=True,
    )
    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("✅ 完成。交付报告: workspace/delivery_report.md")
    print("=" * 60)
    return result


if __name__ == "__main__":
    run()
