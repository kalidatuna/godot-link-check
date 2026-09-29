"""Walk a project and combine resource checks."""

import os
from pathlib import Path

from .model import Finding
from .parse import parse_resource
from .paths import check_paths
from .references import check_ids


def scan(project: Path, include_backups: bool = False) -> list[Finding]:
    project = project.resolve()
    excluded = {".git", ".godot"}
    if not include_backups:
        excluded.add("backups")
    findings: list[Finding] = []
    for current, directories, files in os.walk(project, followlinks=False):
        directories[:] = sorted(name for name in directories if name not in excluded)
        for name in sorted(files):
            if Path(name).suffix not in {".tscn", ".tres"}:
                continue
            source = Path(current) / name
            if source.is_symlink():
                continue
            try:
                text = source.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                findings.append(Finding(source.relative_to(project).as_posix(), 0, "read-error", str(error)))
                continue
            declarations, references = parse_resource(text)
            findings.extend(check_paths(project, source, declarations))
            findings.extend(check_ids(project, source, declarations, references))
    return sorted(findings, key=lambda item: (item.file, item.line, item.code, item.message))
