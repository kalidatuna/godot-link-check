"""Shared records for findings and parsed resources."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ExternalResource:
    resource_id: str
    path: str | None
    line: int


@dataclass(frozen=True)
class ResourceReference:
    resource_id: str
    line: int


@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    code: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)
