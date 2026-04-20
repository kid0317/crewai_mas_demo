"""
第28课·数字员工的自我进化（v8）
test_m4l28_v8.py — 端到端验证测试

测试矩阵：
  T1  seed_logs 生成日志，log_query stats 能查到
  T2  log_query tasks --sort quality_asc 返回排序结果
  T3  log_query steps 返回 ReAct 步骤
  T4  log_query l1 返回人类纠正记录
  T5  log_query l1 --keyword 过滤
  T6  log_query all-agents 返回全员统计
  T7  L2LogRecord result_quality 范围校验
  T8  ImprovementProposal evidence=[] → ValidationError
  T9  ImprovementProposal before_text="" → ValidationError
  T10 RetroOutput max 3 proposals
  T11 RetroReport findings 非空校验
  T12 seed_logs 重复运行不会叠加（清空后重建）
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from schemas import (
    L2LogRecord,
    RetroFinding,
    RetroReport,
    ImprovementProposal,
    RetroOutput,
)
from seed_logs import seed_logs

M4L28_DIR = Path(__file__).resolve().parent
LOG_QUERY = str(M4L28_DIR / "tools" / "log_query.py")


@pytest.fixture(scope="module")
def workspace(tmp_path_factory):
    """Create workspace with seed data."""
    base = tmp_path_factory.mktemp("workspace")
    # Create necessary structure
    (base / "shared" / "logs").mkdir(parents=True)
    (base / "shared" / "mailboxes").mkdir(parents=True)
    (base / "shared" / "proposals").mkdir(parents=True)
    (base / "pm" / "sessions").mkdir(parents=True)
    seed_logs(base)
    return base


def run_query(workspace, *args) -> dict:
    """Run log_query.py with given args, return parsed JSON."""
    cmd = [
        sys.executable, LOG_QUERY,
        "--logs-dir", str(workspace / "shared" / "logs"),
        *args,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(M4L28_DIR))
    assert result.returncode == 0, f"log_query failed: {result.stderr}"
    return json.loads(result.stdout)


# ─── T1: stats ───────────────────────────────────────────────────────────────

def test_stats_pm(workspace):
    data = run_query(workspace, "stats", "--agent-id", "pm", "--days", "7")
    assert data["task_count"] == 8
    assert 0.6 < data["avg_quality"] < 0.8
    assert data["failure_count"] == 3
    assert data["human_correction_count"] == 3


def test_stats_manager(workspace):
    data = run_query(workspace, "stats", "--agent-id", "manager", "--days", "7")
    assert data["task_count"] == 3
    assert data["avg_quality"] > 0.8
    assert data["failure_count"] == 0


# ─── T2: tasks sorted ─────────────────────��──────────────────────────────────

def test_tasks_quality_asc(workspace):
    data = run_query(workspace, "tasks", "--agent-id", "pm", "--days", "7",
                     "--sort", "quality_asc", "--limit", "3")
    tasks = data["tasks"]
    assert len(tasks) == 3
    assert tasks[0]["result_quality"] <= tasks[1]["result_quality"] <= tasks[2]["result_quality"]
    assert tasks[0]["result_quality"] < 0.5


# ─── T3: steps ───────────────────────���────────────────────────────��──────────

def test_steps_t001(workspace):
    cmd = [
        sys.executable, LOG_QUERY,
        "--logs-dir", str(workspace / "shared" / "logs"),
        "steps", "--task-id", "t001", "--agent-id", "pm",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(M4L28_DIR))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["task_id"] == "t001"
    assert data["step_count"] == 3


def test_steps_sessions(workspace):
    cmd = [
        sys.executable, LOG_QUERY,
        "--logs-dir", str(workspace / "shared" / "logs"),
        "steps", "--task-id", "t001",
        "--sessions-dir", str(workspace / "pm" / "sessions"),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(M4L28_DIR))
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["step_count"] >= 3


# ─── T4: l1 ──────────────────────���─────────────────────────���─────────────────

def test_l1_all(workspace):
    data = run_query(workspace, "l1", "--days", "7")
    assert data["count"] == 3
    assert all(r["type"] == "checkpoint_rejected" for r in data["records"])


# ─── T5: l1 keyword ──────────────────────────────────────────────────────────

def test_l1_keyword(workspace):
    data = run_query(workspace, "l1", "--days", "7", "--keyword", "移动端")
    assert data["count"] >= 1
    assert "移动端" in data["records"][0]["content"] or "移动端" in data["records"][0]["subject"]


# ─── T6: all-agents ────────────────────────────��─────────────────────────────

def test_all_agents(workspace):
    data = run_query(workspace, "all-agents", "--days", "7")
    assert "pm" in data
    assert "manager" in data
    assert data["pm"]["task_count"] == 8
    assert data["manager"]["task_count"] == 3


# ─── T7: L2LogRecord validation ──────────────────────────────────────────────

def test_l2_quality_range():
    with pytest.raises(Exception):
        L2LogRecord(
            agent_id="pm", task_id="x", task_desc="test",
            result_quality=1.5, duration_sec=10,
            timestamp="2026-04-13T00:00:00+00:00",
        )


# ─── T8: ImprovementProposal evidence empty ──────────────────────────────────

def test_proposal_evidence_empty():
    with pytest.raises(Exception):
        ImprovementProposal(
            root_cause="sop_gap",
            target_file="agent.md",
            current_behavior="x",
            proposed_change="y",
            before_text="a",
            after_text="b",
            expected_improvement="z",
            evidence=[],
        )


# ─── T9: ImprovementProposal before_text empty ──────────────────���────────────

def test_proposal_before_text_empty():
    with pytest.raises(Exception):
        ImprovementProposal(
            root_cause="sop_gap",
            target_file="agent.md",
            current_behavior="x",
            proposed_change="y",
            before_text="",
            after_text="b",
            expected_improvement="z",
            evidence=["t001"],
        )


# ─── T10: RetroOutput max 3 proposals ────────────────────────────────────────

def test_retro_output_max_proposals():
    proposal = ImprovementProposal(
        root_cause="sop_gap",
        target_file="agent.md",
        current_behavior="x",
        proposed_change="y",
        before_text="before",
        after_text="after",
        expected_improvement="z",
        evidence=["t001"],
    )
    report = RetroReport(
        agent_id="pm",
        period="2026-04-07 ~ 2026-04-13",
        summary="test",
        findings=[RetroFinding(pattern="p", evidence_task_ids=["t001"])],
    )
    with pytest.raises(Exception):
        RetroOutput(
            retrospective_report=report,
            improvement_proposals=[proposal] * 4,
        )


# ─── T11: RetroReport findings non-empty ────────────���─────────────────────��──

def test_retro_report_findings_required():
    with pytest.raises(Exception):
        RetroReport(
            agent_id="pm",
            period="2026-04-07 ~ 2026-04-13",
            summary="test",
            findings=[],
        )


# ─── T12: seed_logs idempotent ──────────────────────���─────────────────────────

def test_seed_logs_idempotent(tmp_path):
    base = tmp_path / "ws"
    base.mkdir()
    (base / "shared" / "logs").mkdir(parents=True)
    (base / "pm" / "sessions").mkdir(parents=True)

    seed_logs(base)
    seed_logs(base)  # run again

    l2_dir = base / "shared" / "logs" / "l2_task"
    pm_files = list(l2_dir.glob("pm_*.json"))
    assert len(pm_files) == 8  # not 16
