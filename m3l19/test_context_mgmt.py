"""
第19课 单元测试：上下文生命周期管理

测试覆盖：
  - build_bootstrap_prompt：加载 workspace 4 个 md 文件
  - prune_tool_results：清空 10 轮之前的 tool 消息内容
  - chunk_by_tokens：按 token 大小切分消息列表
  - load/save/append session：session 持久化
  - maybe_compress：超阈值时触发压缩

运行：
  cd m3l19 && pytest test_context_mgmt.py -v
"""

import json
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# 支持两种运行方式：
#   cd m3l19 && pytest test_context_mgmt.py        （从 m3l19 目录内）
#   cd 项目根 && pytest m3l19/test_context_mgmt.py  （从项目根）
_HERE = Path(__file__).parent
_PROJECT_ROOT = _HERE.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_HERE))

from m3l19_context_mgmt import (  # noqa: E402
    build_bootstrap_prompt,
    prune_tool_results,
    chunk_by_tokens,
    load_session_ctx,
    save_session_ctx,
    append_session_raw,
    maybe_compress,
    PRUNE_KEEP_TURNS,
    COMPRESS_THRESHOLD,
    CHUNK_TOKENS,
    FRESH_KEEP_TURNS,
)

_MODULE = "m3l19_context_mgmt"


# ─────────────────────────────────────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────────────────────────────────────

def _make_turn(turn_idx: int, tool_content: str = "tool result") -> list[dict]:
    """生成一轮对话：user → assistant → tool"""
    return [
        {"role": "user",      "content": f"用户消息 {turn_idx}"},
        {"role": "assistant", "content": f"助手回复 {turn_idx}", "tool_call_id": f"tc_{turn_idx}"},
        {"role": "tool",      "content": tool_content,           "tool_call_id": f"tc_{turn_idx}"},
    ]


def _make_messages(n_turns: int, tool_content: str = "tool result") -> list[dict]:
    """生成 n 轮对话的 message list（不含 system）"""
    msgs = []
    for i in range(n_turns):
        msgs.extend(_make_turn(i, tool_content))
    return msgs


# ─────────────────────────────────────────────────────────────────────────────
# 1. build_bootstrap_prompt
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildBootstrapPrompt:

    def test_loads_all_four_files(self, tmp_path):
        """4 个 md 文件都存在时，prompt 包含全部 4 个 XML 标签"""
        (tmp_path / "soul.md").write_text("soul content", encoding="utf-8")
        (tmp_path / "user.md").write_text("user content", encoding="utf-8")
        (tmp_path / "agent.md").write_text("agent content", encoding="utf-8")
        (tmp_path / "memory.md").write_text("memory content", encoding="utf-8")

        prompt = build_bootstrap_prompt(tmp_path)

        assert "<soul>" in prompt and "soul content" in prompt
        assert "<user_profile>" in prompt and "user content" in prompt
        assert "<agent_rules>" in prompt and "agent content" in prompt
        assert "<memory_index>" in prompt and "memory content" in prompt

    def test_missing_files_are_skipped(self, tmp_path):
        """只有 soul.md 时，其他标签不出现"""
        (tmp_path / "soul.md").write_text("soul only", encoding="utf-8")

        prompt = build_bootstrap_prompt(tmp_path)

        assert "<soul>" in prompt
        assert "<user_profile>" not in prompt
        assert "<agent_rules>" not in prompt
        assert "<memory_index>" not in prompt

    def test_empty_workspace_returns_empty_string(self, tmp_path):
        """workspace 为空时返回空字符串"""
        prompt = build_bootstrap_prompt(tmp_path)
        assert prompt == ""

    def test_memory_truncated_at_200_lines(self, tmp_path):
        """memory.md 超过 200 行时只取前 200 行"""
        lines = [f"line {i}" for i in range(300)]
        (tmp_path / "memory.md").write_text("\n".join(lines), encoding="utf-8")

        prompt = build_bootstrap_prompt(tmp_path)

        assert "line 199" in prompt
        assert "line 200" not in prompt


# ─────────────────────────────────────────────────────────────────────────────
# 2. prune_tool_results
# ─────────────────────────────────────────────────────────────────────────────

class TestPruneToolResults:

    def test_old_tool_results_are_cleared(self):
        """10 轮之前的 tool 消息内容应被替换为 [已剪枝]"""
        msgs = _make_messages(15)  # 15 轮，keep_turns=10 → 前 5 轮被剪枝

        prune_tool_results(msgs, keep_turns=10)

        # 每轮 3 条消息（user + assistant + tool），前 5 轮 = 前 15 条消息
        msgs_per_turn = 3
        pruned_turns = 15 - 10
        old_tool_msgs = [m for m in msgs[:pruned_turns * msgs_per_turn] if m["role"] == "tool"]
        assert len(old_tool_msgs) == pruned_turns
        for m in old_tool_msgs:
            assert m["content"] == "[已剪枝]"

    def test_recent_tool_results_are_kept(self):
        """最近 10 轮的 tool 消息内容不变"""
        msgs = _make_messages(15)

        prune_tool_results(msgs, keep_turns=10)

        recent_tool_msgs = [m for m in msgs[15:] if m["role"] == "tool"]
        assert len(recent_tool_msgs) == 10
        for m in recent_tool_msgs:
            assert m["content"] == "tool result"

    def test_fewer_than_keep_turns_nothing_pruned(self):
        """消息轮数 ≤ keep_turns 时，不剪枝任何内容"""
        msgs = _make_messages(8)

        prune_tool_results(msgs, keep_turns=10)

        for m in msgs:
            if m["role"] == "tool":
                assert m["content"] == "tool result"

    def test_non_tool_messages_untouched(self):
        """user / assistant 消息内容不受剪枝影响"""
        msgs = _make_messages(15)
        original_user_contents = [m["content"] for m in msgs if m["role"] == "user"]

        prune_tool_results(msgs, keep_turns=10)

        user_contents = [m["content"] for m in msgs if m["role"] == "user"]
        assert user_contents == original_user_contents

    def test_tool_call_id_preserved_after_prune(self):
        """剪枝后 tool 消息的 tool_call_id 字段保留"""
        msgs = _make_messages(15)

        prune_tool_results(msgs, keep_turns=10)

        old_tool_msgs = [m for m in msgs[:15] if m["role"] == "tool"]
        for i, m in enumerate(old_tool_msgs):
            assert m["tool_call_id"] == f"tc_{i}"

    def test_uses_default_keep_turns_constant(self):
        """不传 keep_turns 时使用模块常量 PRUNE_KEEP_TURNS"""
        extra_turns  = 5
        total_turns  = PRUNE_KEEP_TURNS + extra_turns
        msgs_per_turn = 3  # user + assistant + tool
        msgs = _make_messages(total_turns)

        prune_tool_results(msgs)  # 不传参数

        # 前 extra_turns 轮的 tool 消息应被剪枝
        old_tool_msgs = [m for m in msgs[:extra_turns * msgs_per_turn] if m["role"] == "tool"]
        pruned = [m for m in old_tool_msgs if m["content"] == "[已剪枝]"]
        assert len(pruned) == extra_turns


# ─────────────────────────────────────────────────────────────────────────────
# 3. chunk_by_tokens
# ─────────────────────────────────────────────────────────────────────────────

class TestChunkByTokens:

    def test_splits_into_correct_number_of_chunks(self):
        """4 条各 500 token 的消息，chunk_tokens=1000 → 2 个 chunk"""
        msgs = [{"role": "user", "content": "x" * 1000} for _ in range(4)]
        # 每条 ~500 token（//2），chunk_tokens=1000 → 每 chunk 2 条

        chunks = chunk_by_tokens(msgs, chunk_tokens=1000)

        assert len(chunks) == 2
        assert len(chunks[0]) == 2
        assert len(chunks[1]) == 2

    def test_single_oversized_message_forms_own_chunk(self):
        """单条消息超过 chunk_tokens 时，独立成一个 chunk"""
        msgs = [{"role": "user", "content": "x" * 4000}]  # ~2000 token

        chunks = chunk_by_tokens(msgs, chunk_tokens=1000)

        assert len(chunks) == 1
        assert chunks[0] == msgs

    def test_empty_messages_returns_empty(self):
        """空列表返回空列表"""
        assert chunk_by_tokens([], chunk_tokens=1000) == []

    def test_all_messages_fit_in_one_chunk(self):
        """所有消息 token 总量 < chunk_tokens 时，只有 1 个 chunk"""
        msgs = [{"role": "user", "content": "短消息"} for _ in range(5)]

        chunks = chunk_by_tokens(msgs, chunk_tokens=10000)

        assert len(chunks) == 1
        assert len(chunks[0]) == 5


# ─────────────────────────────────────────────────────────────────────────────
# 4. session 持久化
# ─────────────────────────────────────────────────────────────────────────────

class TestSessionPersistence:

    def test_save_and_load_roundtrip(self, tmp_path):
        """save 后 load 能还原相同的 messages"""
        msgs = [{"role": "user", "content": "hello"}, {"role": "assistant", "content": "hi"}]

        save_session_ctx("test_session", msgs, sessions_dir=tmp_path)
        loaded = load_session_ctx("test_session", sessions_dir=tmp_path)

        assert loaded == msgs

    def test_load_nonexistent_returns_empty(self, tmp_path):
        """session 不存在时返回空列表"""
        result = load_session_ctx("no_such_session", sessions_dir=tmp_path)
        assert result == []

    def test_append_raw_creates_jsonl(self, tmp_path):
        """append_session_raw 创建 .jsonl 文件，每行是合法 JSON"""
        append_session_raw("s1", [
            {"role": "user",      "content": "消息1"},
            {"role": "assistant", "content": "回复1"},
        ], sessions_dir=tmp_path)

        raw_file = tmp_path / "s1_raw.jsonl"
        assert raw_file.exists()

        lines = raw_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        record = json.loads(lines[0])
        assert record["role"] == "user"
        assert record["content"] == "消息1"
        assert "ts" in record

    def test_append_raw_is_append_only(self, tmp_path):
        """多次 append 不覆盖，累积追加"""
        for i in range(5):
            append_session_raw("s2", [{"role": "user", "content": f"msg{i}"}], sessions_dir=tmp_path)

        lines = (tmp_path / "s2_raw.jsonl").read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 5

    def test_save_creates_parent_dir(self, tmp_path):
        """sessions_dir 不存在时自动创建"""
        new_dir = tmp_path / "new" / "sessions"
        save_session_ctx("s3", [{"role": "user", "content": "x"}], sessions_dir=new_dir)
        assert (new_dir / "s3_ctx.json").exists()


# ─────────────────────────────────────────────────────────────────────────────
# 5. maybe_compress
# ─────────────────────────────────────────────────────────────────────────────

class TestMaybeCompress:

    def _make_large_messages(self, n_turns: int, content_size: int = 500) -> list[dict]:
        """生成内容较大的消息，用于触发压缩阈值"""
        return _make_messages(n_turns, tool_content="x" * content_size)

    def test_no_compress_below_threshold(self):
        """token 使用率低于阈值时，messages 不变"""
        msgs = [{"role": "user", "content": "短消息"}]
        original = list(msgs)

        mock_ctx = MagicMock()
        mock_ctx.llm = MagicMock()
        mock_ctx.llm.context_window_size = 1_000_000  # 极大 context window

        maybe_compress(msgs, mock_ctx)

        assert msgs == original

    def test_compress_triggered_above_threshold(self):
        """token 使用率超过 COMPRESS_THRESHOLD 时，旧消息被替换为摘要"""
        # 构造足够大的消息列表触发压缩
        msgs = [{"role": "system", "content": "系统提示"}]
        msgs += self._make_large_messages(20, content_size=2000)

        mock_ctx = MagicMock()
        mock_ctx.llm = MagicMock()
        mock_ctx.llm.context_window_size = 1000  # 极小 context window，必然触发

        with patch(f"{_MODULE}._summarize_chunk", return_value="摘要内容") as mock_sum:
            maybe_compress(msgs, mock_ctx)
            assert mock_sum.called

        # 压缩后消息数应减少
        assert len(msgs) < 20 * 3 + 1

    def test_system_messages_preserved_after_compress(self):
        """压缩后 system 消息保留"""
        msgs = [{"role": "system", "content": "系统提示"}]
        msgs += self._make_large_messages(20, content_size=2000)

        mock_ctx = MagicMock()
        mock_ctx.llm = MagicMock()
        mock_ctx.llm.context_window_size = 1000

        with patch(f"{_MODULE}._summarize_chunk", return_value="摘要"):
            maybe_compress(msgs, mock_ctx)

        system_msgs = [m for m in msgs if m["role"] == "system"]
        assert any(m["content"] == "系统提示" for m in system_msgs)

    def test_recent_turns_preserved_after_compress(self):
        """压缩后最近 FRESH_KEEP_TURNS 轮的 user 消息内容保留"""
        msgs = [{"role": "system", "content": "系统提示"}]
        msgs += self._make_large_messages(20, content_size=2000)

        # 记录最后 FRESH_KEEP_TURNS 轮的 user 消息（压缩保留区）
        user_msgs = [m for m in msgs if m["role"] == "user"]
        recent_user_contents = {m["content"] for m in user_msgs[-FRESH_KEEP_TURNS:]}

        mock_ctx = MagicMock()
        mock_ctx.llm = MagicMock()
        mock_ctx.llm.context_window_size = 1000

        with patch(f"{_MODULE}._summarize_chunk", return_value="摘要"):
            maybe_compress(msgs, mock_ctx)

        remaining_user_contents = {m["content"] for m in msgs if m["role"] == "user"}
        assert recent_user_contents.issubset(remaining_user_contents)
