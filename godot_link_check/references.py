"""Validate external resource identifiers within one text resource."""

from pathlib import Path

from .model import ExternalResource, Finding, ResourceReference


def check_ids(
    project: Path,
    source: Path,
    declarations: list[ExternalResource],
    references: list[ResourceReference],
) -> list[Finding]:
    relative_source = source.relative_to(project).as_posix()
    findings: list[Finding] = []
    seen: set[str] = set()
    for declaration in declarations:
        if declaration.resource_id in seen:
            findings.append(Finding(relative_source, declaration.line, "duplicate-id", declaration.resource_id))
        seen.add(declaration.resource_id)
    for reference in references:
        if reference.resource_id not in seen:
            findings.append(Finding(relative_source, reference.line, "unknown-id", reference.resource_id))
    return findings
