# Design System: Hermes

> Source of truth for Hermes' visual language. The Hermes web dashboard (React 19 + Vite + Tailwind v4) renders on top of the internal `@nous-research/ui` design system (v^0.10.0). This document captures the canonical Hermes look (LENS_0 — "Hermes Teal") plus the six built-in dashboard themes that ship as runtime presets in `web/src/themes/presets.ts`.

## 1. Visual Theme & Atmosphere

Hermes is a self-improving terminal-native AI agent built by Nous Research. The dashboard is the agent's window — not its center of gravity. The default look is a **deep nocturnal teal canvas with a warm cream foreground and a single low-amber vignette in the top-left corner**, evoking a CRT glowing in a dim room rather than a bright SaaS dashboard. [needs-review]

- **Mood**: nocturnal, contemplative, terminal-adjacent. Equal parts research lab and personal chamber. [needs-review]
- **Anti-skeuomorphism**: no drop shadows, no gradients-as-decoration, no glassmorphism. Depth is communicated through `mix-blend-mode` (difference, lighten, plus-lighter, color-dodge) and an SVG noise grain layer rather than blurs.
- **Layered backdrop** (canonical, see `web/src/components/Backdrop.tsx`): four stacked layers — `z-1` solid background with `difference` blend, `z-2` inverted filler image at ~3.3% opacity, `z-99` warm top-left vignette (`--warm-glow`) at 22% opacity with `lighten` blend, `z-101` SVG noise grain at ~55% opacity with `color-dodge` (gated on GPU tier; auto-disabled for `prefers-reduced-motion` and software rasterizers).
- **Living surface**: the canvas is never flat. The grain + difference-blend stack means the same hex appears subtly different across the viewport. [needs-review]
- **Theme-switchable**: every visual decision flows through CSS custom properties (`--background-base`, `--midground-base`, `--warm-glow`, `--theme-font-sans`, etc.) so the entire UI repaints when a user picks a different theme — no remount, no flash.
- **Logos & marks**: use `mix-blend-mode: plus-lighter` (the `.blend-lighter` utility) so they sit on the canvas as light, not as opaque graphics. [needs-review]

## 2. Color Palette & Roles

Hermes uses a **two-axis palette**: `background` (canvas) and `midground` (foreground/text/borders), with a third `foreground` slot intentionally set to alpha 0 in LENS_0 (used as a token slot, not a visible color). All UI tints are derived from these two anchors via `color-mix()` rather than hand-picked grays — this keeps every theme internally coherent.

### Canonical palette — LENS_0 (Hermes Teal, default)

| Role | Name | Hex | Notes |
|---|---|---|---|
| Canvas / background | Hermes Deep Teal | `#041c1c` | The default page/app background. Solid + difference-blended. |
| Midground / foreground / text / borders | Hermes Cream | `#ffe6cb` | Primary text, primary buttons, borders (at 15% mix), rings. |
| Foreground slot (token-only) | Pure White (transparent) | `#ffffff` (alpha 0) | Reserved token slot; not visible by default. |
| Warm vignette | Amber Glow | `rgba(255, 189, 56, 0.35)` | Top-left atmospheric glow only. |
| Destructive | Bright Red | `#fb2c36` | Error / destructive actions. |
| Success | Green Tea | `#4ade80` | Success states. |
| Warning | Amber | `#ffbd38` | Warnings, sidebar status indicators. |

### Derived semantic tokens (LENS_0)

These are computed via `color-mix()` against `--midground-base` and `--background-base` and exposed as Tailwind/shadcn tokens in `web/src/index.css`:

- **Card** = `mix(midground 4%, background)` — slightly lifted surfaces.
- **Secondary** = `mix(midground 6%, background)` — secondary buttons.
- **Muted** = `mix(midground 8%, background)` — muted regions.
- **Muted foreground** = `mix(midground 55%, transparent)` — secondary text.
- **Accent** = `mix(midground 10%, background)` — hover surfaces.
- **Border / Input** = `mix(midground 15%, transparent)` — hairline borders.
- **Ring** = full midground — focus rings.
- **Popover** = `mix(midground 4%, background)` — popovers, dialogs.

### Built-in theme presets (alternate palettes)

Each is a complete swap of `background` + `midground` + `warmGlow` + typography + radius. Defined in `web/src/themes/presets.ts`. Theme name is the `name` key consumed by the backend in `hermes_cli/web_server.py`.

| Theme | Background | Midground | Warm Glow | Notes |
|---|---|---|---|---|
| `default` — Hermes Teal | `#041c1c` | `#ffe6cb` | `rgba(255,189,56,0.35)` | The canonical Hermes look. |
| `default-large` — Hermes Teal (Large) | `#041c1c` | `#ffe6cb` | `rgba(255,189,56,0.35)` | Same palette, 18px base, spacious density. |
| `midnight` — Midnight | `#0a0a1f` | `#d4c8ff` | `rgba(167,139,250,0.32)` | Deep blue-violet, lavender accents. |
| `ember` — Ember | `#1a0a06` | `#ffd8b0` | `rgba(249,115,22,0.38)` | Crimson + bronze; destructive `#c92d0f`, warning `#f97316`. |
| `mono` — Mono | `#0e0e0e` | `#eaeaea` | `rgba(255,255,255,0.10)` | Grayscale, zero radius. |
| `cyberpunk` — Cyberpunk | `#040608` | `#9bffcf` | `rgba(0,255,136,0.22)` | Neon-on-black; success `#00ff88`, warning `#ffd700`, destructive `#ff0055`. |
| `rose` — Rosé | `#1a0f15` | `#ffd4e1` | `rgba(249,168,212,0.30)` | Soft pink + warm ivory. |

### Color rules

- **Never hardcode background hex in components** — always go through `var(--background-base)` or the Tailwind alias (`bg-background`).
- **Never hardcode foreground hex in components** — use `text-midground`, `text-foreground`, or `text-muted-foreground`.
- **Borders** are derived (`border-current/10`, `border-border`), not hand-picked grays.
- **Glow is the only ambient color** — there are no hand-painted shadows. If a region needs lift, raise the midground mix from 4% → 6% → 8%.

## 3. Typography Rules

Hermes' typography stack is **theme-defined and CSS-variable-driven**. The default LENS_0 deliberately uses the system stack so the dashboard looks native on every OS. Themes that override fonts pull them from Google Fonts at runtime (`fontUrl` in the theme object).

### Default stack (LENS_0)

- **Sans (`--theme-font-sans`)**: `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
- **Mono (`--theme-font-mono`)**: `ui-monospace, "SF Mono", "Cascadia Mono", Menlo, Consolas, monospace`
- **Display (`--theme-font-display`)**: aliases sans by default

### Locally bundled display fonts (`web/public/fonts/`)

These ship with the `@nous-research/ui` package and are synced into `public/fonts/` by the `sync-assets` npm script. They are used by Nous DS components (notably `<Typography mondwest …>`):

- **Collapse** (Regular, Bold) — display sans, used for headings/numerics. [needs-review]
- **Mondwest** (Regular) — geometric display, used for sidebar status, version chips, footer org link.
- **RulesCompressed** (Regular, Medium) — condensed display, used for dense labels. [needs-review]
- **RulesExpanded** (Regular, Bold) — wide display, used for prominent titles. [needs-review]

### Locally bundled terminal font (`web/public/fonts-terminal/`)

- **JetBrains Mono** (Regular, Bold, Italic) — the embedded TUI font. Wired into xterm.js via `ChatPage` so the `/chat` tab has a true monospace even on systems without one installed locally. Apache-2.0.

### Theme-specific font stacks (Google Fonts at runtime)

- `midnight`: **Inter** (sans) + **JetBrains Mono** (mono), letter-spacing `-0.005em`, radius `0.75rem`.
- `ember`: **Spectral** (serif sans) + **IBM Plex Mono**, radius `0.25rem`.
- `mono`: **IBM Plex Sans** + **IBM Plex Mono**, radius `0`.
- `cyberpunk`: **Share Tech Mono** + **JetBrains Mono** (mono everywhere), radius `0`.
- `rose`: **Fraunces** (variable serif) + **DM Mono**, radius `1rem`.

### Type scale

- **Base size**: `15px` (LENS_0), `18px` (large variants). `--theme-base-size`.
- **Line-height**: `1.55` (LENS_0), `1.65` (large). `--theme-line-height`.
- **Letter-spacing**: `0` default. Themes can tighten (e.g. midnight: `-0.005em`).
- **Tracked overrides** (set inline in components): wide-tracked uppercase labels at `tracking-[0.1em]` to `tracking-[0.15em]` (sidebar nav, footer org link, version chips).
- **`small` is bumped to `1.0625rem`** and `code` to `0.875rem` — these match the nousnet hermes-agent layout for dashboard readability.

### Font-feature conventions

- **`tabular-nums`** on every numeric readout (versions, counters, status strips). [needs-review]
- **`lowercase`** on chrome metadata (version chips, org footer) for the lab/zine vibe.
- **`mix-blend-mode: plus-lighter`** on logo wordmarks and footer brand tag so they read as light, not paint.

## 4. Component Stylings

The dashboard composes from `@nous-research/ui` (referred to as "Nous DS" or "Noui") — a published React design system. App-level components live in `web/src/components/` and pages in `web/src/pages/`. Tailwind v4 utility classes resolve through the shadcn-compat token layer in `index.css`.

### Imported Nous DS primitives in active use

- `@nous-research/ui/ui/components/button` — `<Button>` (CTA, secondary, destructive variants).
- `@nous-research/ui/ui/components/list-item` — `<ListItem>` (used in nav, list rows).
- `@nous-research/ui/ui/components/selection-switcher` — `<SelectionSwitcher>` (theme/variant pickers).
- `@nous-research/ui/ui/components/spinner` — `<Spinner>` (loading states).
- `@nous-research/ui` `<Typography>` — re-exported via `web/src/components/NouiTypography.tsx`. Supports `mondwest` prop for the display variant.
- `@nous-research/ui/hooks/use-gpu-tier` — gates the noise-grain layer for low-power devices.
- `@nous-research/ui/styles/globals.css` — the package's token + reset baseline (imported first in `web/src/index.css`).

### App-level component patterns

- **Sidebar / nav** (`App.tsx`): primary navigation lives in a left sidebar; nav items use `lucide-react` icons (`Activity`, `Terminal`, `Cpu`, `Settings`, `Sparkles`, `Wrench`, etc.). Active state via `NavLink` + Tailwind. Status strip + footer at the bottom.
- **Backdrop** (`components/Backdrop.tsx`): the four-layer atmospheric stack (see Visual Theme). Always rendered; never per-page.
- **Cards / surfaces**: use `bg-card` + `border-border` (token-driven). No box-shadow.
- **Buttons**: from Nous DS. App-level styling never overrides the DS button — variants are picked via the DS prop API.
- **Dialogs / popovers** (`SlashPopover.tsx`, `ModelPickerDialog.tsx`, `confirm-dialog.tsx`): use `bg-popover` + `border-border`, animate via `dialog-in` keyframe (`opacity 0→1`, `translateY(4px) scale(0.98)→0,1`). 200ms-ish entrances.
- **Toasts** (`components/Toast.tsx`): slide in from the right via `toast-in` keyframe (`translateX(16px)→0`).
- **Markdown** (`components/Markdown.tsx`): styled prose for agent output.
- **Tool calls** (`components/ToolCall.tsx`): collapsible code-style blocks for agent tool invocation transcripts.
- **Embedded TUI** (`pages/ChatPage.tsx`): xterm.js with addons (`fit`, `unicode11`, `web-links`, `webgl`) — uses JetBrains Mono.
- **Plugins surface** (`web/src/plugins/`): plugin pages and slots loaded from `/dashboard-plugins/*`; slot architecture lets external plugins inject UI without forking the dashboard.

### Iconography

- **Library**: `lucide-react` (v0.577) — strict adherence, no mixing with other icon sets.
- **Sizing**: small icons read in nav rails and inline with text; pair size with the text size, not arbitrary pixel values. [needs-review]
- **Color**: inherits `currentColor` from the surrounding text token — never colored independently.

### Visual effects

- **`.blend-lighter` utility** (`mix-blend-mode: plus-lighter`) — for logos, wordmarks, brand titles.
- **`.grain` utility** — adds a 12%-opacity 2px conic-gradient pattern (used on badges).
- **`.scrollbar-none` utility** — hides scrollbars on the header overflow-x nav row.
- **GSAP** (v3.15) — used for keyed animation sequences (where react-spring would be too heavy). [needs-review]
- **`@react-three/fiber` + three** — present for 3D/visualization on `/analytics`. [needs-review]

## 5. Layout Principles

- **Full-viewport shell**: `html`, `body`, `#root` are all `height: 100%; max-height: 100%; overflow: hidden`. The dashboard is an app, not a scrolling document — only inner regions scroll.
- **Density tokens**: the `--theme-spacing-mul` CSS variable feeds Tailwind v4's `--spacing` so `comfortable` (1×) and `spacious` (1.25×–1.5×) themes scale every `p-N` / `gap-N` / `space-*` proportionally. No hand-tuned spacing per theme.
- **Radius tokens**: `--theme-radius` (default `0.5rem`) feeds `radius-sm/md/lg/xl` (sm = `radius - 4px`, xl = `radius + 4px`). Themes can pin to `0` (mono, cyberpunk), `0.25rem` (ember), `0.75rem` (midnight), or `1rem` (rose).
- **Sidebar + content split**: classic two-column app shell. Sidebar is fixed-width with internal scroll; the right pane swaps via React Router routes.
- **Persistent embedded chat host**: when `__HERMES_DASHBOARD_EMBEDDED_CHAT__` is true, the chat page is rendered persistently outside `<Routes>` so the terminal session survives route changes.
- **Modular plugin pages**: `/plugins/<id>` routes mount plugin UI from `/dashboard-plugins/<id>`; plugin slots can also embed inline.

## 6. Depth & Elevation

Depth is **chromatic**, not shadow-based.

- **Layer 0 — canvas**: solid background hex.
- **Layer 1 — atmosphere**: difference blend, inverted filler image at 3.3%, warm vignette at 22%, noise grain at ~55%.
- **Layer 2 — surface**: `bg-card` (4% midground mix), `bg-popover` (4% mix), `bg-secondary` (6% mix), `bg-muted` (8% mix), `bg-accent` (10% mix). The deeper the level, the more midground bleed.
- **Layer 3 — borders**: `mix(midground 15%, transparent)` — visible on every surface but never harsh.
- **Layer 4 — focus / emphasis**: full midground for `ring-ring`, `border-input` on focus, primary buttons.
- **No `box-shadow`** as elevation. If a popover or dialog needs to detach, it does so via the surface mix percentage and an animated entrance, not a drop shadow.
- **Glow** (warm vignette) is **ambient only** — never tied to component hover or active state. [needs-review]

## 7. Do's and Don'ts

### Do

- Use the theme tokens (`var(--background-base)`, `var(--midground-base)`, `bg-background`, `text-midground`, `border-border`, etc.) — never raw hex in component files.
- Compose new surfaces by adjusting the midground-mix percentage (4% → 6% → 8% → 10%), so they automatically retheme.
- Trust `--theme-spacing-mul` and `--theme-radius` — write Tailwind utilities normally and let theme density/radius cascade.
- Hide scrollbars in horizontal nav rails (`.scrollbar-none`).
- Use `mix-blend-mode: plus-lighter` on logos and wordmarks so they sit on the canvas as light. [needs-review]
- Use `lucide-react` icons exclusively at sizes that pair with surrounding text.
- Wrap text in `<Typography>` (re-exported via `NouiTypography`) when display variants are needed. [needs-review]
- Keep numeric readouts on `tabular-nums`. [needs-review]
- Auto-disable expensive layers (noise grain) when `useGpuTier()` returns 0.

### Don't

- Don't introduce a third color axis. The system is two-anchor (background + midground); resist adding "primary blue" or "brand accent". [needs-review]
- Don't use `box-shadow` for elevation. Depth is chromatic + grain + blend-mode.
- Don't hardcode font families in components — go through `--theme-font-sans` / `--theme-font-mono` (or the Tailwind `font-sans` / `font-mono` utilities).
- Don't paint over the warm vignette with a per-component glow — the warm glow is global atmosphere, not a component effect. [needs-review]
- Don't introduce new icon libraries — `lucide-react` is the single source.
- Don't mix `@nous-research/ui` button styling with hand-rolled buttons — extend the DS, don't fork it.
- Don't allow the page to scroll the document — only inner regions scroll.
- Don't use the `--foreground` token for visible text (it's alpha 0 in LENS_0); use `--midground` / `text-midground` / `text-foreground` (which is aliased to midground).
- Don't ship a theme without all four anchors (`background`, `midground`, `warmGlow`, plus typography stack) — see `web/src/themes/types.ts`.

## 8. Responsive Behavior

- **Primary target**: desktop dashboard. The Hermes web UI is the agent's control panel, typically running alongside the terminal — not a phone-first product. [needs-review]
- **Viewport units**: the shell uses `100dvh` / `max-height: 100dvh` so it adapts to mobile browser chrome correctly when accessed from a phone. [needs-review]
- **Sidebar collapse**: there's a `Menu`/`X` icon pair in `App.tsx` — the sidebar collapses to a hamburger at narrow widths. [needs-review]
- **Density themes**: the `default-large` preset bumps base size to 18px and switches density to `spacious` for users who want a roomier feel — no separate "mobile" theme is shipped.
- **Plugin pages** are responsible for their own responsive behavior; the host shell only guarantees a scrollable content region. [needs-review]
- **No fixed pixel breakpoints in shared components** — components rely on Tailwind's `sm`/`md`/`lg`/`xl` defaults and on flex/grid intrinsic sizing. [needs-review]

## 9. Agent Prompt Guide

When asking Claude (or any agent) to design or build new Hermes UI, prefer prompts shaped like these:

- **Atmosphere reminder**: "This is the Hermes dashboard — nocturnal teal canvas (`#041c1c`), cream foreground (`#ffe6cb`), single warm top-left vignette. No drop shadows, no gradients-as-decoration. Depth comes from `mix-blend-mode` and the noise grain layer."
- **Token-first**: "Use `var(--background-base)` / `var(--midground-base)` / `var(--warm-glow)` and the shadcn-compat tokens (`bg-card`, `text-muted-foreground`, `border-border`). Never hardcode hex."
- **Two-anchor rule**: "The palette is exactly two anchors — background and midground. Do not introduce a third brand color. Derive surfaces by `color-mix()` against midground at 4 / 6 / 8 / 10 / 15 percent."
- **Typography**: "Sans + mono come from `--theme-font-sans` / `--theme-font-mono`. Display moments can use Mondwest, Collapse, RulesExpanded, or RulesCompressed via `<Typography mondwest>` / `font-mondwest`. Numerics get `tabular-nums`. Chrome metadata is lowercase + wide-tracked (`tracking-[0.1em]` to `tracking-[0.15em]`)."
- **Components first**: "Compose with `@nous-research/ui` primitives — `<Button>`, `<ListItem>`, `<SelectionSwitcher>`, `<Spinner>`, `<Typography>`. Icons are `lucide-react`."
- **Theme-portable**: "Whatever you build must look right in all seven themes (default, default-large, midnight, ember, mono, cyberpunk, rose). If you find yourself writing per-theme overrides, you're using a token wrong."
- **Layout**: "Full-height shell, no document scroll. Sidebar + content. Use `100dvh`. Density and radius come from theme tokens."
- **Anti-skeuomorphism**: "No `box-shadow`. No glassmorphism. No gradient buttons. Depth is `mix-blend-mode` and surface-mix percentages."
- **Reduced-motion**: "Gate any expensive or animated effect on `useGpuTier()` from `@nous-research/ui/hooks/use-gpu-tier`."

When in doubt, the visual reference is `web/src/components/Backdrop.tsx` + `web/src/index.css` (the `:root` and `@theme inline` blocks). If something looks off, those two files are the source of truth.
