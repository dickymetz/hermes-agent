---
sidebar_position: 11
title: Model Catalog
description: Remotely-hosted manifest driving curated current model picker lists for OpenRouter and Nous Portal.
---

# Model Catalog

Hermes fetches curated current model lists for **OpenRouter** and **Nous Portal** from a JSON manifest hosted alongside the docs site. This lets maintainers update picker lists without shipping a new `hermes-agent` release. The active inventory is refreshed from provider documentation and exact registry IDs; historical run reports and compatibility mappings are not rewritten by a catalog refresh.

When the manifest is unreachable (offline, network blocked, hosting failure), Hermes silently falls back to the in-repo snapshot that ships with the CLI. The manifest never breaks the picker — worst case you see whatever list was bundled with your installed version.

## Live manifest URL

```
https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
```

Published on every merge to `main` via the existing `deploy-site.yml` GitHub Pages pipeline. The source of truth lives in the repo at `website/static/api/model-catalog.json`.

## Schema

```json
{
  "version": 1,
  "updated_at": "2026-09-01T14:00:00Z",
  "metadata": {},
  "providers": {
    "openrouter": {
      "metadata": {},
      "models": [
        {"id": "openai/gpt-5.6-sol", "description": "reasoning: none → max", "metadata": {}},
        {"id": "openai/gpt-5.4-nano", "description": "reasoning controls", "metadata": {}},
        {"id": "openai/gpt-5.3-codex", "description": "coding-focused reasoning", "metadata": {}},
        {"id": "anthropic/claude-opus-5", "description": "thinking + effort: low → max"}
      ]
    },
    "nous": {
      "metadata": {},
      "models": [
        {"id": "google/gemini-3.6-flash"},
        {"id": "google/gemini-3.5-flash-lite"},
        {"id": "google/gemini-3.1-flash-lite"}
      ]
    }
  }
}
```

Field notes:

- **`version`** — integer schema version. Future schemas bump this; Hermes refuses manifests with versions it doesn't understand and falls back to the hardcoded snapshot.
- **`metadata`** — free-form dict at the manifest, provider, and model level. Any keys. Hermes ignores unknown fields, so you can annotate entries (`"tier": "paid"`, `"tags": [...]`, etc.) without coordinating a schema change.
- **`description`** — OpenRouter-only. Drives picker badge text (`"recommended"`, `"free"`, or empty). Nous Portal doesn't use this — free-tier gating is determined live from the Portal's pricing endpoint.
- **Pricing and context length** are NOT in the manifest. Those come from live provider APIs (`/v1/models` endpoints, models.dev) at fetch time.

## Current curation policy

Google's current stable Flash inventory includes `gemini-3.7-flash`, alongside retained 3.6 and 3.5 compatibility entries. This verification was refreshed on 2026-09-01. Google lists `gemini-3.1-flash-lite` as stable but announces shutdown on 2027-05-07 with `gemini-3.5-flash-lite` as the recommended replacement; retain the current ID until shutdown and do not change runtime defaults from this catalog.

DeepSeek's official change log documents `deepseek-chat` and `deepseek-reasoner` as DeepSeek-V3.2 compatibility IDs for non-thinking and thinking modes. No current DeepSeek V4 primary release was verified in this refresh, so V4 registry entries remain unverified and are excluded from this manifest.

The 2026-09-01 current set includes Claude Fable 5.1, Opus 5, Sonnet 5, GPT-5.6 Sol/Terra/Luna, Gemini 3.7 Flash, Gemini 3.6 Flash, Gemini 3.5 Flash and Flash-Lite, Gemini 3.1 Flash-Lite, Gemini 3.1 Pro (preview), and Gemma 4 open-weight checkpoints. OpenRouter availability is checked against its model registry; a registry slug does not by itself establish a model's provider support, release status, or license. Registry-only candidates, including DeepSeek V4, the Qwen3.6 URL’s redirect to Qwen3.8, GLM 5.3, and Grok 4.6 entries whose primary release or provider evidence is absent, remain explicitly unverified in the shared catalog watchlist.

The catalog may remove a previous-generation entry after a provider confirms its successor or retirement. It must not change executable defaults, historical reports, receipts, or evaluation fixtures. ChatGPT 6 / GPT-6 remains an unverified watchlist item until an official OpenAI model ID and availability statement exists.

## Fetch behavior

| When | What happens |
|---|---|
| `/model` or `hermes model` | Fetches if disk cache is stale, else uses cache |
| Disk cache fresh (< TTL) | No network hit |
| Network failure with cache | Silent fallback to cache, one log line |
| Network failure, no cache | Silent fallback to in-repo snapshot |
| Manifest fails schema validation | Treated as unreachable |

Cache location: `~/.hermes/cache/model_catalog.json`.

## Config

```yaml
model_catalog:
  enabled: true
  url: https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
  ttl_hours: 1
  providers: {}
```

Set `enabled: false` to disable remote fetch entirely and always use the in-repo snapshot.

### Per-provider override URLs

Third parties can self-host their own curation list using the same schema. Point a provider at a custom URL:

```yaml
model_catalog:
  providers:
    openrouter:
      url: https://example.com/my-openrouter-curation.json
```

The overriding manifest only needs to populate the provider block(s) it cares about. Other providers continue to resolve against the master URL.

## Updating the manifest

Maintainers:

```bash
# Re-generate from the in-repo hardcoded lists (keeps the fallback manifest in sync after
# editing OPENROUTER_MODELS or _PROVIDER_MODELS["nous"] in hermes_cli/models.py).
python scripts/build_model_catalog.py
```

Then PR the resulting change to `website/static/api/model-catalog.json` to `main`. The docs site auto-deploys on merge and the new manifest is live within a few minutes.

You can also hand-edit the JSON directly for fine-grained metadata changes that don't belong in the in-repo snapshot — the generator script is a convenience, not the single source of truth.
