#!/usr/bin/env python3
"""Read-only structural audit for the multi-agent orchestration policy."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SKILL_GROUPS = {
    "architecture": ("Brain thinks.", "Worker executes.", "Brain validates."),
    "native_only": ("Codex native runtime", "scheduler", "watchdog"),
    "task_contract": ("Task Contract", "raw-forward"),
    "non_duplication": ("must not secretly repeat",),
    "wait_semantics": (
        "ANY-child",
        "Wait timed out.",
        "quiescent wait",
        "not a reason to create work",
    ),
    "running_immunity": ("failure evidence", "progress inspection"),
    "result_validation": ("RESULT_PACKET STATUS", "Stage 2", "Stage 3"),
    "interrupt_boundary": ("interrupt_agent", "hard deadline"),
    "worker_default": (
        "deepseek-v4-flash:0731",
        "`high` reasoning",
        "never `max`",
        "gemini-3.7-flash-high",
        "grok-4.6",
        "explicit user model or reasoning choice",
    ),
}

FORBIDDEN_RUNTIME_NAMES = {
    "scheduler.py",
    "worker_manager.py",
    "wait_loop.py",
    "recovery_engine.py",
    "agent_state.py",
    "heartbeat.py",
    "watchdog.py",
    "completion_db.py",
    "mode2_runtime.py",
}

GLOBAL_DETAIL_MARKERS = (
    "wait_agent is an ANY-child",
    "Running Worker Immunity",
    "RESULT_PACKET\nSTATUS:",
    "Stage 1 (Worker Settlement)",
    "interrupt_agent is exceptional",
)


def emit(level: str, location: str, message: str) -> None:
    print(f"{level} {location}: {message}")


def read_text(path: Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(str(path))
        emit("FAIL", str(path), f"cannot read: {exc}")
        return ""


def audit(args: argparse.Namespace) -> int:
    failures: list[str] = []
    warnings: list[str] = []
    agents = Path(args.agents)
    skill_dir = Path(args.skill_dir)
    skill_file = skill_dir / "SKILL.md"
    legacy = Path(args.legacy_policy)

    agents_text = read_text(agents, failures)
    skill_text = read_text(skill_file, failures)
    legacy_text = read_text(legacy, failures)

    if agents_text:
        for token in ("## Multi-agent orchestration", "$multi-agent-orchestration"):
            if token not in agents_text:
                failures.append(f"global:{token}")
                emit("FAIL", f"{agents} / Multi-agent orchestration", f"missing {token}")
        for marker in GLOBAL_DETAIL_MARKERS:
            if marker in agents_text:
                failures.append(f"global-detail:{marker}")
                emit("FAIL", f"{agents} / Multi-agent orchestration", f"workflow detail remains: {marker}")
        if "Simple tasks stay single-agent" not in agents_text:
            warnings.append("global-simple-task")
            emit("WARN", f"{agents} / Multi-agent orchestration", "simple-task boundary is not explicit")

    combined_skill = skill_text
    if skill_text:
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", skill_text)
        for rel in links:
            target = skill_dir / rel
            if not target.is_file():
                failures.append(f"missing-reference:{rel}")
                emit("FAIL", f"{skill_file} / references", f"missing {rel}")
            else:
                combined_skill += "\n" + read_text(target, failures)

        for section, tokens in REQUIRED_SKILL_GROUPS.items():
            missing = [token for token in tokens if token not in combined_skill]
            if missing:
                failures.append(f"skill:{section}")
                emit("FAIL", f"{skill_file} / {section}", f"missing: {', '.join(missing)}")

        frontmatter = re.match(r"\A---\s*\n(.*?)\n---", skill_text, re.S)
        if not frontmatter or "name: multi-agent-orchestration" not in frontmatter.group(1):
            failures.append("frontmatter")
            emit("FAIL", f"{skill_file} / frontmatter", "name is missing or invalid")
        if "启动模式2" not in skill_text or "parallel native multi-agent" not in skill_text:
            failures.append("activation")
            emit("FAIL", f"{skill_file} / description", "explicit Mode 2 activation terms are incomplete")

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for path in scripts_dir.iterdir():
            if path.name.lower() in FORBIDDEN_RUNTIME_NAMES:
                failures.append(f"runtime-script:{path.name}")
                emit("FAIL", str(path), "forbidden orchestration runtime file")

    if legacy_text:
        if "ARCHIVED" not in legacy_text or "multi-agent-orchestration" not in legacy_text:
            failures.append("legacy-authority")
            emit("FAIL", str(legacy), "legacy policy is not an archived pointer to the skill")
        if "wait_agent is an ANY-child" in legacy_text or "RESULT_PACKET\nSTATUS:" in legacy_text:
            failures.append("legacy-duplicate")
            emit("FAIL", str(legacy), "workflow detail still duplicates the skill")

    if failures:
        emit("FAIL", "summary", f"{len(failures)} failure(s), {len(warnings)} warning(s)")
        return 1
    if warnings:
        emit("WARN", "summary", f"0 failures, {len(warnings)} warning(s)")
        return 0
    emit("PASS", "summary", "policy structure and references are consistent")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agents", default=r"C:\Users\1\.codex\AGENTS.md")
    parser.add_argument(
        "--skill-dir",
        default=r"C:\Users\1\.codex\skills\multi-agent-orchestration",
    )
    parser.add_argument(
        "--legacy-policy",
        default=r"D:\00_SYSTEM\codex_policies\MAESTRO_MODE2.md",
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(audit(parse_args()))
