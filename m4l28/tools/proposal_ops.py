"""
第28课·数字员工的自我进化（v8）
tools/proposal_ops.py — 提案读写操作

v8 简化：
  - Agent 直接写 JSON 文件（RetroOutput 格式）
  - 本模块提供读取和校验功能
  - memory 自动批准的闸门逻辑（3条/天）
"""

from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

from schemas import RetroOutput, ImprovementProposal

logger = logging.getLogger(__name__)

MEMORY_DAILY_LIMIT_PER_AGENT = 3


def read_retro_output(file_path: Path) -> RetroOutput | None:
    """读取 Agent 产出的复盘 JSON，校验格式。"""
    if not file_path.exists():
        return None
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        return RetroOutput(**data)
    except Exception as exc:
        logger.warning("read_retro_output: 解析失败 %s: %s", file_path, exc)
        return None


def list_retro_files(proposals_dir: Path) -> list[Path]:
    """列出 proposals 目录下所有 JSON 文件���"""
    if not proposals_dir.exists():
        return []
    return sorted(proposals_dir.glob("*.json"))


def classify_proposal_tier(proposal: ImprovementProposal) -> int:
    """按 target_file 分档：1=memory, 2=skill/agent, 3=soul"""
    target = proposal.target_file.lower()
    if "soul" in target:
        return 3
    if "memory" in target:
        return 1
    return 2


def can_auto_approve_memory(
    proposals_dir: Path,
    agent_id: str,
) -> tuple[bool, str]:
    """检查今日 memory 自动批准是否超过闸门（3条/天）。"""
    today = date.today().isoformat()
    approved_today = 0

    approved_dir = proposals_dir / "approved"
    if approved_dir.exists():
        for f in approved_dir.glob(f"{agent_id}_*_{today}*.json"):
            approved_today += 1

    if approved_today >= MEMORY_DAILY_LIMIT_PER_AGENT:
        return False, f"{agent_id} 今日 memory 自动批准已满 {approved_today} 条"
    return True, "可自动批准"
