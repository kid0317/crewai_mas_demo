"""
第28课·数字员工的自我进化（v6）
seed_logs.py — 预置演示用历史日志

教学说明：
  本文件预置"团队已运行一周"的模拟日志数据，用于演示自我复盘和团队复盘功能。
  模拟场景：PM Agent 在设计文档任务上多次被 checkpoint 退回，质量分偏低。

  预置数据包含：
    - L2 日志：PM Agent 8条任务记录（3条低质量），Manager 3条任务记录
    - L3 日志（旧格式）：保留 l3_react/ 目录的步骤文件（兼容）
    - L3 日志（v6 格式）：写入 sessions/*_raw.jsonl + index.jsonl
    - L1 日志：3条 checkpoint_rejected 记录（人类退回产品设计文档）

  接受 base_dir 参数，测试时可传 tmp_path 避免污染真实工作区。
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from filelock import FileLock
from tools.log_ops import write_l2, write_l3


def seed_logs(base_dir: Path | None = None) -> None:
    """
    写入预置演示日志（基于当前时刻生成，每次运行前清空旧数据）。

    Args:
        base_dir: workspace 根目录。默认为本文件所在目录的 workspace/
    """
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent / "workspace"

    logs_dir = base_dir / "shared" / "logs"
    # 清空旧日志，确保每次运行都基于当前时刻重新生成
    if logs_dir.exists():
        shutil.rmtree(logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # 清空旧 session 数据
    pm_sessions_dir = base_dir / "pm" / "sessions"
    if pm_sessions_dir.exists():
        shutil.rmtree(pm_sessions_dir)
    pm_sessions_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)

    # ── L2 日志：PM Agent（8条，3条低质量——模拟真实运行一周）─────────────────
    pm_tasks = [
        # 任务ID, 描述, 质量分, 耗时, 错误类型, 偏移天数
        ("t001", "用户登录功能产品设计文档",      0.40, 180, "checkpoint_rejected", 6),
        ("t002", "用户注册流程产品设计文档",      0.85, 120, None, 5),
        ("t003", "产品设计文档v2（用户登录）",    0.42, 200, "checkpoint_rejected", 5),
        ("t004", "支付流程产品规格说明",          0.90, 150, None, 4),
        ("t005", "数据看板产品设计文档",          0.88, 130, None, 3),
        ("t006", "用户注册设计迭代（移动端）",    0.38, 220, "checkpoint_rejected", 2),
        ("t007", "搜索功能产品需求文档",          0.82, 110, None, 2),
        ("t008", "消息通知产品设计文档",          0.79, 140, None, 1),
    ]

    for task_id, task_desc, quality, duration, error, days_ago in pm_tasks:
        ts = now - timedelta(days=days_ago)
        write_l2(
            logs_dir = logs_dir,
            agent_id = "pm",
            task_id  = task_id,
            record   = {
                "agent_id":       "pm",
                "task_id":        task_id,
                "task_desc":      task_desc,
                "result_quality": quality,
                "duration_sec":   duration,
                "error_type":     error,
                "timestamp":      ts.isoformat(),
            },
        )

    print(f"[SEED] PM L2 日志已写入：{len(pm_tasks)} 条")

    # ── L2 日志：Manager（3条，质量正常）────────────────────────────────────
    manager_tasks = [
        ("m001", "需求澄清：用户注册功能",  0.92, 90,  None, 6),
        ("m002", "任务分配：产品设计文档",  0.88, 60,  None, 5),
        ("m003", "验收：用户注册产品文档",  0.85, 75,  None, 4),
    ]

    for task_id, task_desc, quality, duration, error, days_ago in manager_tasks:
        ts = now - timedelta(days=days_ago)
        write_l2(
            logs_dir = logs_dir,
            agent_id = "manager",
            task_id  = task_id,
            record   = {
                "agent_id":       "manager",
                "task_id":        task_id,
                "task_desc":      task_desc,
                "result_quality": quality,
                "duration_sec":   duration,
                "error_type":     error,
                "timestamp":      ts.isoformat(),
            },
        )

    print(f"[SEED] Manager L2 日志已写入：{len(manager_tasks)} 条")

    # ── L3 日志：PM 3条低质量任务的 ReAct 步骤（展示失败节点）────────────────
    # t001 失败原因：没有考虑移动端适配
    _write_l3_steps(logs_dir, "pm", "t001", now - timedelta(days=6), [
        (0, "读取需求文档，了解登录功能要求", "read_requirements", "已读取，要求：邮箱登录+密码",        True),
        (1, "开始撰写产品规格文档",          "write_document",    "已写入基本结构",                    True),
        (2, "文档完成，发送完成通知",        "send_mail",         "已发送 task_done 给 manager",       True),
    ])

    # t003 失败原因：交互细节不足（表单验证逻辑缺失）
    _write_l3_steps(logs_dir, "pm", "t003", now - timedelta(days=5), [
        (0, "读取需求文档和前一版设计文档",          "read_requirements", "已读取",               True),
        (1, "撰写v2文档，修改登录页面描述",          "write_document",    "已更新产品文档",        True),
        (2, "检查是否覆盖所有需求点",               "read_document",     "发现缺少错误状态处理",  False),
        (3, "补充错误处理，但未完整覆盖",            "write_document",    "部分补充",              True),
        (4, "发送完成通知",                         "send_mail",         "已发送 task_done",      True),
    ])

    # t006 失败原因：没有多端适配检查（桌面端/移动端）
    _write_l3_steps(logs_dir, "pm", "t006", now - timedelta(days=2), [
        (0, "读取需求文档",                          "read_requirements", "需求：注册流程+移动端优先", True),
        (1, "撰写产品设计文档（桌面端视角）",         "write_document",    "已完成桌面端设计",          True),
        (2, "完成，发通知",                           "send_mail",         "已发送",                    True),
    ])

    print(f"[SEED] PM L3 日志已写入：3个失败任务（t001/t003/t006）")

    # ── L3（v6）：写入 session 格式（sessions/index.jsonl + *_raw.jsonl）─────
    pm_sessions_dir = base_dir / "pm" / "sessions"
    pm_sessions_dir.mkdir(parents=True, exist_ok=True)

    _write_session_l3(
        sessions_dir=pm_sessions_dir,
        session_id="demo_m4l28",
        agent_id="pm",
        task_entries=[
            ("t001", now - timedelta(days=6), [
                {"role": "assistant", "content": "读取需求文档，了解登录功能要求"},
                {"role": "tool", "content": "已读取，要求：邮箱登录+密码"},
                {"role": "assistant", "content": "开始撰写产品规格文档"},
                {"role": "tool", "content": "已写入基本结构"},
                {"role": "assistant", "content": "文档完成，发送完成通知"},
                {"role": "tool", "content": "已发送 task_done 给 manager"},
            ]),
            ("t003", now - timedelta(days=5), [
                {"role": "assistant", "content": "读取需求文档和前一版设计文档"},
                {"role": "tool", "content": "已读取"},
                {"role": "assistant", "content": "撰写v2文档，修改登录页面描述"},
                {"role": "tool", "content": "已更新产品文档"},
                {"role": "assistant", "content": "检查是否覆盖所有需求点"},
                {"role": "tool", "content": "Error: 发现缺少错误状态处理，表单验证逻辑缺失"},
                {"role": "assistant", "content": "补充错误处理，但未完整覆盖"},
                {"role": "tool", "content": "部分补充"},
            ]),
            ("t006", now - timedelta(days=2), [
                {"role": "assistant", "content": "读取需求文档"},
                {"role": "tool", "content": "需求：注册流程+移动端优先"},
                {"role": "assistant", "content": "撰写产品设计文档（桌面端视角）"},
                {"role": "tool", "content": "已完成桌面端设计"},
                {"role": "assistant", "content": "Fail: 未考虑移动端适配，直接提交"},
                {"role": "tool", "content": "已发送"},
            ]),
        ],
    )
    print("[SEED] PM session L3 日志已写入（v6 格式：sessions/index.jsonl）")

    # ── L1 日志：3条人类纠正记录（直接写文件，模拟来自 mailbox_ops 的记录）───
    # 注意：seed_logs 绕过 send_mail() 是有意为之——这里预置的是模拟的历史数据，
    # 而不是真实的 send_mail 调用。真实运行时 L1 由 mailbox_ops.send_mail 自动写入。
    l1_dir = logs_dir / "l1_human"
    l1_dir.mkdir(parents=True, exist_ok=True)

    l1_entries = [
        ("l1_001", "checkpoint_rejected", "设计文档退回：t001", "缺少移动端适配方案，请重新设计",     5),
        ("l1_002", "checkpoint_rejected", "设计文档退回：t003", "交互细节不足，表单验证逻辑缺失",     4),
        ("l1_003", "checkpoint_rejected", "设计文档退回：t006", "未考虑桌面端/移动端差异，需补充多端设计", 1),
    ]

    for msg_id, type_, subject, content, days_ago in l1_entries:
        ts = now - timedelta(days=days_ago)
        rec = {
            "id":        msg_id,
            "from":      "manager",
            "to":        "human",
            "type":      type_,
            "subject":   subject,
            "content":   content,
            "timestamp": ts.isoformat(),
            "read":      True,
        }
        file_path = l1_dir / f"{msg_id}.json"
        lock_path = file_path.with_suffix(".lock")
        with FileLock(str(lock_path)):
            file_path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[SEED] L1 人类纠正日志已写入：{len(l1_entries)} 条")

    # ── 重置 PM 工作区文件（确保演示可重复运行）────────────────────────────────
    _reset_workspace_files(base_dir)

    print(f"[SEED] 完成！日志目录：{logs_dir}")


def _write_l3_steps(
    logs_dir:  Path,
    agent_id:  str,
    task_id:   str,
    base_time: datetime,
    steps: list[tuple[int, str, str, str, bool]],
) -> None:
    """辅助函数：批量写入 L3 步骤日志。"""
    for i, (step_idx, thought, action, observation, converged) in enumerate(steps):
        ts = base_time + timedelta(minutes=i * 5)
        write_l3(
            logs_dir  = logs_dir,
            agent_id  = agent_id,
            task_id   = task_id,
            step_idx  = step_idx,
            record    = {
                "agent_id":    agent_id,
                "task_id":     task_id,
                "step_idx":    step_idx,
                "thought":     thought,
                "action":      action,
                "observation": observation,
                "converged":   converged,
                "timestamp":   ts.isoformat(),
            },
        )


def _write_session_l3(
    sessions_dir: Path,
    session_id: str,
    agent_id: str,
    task_entries: list[tuple[str, datetime, list[dict]]],
) -> None:
    """v6：将模拟 L3 数据写入 sessions/*_raw.jsonl + index.jsonl。"""
    raw_file = sessions_dir / f"{session_id}_raw.jsonl"
    idx_file = sessions_dir / "index.jsonl"

    line_num = 0
    if raw_file.exists():
        line_num = len(raw_file.read_text(encoding="utf-8").splitlines())

    with open(raw_file, "a", encoding="utf-8") as f:
        with open(idx_file, "a", encoding="utf-8") as idx:
            for task_id, base_time, messages in task_entries:
                start_line = line_num
                for i, msg in enumerate(messages):
                    ts = base_time + timedelta(minutes=i * 2)
                    record = {**msg, "ts": ts.isoformat()}
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    line_num += 1
                end_line = line_num

                end_time = base_time + timedelta(minutes=len(messages) * 2)
                idx_entry = {
                    "session_id": session_id,
                    "task_id": task_id,
                    "agent_id": agent_id,
                    "start_ts": base_time.isoformat(),
                    "end_ts": end_time.isoformat(),
                    "start_line": start_line,
                    "end_line": end_line,
                }
                idx.write(json.dumps(idx_entry, ensure_ascii=False) + "\n")


def _reset_workspace_files(base_dir: Path) -> None:
    """重置复盘演示会修改的 PM 文件到 baseline 状态。

    复盘流程会通过 before_text → after_text 修改 PM 的配置文件。
    每次重跑演示前，需要恢复这些文件到初始状态。
    """
    baselines_dir = Path(__file__).resolve().parent / "baselines"

    file_map = {
        "pm_agent.md":                base_dir / "pm" / "agent.md",
        "pm_soul.md":                 base_dir / "pm" / "soul.md",
        "pm_memory.md":               base_dir / "pm" / "memory.md",
        "pm_product_design_skill.md": base_dir / "pm" / "skills" / "product_design" / "SKILL.md",
    }

    for baseline_name, target_path in file_map.items():
        src = baselines_dir / baseline_name
        if not src.exists():
            print(f"[WARN] baseline 文件不存在，跳过：{src}")
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"[SEED] PM 工作区文件已重置到 baseline（{len(file_map)} 个文件）")


if __name__ == "__main__":
    seed_logs()
    print("预置日志完成。")
