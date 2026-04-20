#!/usr/bin/env python3
"""
第28课·数字员工的自我进化（v8）
tools/log_query.py — 统一日志查询 CLI

Agent 通过 bash 调用本脚本查询三层日志，支持以下子命令：
  stats       整体统计（任务数/均值/失败数/人类纠正数）
  tasks       任务列表（可排序、可筛选）
  steps       某任务的 ReAct 步骤回放
  l1          人类纠正记录搜索
  all-agents  全员统计

设计原则：
  - 纯数据查询，不做判断（Agent 自行决定查什么、怎么解读）
  - 输出 JSON，一条命令一个 JSON 对象
  - 是 log_ops.py 的 CLI wrapper（log_ops.py 保持为 Python 库供测试/回调使用）
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.log_ops import read_l2, read_l1, read_l3, read_l3_from_sessions


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent / "workspace"
DEFAULT_LOGS_DIR = WORKSPACE_ROOT / "shared" / "logs"
AGENT_IDS = ("pm", "manager")


def cmd_stats(args: argparse.Namespace) -> None:
    """整体统计：任务数/均值/失败数/人类纠正数"""
    logs_dir = Path(args.logs_dir)
    records = read_l2(logs_dir, args.agent_id, days=args.days)

    task_count = len(records)
    if task_count == 0:
        print(json.dumps({
            "agent_id": args.agent_id, "days": args.days,
            "task_count": 0, "avg_quality": 0.0,
            "failure_count": 0, "human_correction_count": 0,
        }))
        return

    qualities = [r.get("result_quality", 0.0) for r in records]
    avg_quality = sum(qualities) / len(qualities)
    failure_count = sum(1 for q in qualities if q < 0.5)

    l1_records = read_l1(logs_dir, days=args.days)
    human_correction_count = sum(
        1 for r in l1_records
        if r.get("type") in ("checkpoint_rejected", "retro_decision")
    )

    print(json.dumps({
        "agent_id": args.agent_id, "days": args.days,
        "task_count": task_count,
        "avg_quality": round(avg_quality, 3),
        "failure_count": failure_count,
        "human_correction_count": human_correction_count,
    }, ensure_ascii=False))


def cmd_tasks(args: argparse.Namespace) -> None:
    """任务列表（可排序、可筛选）"""
    logs_dir = Path(args.logs_dir)
    records = read_l2(logs_dir, args.agent_id, days=args.days)

    if args.sort == "quality_asc":
        records.sort(key=lambda r: r.get("result_quality", 1.0))
    elif args.sort == "quality_desc":
        records.sort(key=lambda r: r.get("result_quality", 0.0), reverse=True)
    elif args.sort == "time_desc":
        records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)

    if args.limit and args.limit > 0:
        records = records[:args.limit]

    tasks = [
        {
            "task_id": r.get("task_id", "unknown"),
            "task_desc": r.get("task_desc", "")[:120],
            "result_quality": r.get("result_quality", 0.0),
            "duration_sec": r.get("duration_sec", 0),
            "error_type": r.get("error_type"),
            "timestamp": r.get("timestamp", ""),
        }
        for r in records
    ]

    print(json.dumps({"agent_id": args.agent_id, "count": len(tasks), "tasks": tasks}, ensure_ascii=False))


def cmd_steps(args: argparse.Namespace) -> None:
    """某任务的 ReAct 步骤回放"""
    logs_dir = Path(args.logs_dir)
    sessions_dir = Path(args.sessions_dir) if args.sessions_dir else None

    steps = []
    if sessions_dir and sessions_dir.exists():
        steps = read_l3_from_sessions(
            sessions_dir, task_id=args.task_id, only_failed=args.only_failed
        )

    if not steps:
        steps = read_l3(logs_dir, agent_id=args.agent_id or "pm", task_id=args.task_id)
        if args.only_failed:
            steps = [s for s in steps if not s.get("converged", True)]

    print(json.dumps({"task_id": args.task_id, "step_count": len(steps), "steps": steps}, ensure_ascii=False))


def cmd_l1(args: argparse.Namespace) -> None:
    """人类纠正记录搜索"""
    logs_dir = Path(args.logs_dir)
    records = read_l1(logs_dir, days=args.days)

    if args.keyword:
        kw = args.keyword.lower()
        records = [
            r for r in records
            if kw in r.get("content", "").lower()
            or kw in r.get("subject", "").lower()
        ]

    results = [
        {
            "id": r.get("id", ""),
            "type": r.get("type", ""),
            "subject": r.get("subject", ""),
            "content": r.get("content", "")[:200],
            "timestamp": r.get("timestamp", ""),
        }
        for r in records
    ]

    print(json.dumps({"count": len(results), "records": results}, ensure_ascii=False))


def cmd_all_agents(args: argparse.Namespace) -> None:
    """全员统计"""
    logs_dir = Path(args.logs_dir)
    result = {}

    for agent_id in AGENT_IDS:
        records = read_l2(logs_dir, agent_id, days=args.days)
        qualities = [r.get("result_quality", 0.0) for r in records]
        result[agent_id] = {
            "task_count": len(records),
            "avg_quality": round(sum(qualities) / max(len(qualities), 1), 3),
            "failure_count": sum(1 for q in qualities if q < 0.5),
        }

    print(json.dumps(result, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="统一日志查询 CLI")
    parser.add_argument("--logs-dir", default=str(DEFAULT_LOGS_DIR))
    subparsers = parser.add_subparsers(dest="command", required=True)

    # stats
    p_stats = subparsers.add_parser("stats", help="整体统计")
    p_stats.add_argument("--agent-id", required=True)
    p_stats.add_argument("--days", type=int, default=7)

    # tasks
    p_tasks = subparsers.add_parser("tasks", help="任务列表")
    p_tasks.add_argument("--agent-id", required=True)
    p_tasks.add_argument("--days", type=int, default=7)
    p_tasks.add_argument("--sort", choices=["quality_asc", "quality_desc", "time_desc"], default=None)
    p_tasks.add_argument("--limit", type=int, default=None)

    # steps
    p_steps = subparsers.add_parser("steps", help="ReAct 步骤回放")
    p_steps.add_argument("--task-id", required=True)
    p_steps.add_argument("--agent-id", default=None)
    p_steps.add_argument("--sessions-dir", default=None)
    p_steps.add_argument("--only-failed", action="store_true")

    # l1
    p_l1 = subparsers.add_parser("l1", help="人类纠正记录")
    p_l1.add_argument("--days", type=int, default=7)
    p_l1.add_argument("--keyword", default=None)

    # all-agents
    p_all = subparsers.add_parser("all-agents", help="全员统计")
    p_all.add_argument("--days", type=int, default=7)

    args = parser.parse_args()

    handlers = {
        "stats": cmd_stats,
        "tasks": cmd_tasks,
        "steps": cmd_steps,
        "l1": cmd_l1,
        "all-agents": cmd_all_agents,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
