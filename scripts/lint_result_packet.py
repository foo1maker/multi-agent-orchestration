#!/usr/bin/env python3
"""Lint RESULT_PACKET text structure without judging the underlying result."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ALLOWED_STATUSES = {"SUCCESS", "PARTIAL", "BLOCKED", "ERROR"}
NATIVE_LIFECYCLE_WORDS = {
    "RUNNING",
    "INTERRUPTED",
    "SHUTDOWN",
    "COMPLETED",
    "ERRORED",
    "NULL",
}


def emit(level: str, message: str) -> None:
    print(f"{level} result_packet: {message}")


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def lint(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines or lines[0] != "RESULT_PACKET":
        emit("FAIL", "first non-empty line must be RESULT_PACKET")
        return 1

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().upper()] = value.strip()

    status = fields.get("STATUS")
    if not status:
        emit("FAIL", "STATUS is missing")
        return 1
    status = status.upper()
    if status not in ALLOWED_STATUSES:
        if status in NATIVE_LIFECYCLE_WORDS:
            emit("FAIL", f"STATUS {status} is a native lifecycle value, not a RESULT_PACKET status")
        else:
            emit("FAIL", f"unknown STATUS {status}; allowed: {', '.join(sorted(ALLOWED_STATUSES))}")
        return 1

    if not any(key in fields for key in ("OUTPUTS", "KEY_RESULTS", "ISSUES")):
        emit("WARN", "include at least one of OUTPUTS, KEY_RESULTS, or ISSUES")
        return 0
    if "VALIDATION" not in fields and status == "SUCCESS":
        emit("WARN", "SUCCESS packet has no VALIDATION field")
        return 0

    emit("PASS", f"STATUS {status} and packet structure are valid")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="packet text file; stdin when omitted")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        packet = read_input(args.path)
    except OSError as exc:
        emit("FAIL", f"cannot read input: {exc}")
        raise SystemExit(1)
    raise SystemExit(lint(packet))
