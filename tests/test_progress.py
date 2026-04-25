"""Tests for JSON progress output."""

import json

import pytest

from site2vault.progress import JsonEmitter, RichEmitter, set_emitter, get_emitter, emit


class TestJsonEmitter:
    def test_emits_valid_json(self, capsys):
        emitter = JsonEmitter()
        emitter.emit("test_event", url="https://example.com", count=5)

        captured = capsys.readouterr()
        line = captured.out.strip()
        data = json.loads(line)
        assert data["event"] == "test_event"
        assert data["url"] == "https://example.com"
        assert data["count"] == 5
        assert "ts" in data

    def test_emits_one_line_per_event(self, capsys):
        emitter = JsonEmitter()
        emitter.emit("event_1", a=1)
        emitter.emit("event_2", b=2)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["event"] == "event_1"
        assert json.loads(lines[1])["event"] == "event_2"

    def test_required_fields(self, capsys):
        emitter = JsonEmitter()
        emitter.emit("run_start", seed_url="https://example.com")

        data = json.loads(capsys.readouterr().out.strip())
        assert "event" in data
        assert "ts" in data

    def test_run_end_has_exit_code(self, capsys):
        emitter = JsonEmitter()
        emitter.emit("run_end", exit_code=0, stats={"done": 10})

        data = json.loads(capsys.readouterr().out.strip())
        assert data["event"] == "run_end"
        assert data["exit_code"] == 0

    def test_all_event_types(self, capsys):
        emitter = JsonEmitter()
        events = [
            ("run_start", {"config": {}}),
            ("phase_start", {"phase": "crawl"}),
            ("fetch_start", {"url": "https://example.com", "depth": 0}),
            ("fetch_done", {"url": "https://example.com", "status": 200, "bytes": 1000, "duration_ms": 100}),
            ("fetch_failed", {"url": "https://example.com/bad", "reason": "timeout", "attempt": 3}),
            ("note_written", {"url": "https://example.com", "file": "Page.md"}),
            ("phase_end", {"phase": "crawl", "stats": {"done": 1}}),
            ("phase_start", {"phase": "rewrite"}),
            ("phase_end", {"phase": "rewrite"}),
            ("phase_start", {"phase": "index"}),
            ("phase_end", {"phase": "index"}),
            ("phase_start", {"phase": "manifest"}),
            ("phase_end", {"phase": "manifest"}),
            ("run_end", {"exit_code": 0, "stats": {}}),
        ]

        for event, fields in events:
            emitter.emit(event, **fields)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == len(events)
        for line in lines:
            data = json.loads(line)
            assert "event" in data
            assert "ts" in data


class TestRichEmitter:
    def test_does_not_emit_json_to_stdout(self, capsys):
        """RichEmitter routes through the logger, not raw JSON to stdout."""
        emitter = RichEmitter()
        emitter.emit("run_start", seed_url="https://example.com")

        captured = capsys.readouterr()
        # Should NOT produce JSON lines (that's JsonEmitter's job)
        for line in captured.out.strip().split("\n"):
            if line.strip():
                with pytest.raises(json.JSONDecodeError):
                    json.loads(line)


class TestGlobalEmitter:
    def test_set_and_get(self):
        original = get_emitter()
        try:
            new_emitter = JsonEmitter()
            set_emitter(new_emitter)
            assert get_emitter() is new_emitter
        finally:
            set_emitter(original)

    def test_emit_uses_global(self, capsys):
        original = get_emitter()
        try:
            set_emitter(JsonEmitter())
            emit("test_global", x=1)
            data = json.loads(capsys.readouterr().out.strip())
            assert data["event"] == "test_global"
        finally:
            set_emitter(original)
