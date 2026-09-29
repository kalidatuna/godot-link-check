"""Resolve and check project-relative resource paths."""

from pathlib import Path, PurePosixPath

from .model import ExternalResource, Finding


def check_paths(
    project: Path, source: Path, declarations: list[ExternalResource]
) -> list[Finding]:
    findings: list[Finding] = []
    relative_source = source.relative_to(project).as_posix()
    for declaration in declarations:
        value = declaration.path
        if not isinstance(value, str) or not value.startswith("res://"):
            continue
        relative = value.removeprefix("res://")
        parts = PurePosixPath(relative).parts
        if not relative or ".." in parts or relative.startswith("/"):
            findings.append(Finding(relative_source, declaration.line, "unsafe-path", value))
            continue
        target = (project / relative).resolve()
        if not target.is_relative_to(project.resolve()):
            findings.append(Finding(relative_source, declaration.line, "unsafe-path", value))
        elif not target.is_file():
            findings.append(Finding(relative_source, declaration.line, "missing-file", value))
    return findings
