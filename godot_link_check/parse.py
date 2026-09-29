"""Parse the small subset of Godot text resource syntax needed for links."""

import json
import re

from .model import ExternalResource, ResourceReference

_ATTRIBUTE = re.compile(r'(\w+)=("(?:\\.|[^"\\])*")')
_REFERENCE = re.compile(r'ExtResource\("([^"\n]+)"\)')


def parse_resource(text: str) -> tuple[list[ExternalResource], list[ResourceReference]]:
    declarations: list[ExternalResource] = []
    references: list[ResourceReference] = []
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("[ext_resource ") and stripped.endswith("]"):
            attributes = {}
            for key, value in _ATTRIBUTE.findall(stripped):
                try:
                    attributes[key] = json.loads(value)
                except json.JSONDecodeError:
                    continue
            if isinstance(attributes.get("id"), str):
                declarations.append(
                    ExternalResource(attributes["id"], attributes.get("path"), number)
                )
        if not stripped.startswith(";"):
            references.extend(
                ResourceReference(match.group(1), number)
                for match in _REFERENCE.finditer(line)
            )
    return declarations, references
