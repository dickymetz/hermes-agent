---
name: project-conventions
description: Resolve inherited project conventions and audit artifacts for brand, visual, Office, graphics, writing voice, audience, style, grammar, and syntax work.
version: 0.1.0
metadata:
  hermes:
    tags: [conventions, brand, writing, office, visual]
---

# Project Conventions

Use this skill before work that can be affected by brand, visuals, Office
formatting, graphics, writing voice, audience, style, grammar, or syntax.

1. Resolve the active convention pack with the `conventions_resolve` tool.
   Pass the exact file or directory path and the relevant surface.
2. Treat the nearest child project pack as binding. Parent packs provide
   defaults. SDD defaults are fallback only.
3. Use another project's brand or voice only as labeled inspiration when the
   current project is missing or weak on that point.
4. For final DOCX/PPTX, markdown, HTML, or visual deliverables, call
   `audit_artifact` before claiming the artifact is ready.
5. Surface ambiguity as a finding when conventions are missing, contradictory,
   or too vague to enforce.
