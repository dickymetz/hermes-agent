"""Tool handlers that bridge Hermes to SDD convention commands."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict


CONVENTIONS_RESOLVE_SCHEMA: Dict[str, Any] = {
    "name": "conventions_resolve",
    "description": (
        "Resolve inherited project convention packs for a file or directory. "
        "Use before brand, visual, Office, graphics, writing voice, audience, "
        "style, grammar, or syntax work."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Target path. Defaults to the current working directory.",
            },
            "surface": {
                "type": "string",
                "description": "Optional surface such as writing, office, visual, ui, plugin, or code.",
            },
        },
        "additionalProperties": False,
    },
}

AUDIT_ARTIFACT_SCHEMA: Dict[str, Any] = {
    "name": "audit_artifact",
    "description": (
        "Audit an artifact against resolved project conventions. Use for DOCX, "
        "PPTX, markdown, HTML, and visual deliverables before treating them as final."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "artifact": {
                "type": "string",
                "description": "Artifact path to audit.",
            },
            "path": {
                "type": "string",
                "description": "Convention resolution path. Defaults to the artifact path.",
            },
            "surface": {
                "type": "string",
                "description": "Optional surface such as writing, office, visual, ui, plugin, or code.",
            },
            "render": {
                "type": "boolean",
                "description": "Render Office artifacts through LibreOffice when available.",
            },
        },
        "required": ["artifact"],
        "additionalProperties": False,
    },
}


def check_sdd_available() -> bool:
    return _command_spec() is not None


def handle_conventions_resolve(args: Dict[str, Any], **_kw) -> str:
    target_path = str(args.get("path") or os.getcwd())
    command = ["conventions", "resolve", "--path", target_path, "--json"]
    if args.get("surface"):
        command.extend(["--surface", str(args["surface"])])
    return _run_sdd(command)


def handle_audit_artifact(args: Dict[str, Any], **_kw) -> str:
    artifact = str(args.get("artifact") or "").strip()
    if not artifact:
        return _json({"success": False, "error": "artifact is required"})
    command = ["convention-audit", artifact, "--json", "--no-fail"]
    if args.get("path"):
        command.extend(["--path", str(args["path"])])
    if args.get("surface"):
        command.extend(["--surface", str(args["surface"])])
    if args.get("render"):
        command.append("--render")
    return _run_sdd(command)


def _run_sdd(arguments: list[str]) -> str:
    spec = _command_spec()
    if spec is None:
        return _json(
            {
                "success": False,
                "error": "SDD command is unavailable. Set SDD_CONVENTIONS_COMMAND or install sdd.",
            }
        )
    command, cwd = spec
    process = subprocess.run(
        [*command, *arguments],
        cwd=str(cwd) if cwd else None,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if process.returncode != 0 and not process.stdout.strip():
        return _json(
            {
                "success": False,
                "returncode": process.returncode,
                "stderr": process.stderr.strip(),
            }
        )
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        payload = {"stdout": process.stdout.strip()}
    return _json(
        {
            "success": process.returncode == 0,
            "returncode": process.returncode,
            "payload": payload,
            "stderr": process.stderr.strip(),
        }
    )


def _command_spec() -> tuple[list[str], Path | None] | None:
    configured = os.environ.get("SDD_CONVENTIONS_COMMAND")
    if configured:
        return shlex.split(configured), None
    if shutil.which("sdd"):
        return ["sdd"], None
    sdd_repo = Path(os.environ.get("SDD_REPO", "/Users/richard/code/SDD"))
    if (sdd_repo / "pyproject.toml").exists() and shutil.which("uv"):
        return ["uv", "run", "sdd"], sdd_repo
    return None


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)
