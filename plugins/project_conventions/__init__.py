"""Hermes plugin for project convention resolution and audits."""

from __future__ import annotations

from plugins.project_conventions.tools import (
    AUDIT_ARTIFACT_SCHEMA,
    CONVENTIONS_RESOLVE_SCHEMA,
    check_sdd_available,
    handle_audit_artifact,
    handle_conventions_resolve,
)


def register(ctx) -> None:
    ctx.register_tool(
        name="conventions_resolve",
        toolset="project_conventions",
        schema=CONVENTIONS_RESOLVE_SCHEMA,
        handler=handle_conventions_resolve,
        check_fn=check_sdd_available,
        emoji="C",
    )
    ctx.register_tool(
        name="audit_artifact",
        toolset="project_conventions",
        schema=AUDIT_ARTIFACT_SCHEMA,
        handler=handle_audit_artifact,
        check_fn=check_sdd_available,
        emoji="A",
    )
