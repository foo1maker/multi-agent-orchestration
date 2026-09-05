#!/usr/bin/env python3
"""Read-only structural audit for the multi-agent orchestration skill.

The repository-local skill is audited by default. Host/global policy files are
optional and must be supplied explicitly so the script remains portable across
machines and operating systems.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SKILL_GROUPS = {
    "architecture": ("Brain thinks.", "Worker executes.", "Brain validates."),
    "native_only": ("Codex native runtime", "scheduler", "watchdog"),
    "task_contract": ("Task Contract", "raw-forward"),
    "discovery_bootstrap": (
        "TASK_MODE: EXECUTION | DISCOVERY | ANALYSIS | REVIEW",
        "DISCOVERY ROOTS",
        "bounded `DISCOVERY` contract",
    ),
    "non_duplication": ("must not secretly repeat",),
    "wait_semantics": ("quiescent wait", "list_agents"),
    "result_validation": ("RESULT_PACKET STATUS", "Stage 2", "Stage 3"),
    "clean_context": ("fork_turns", "clean Worker context"),
    "portable_worker_route": ("inherit the Codex host",),
    "worker_model_config": (
        "config/worker_defaults.yaml",
        "model: inherit",
        "reasoning_effort: auto",
        "Explicit model or reasoning-effort choice in the current user task",
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

DEFAULT_SKILL_DIR = Path(__file__).resolve().parents[1]


def emit(level: str, location: str, message: str) -> None:
    print(f"{level} {location}: {message}")


def read_text(path: Path, failures: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        failures.append(str(path))
        emit("FAIL", str(path), f"cannot read: {exc}")
        return ""


def audit_worker_config(skill_dir: Path, failures: list[str]) -> None:
    path = skill_dir / "config" / "worker_defaults.yaml"
    text = read_text(path, failures)
    if not text:
        return

    if not re.search(r"(?m)^\s*worker\s*:\s*$", text):
        failures.append("worker-config:worker")
        emit("FAIL", str(path), "missing top-level worker mapping")

    model_match = re.search(r"(?m)^\s+model\s*:\s*([^#\n]+?)\s*(?:#.*)?$", text)
    effort_match = re.search(
        r"(?m)^\s+reasoning_effort\s*:\s*([^#\n]+?)\s*(?:#.*)?$", text
    )

    if not model_match or not model_match.group(1).strip():
        failures.append("worker-config:model")
        emit("FAIL", str(path), "worker.model is missing or empty")
    if not effort_match or not effort_match.group(1).strip():
        failures.append("worker-config:reasoning_effort")
        emit("FAIL", str(path), "worker.reasoning_effort is missing or empty")


def audit_optional_global_agents(path_text: str | None, failures: list[str], warnings: list[str]) -> None:
    if not path_text:
        return
    path = Path(path_text).expanduser()
    text = read_text(path, failures)
    if not text:
        return
    for token in ("## Multi-agent orchestration", "$multi-agent-orchestration"):
        if token not in text:
            failures.append(f"global:{token}")
            emit("FAIL", f"{path} / Multi-agent orchestration", f"missing {token}")
    for marker in GLOBAL_DETAIL_MARKERS:
        if marker in text:
            failures.append(f"global-detail:{marker}")
            emit("FAIL", f"{path} / Multi-agent orchestration", f"workflow detail remains: {marker}")
    if "Simple tasks stay single-agent" not in text:
        warnings.append("global-simple-task")
        emit("WARN", f"{path} / Multi-agent orchestration", "simple-task boundary is not explicit")


def audit_optional_legacy_policy(path_text: str | None, failures: list[str]) -> None:
    if not path_text:
        return
    path = Path(path_text).expanduser()
    text = read_text(path, failures)
    if not text:
        return
    if "ARCHIVED" not in text or "multi-agent-orchestration" not in text:
        failures.append("legacy-authority")
        emit("FAIL", str(path), "legacy policy is not an archived pointer to the skill")
    if "wait_agent is an ANY-child" in text or "RESULT_PACKET\nSTATUS:" in text:
        failures.append("legacy-duplicate")
        emit("FAIL", str(path), "workflow detail still duplicates the skill")


def audit(args: argparse.Namespace) -> int:
    failures: list[str] = []
    warnings: list[str] = []
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    skill_file = skill_dir / "SKILL.md"

    skill_text = read_text(skill_file, failures)
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

    audit_worker_config(skill_dir, failures)

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for path in scripts_dir.iterdir():
            if path.name.lower() in FORBIDDEN_RUNTIME_NAMES:
                failures.append(f"runtime-script:{path.name}")
                emit("FAIL", str(path), "forbidden orchestration runtime file")

    audit_optional_global_agents(args.agents, failures, warnings)
    audit_optional_legacy_policy(args.legacy_policy, failures)

    if failures:
        emit("FAIL", "summary", f"{len(failures)} failure(s), {len(warnings)} warning(s)")
        return 1
    if warnings:
        emit("WARN", "summary", f"0 failures, {len(warnings)} warning(s)")
        return 0
    emit("PASS", "summary", "policy structure, references, and worker routing config are consistent")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill-dir",
        default=str(DEFAULT_SKILL_DIR),
        help="skill repository/root directory; defaults to the parent of this script",
    )
    parser.add_argument(
        "--agents",
        default=None,
        help="optional host/global AGENTS.md to audit; no host-specific default is assumed",
    )
    parser.add_argument(
        "--legacy-policy",
        default=None,
        help="optional archived legacy policy to audit; no machine-specific default is assumed",
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(audit(parse_args()))
