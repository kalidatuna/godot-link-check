"""Command line interface."""

import argparse
import json
from pathlib import Path

from .scanner import scan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check links in Godot text resources")
    parser.add_argument("project", type=Path, help="directory containing project.godot")
    parser.add_argument("--json", action="store_true", help="write machine-readable findings")
    parser.add_argument("--include-backups", action="store_true", help="scan backup folders")
    args = parser.parse_args(argv)
    if not args.project.is_dir() or not (args.project / "project.godot").is_file():
        parser.error("project must contain a project.godot file")
    findings = scan(args.project, include_backups=args.include_backups)
    if args.json:
        print(json.dumps([finding.to_dict() for finding in findings], indent=2))
    else:
        for finding in findings:
            print(f"{finding.file}:{finding.line}: {finding.code}: {finding.message}")
        print(f"{len(findings)} finding(s)")
    return 1 if findings else 0
