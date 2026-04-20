"""
第28课·数字员工的自我进化（v8）
schemas.py — 日志记录、复盘报告与改进提案的 Pydantic 数据模型

v8 变更（重构）：
  - 删除 ProposalPatch / ValidationCheck（精确 patch 由 Agent 直接写 before/after_text）
  - 新增 RetroFinding / RetroReport / ImprovementProposal（对齐 SKILL.md 输出格式）
  - 删除 RetroProposal（被 RetroOutput 替代）
  - root_cause 枚举更新：sop_gap / prompt_ambiguity / ability_gap / integration_issue
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator


# ─────────────────────────────────────────────────────────────────────────────
# L2 日志记录（任务-Agent 层）— 保持不变
# ─────────────────────────────────────────────────────────────────────────────

class L2LogRecord(BaseModel):
    agent_id:       str
    task_id:        str
    task_desc:      str
    result_quality: float
    duration_sec:   float
    error_type:     str | None = None
    timestamp:      str

    @field_validator("result_quality")
    @classmethod
    def quality_in_range(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"result_quality 必须在 0.0–1.0 之间，当前值：{v}")
        return v

    @field_validator("timestamp")
    @classmethod
    def valid_iso_timestamp(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
        except ValueError as exc:
            raise ValueError(f"timestamp 格式不合法（需要 ISO 8601），当前值：{v!r}") from exc
        return v


# ─────────────────────────────────────────────────────────────────────────────
# 复盘报告（v8 新增）
# ─────────────────────────────────────────────────────────────────────────────

class RetroFinding(BaseModel):
    """复盘发现：一个模式 + 支撑证据"""
    pattern:            str
    evidence_task_ids:  list[str]
    l1_corroboration:   str = ""

    @field_validator("evidence_task_ids")
    @classmethod
    def has_evidence(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("evidence_task_ids 至少需要 1 条 task_id")
        return v


class RetroReport(BaseModel):
    """复盘报告头部"""
    agent_id: str
    period:   str
    summary:  str
    findings: list[RetroFinding]

    @field_validator("findings")
    @classmethod
    def has_findings(cls, v: list[RetroFinding]) -> list[RetroFinding]:
        if not v:
            raise ValueError("findings 不允许为空")
        return v


# ─────────────────────────────────────────────────────────────────────────────
# 改进提案（v8 新增）
# ─────────────────────────────────────────────────────────────────────────────

class ImprovementProposal(BaseModel):
    """单条改进提案：Agent 产出，Manager 审批，Agent 执行"""
    root_cause:           Literal["sop_gap", "prompt_ambiguity", "ability_gap", "integration_issue"]
    target_file:          str
    current_behavior:     str
    proposed_change:      str
    before_text:          str
    after_text:           str
    expected_improvement: str
    evidence:             list[str]

    @field_validator("target_file")
    @classmethod
    def target_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("target_file 不允许为空")
        return v

    @field_validator("evidence")
    @classmethod
    def has_evidence(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("evidence 至少需要 1 条日志 ID")
        return v

    @field_validator("before_text", "after_text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("before_text 和 after_text 不允许为空")
        return v


# ─────────────────────────────────────────────────────────────────────────────
# 完整复盘产出（报告 + 提案列表）
# ─────────────────────────────────────────────────────────────────────────────

class RetroOutput(BaseModel):
    """Agent 复盘的完整产出，对应 SKILL.md 要求的输出 JSON"""
    retrospective_report:   RetroReport
    improvement_proposals:  list[ImprovementProposal]

    @field_validator("improvement_proposals")
    @classmethod
    def max_proposals(cls, v: list[ImprovementProposal]) -> list[ImprovementProposal]:
        if len(v) > 3:
            raise ValueError("一次复盘最多 3 条提案，请聚焦最重要的改进")
        return v
