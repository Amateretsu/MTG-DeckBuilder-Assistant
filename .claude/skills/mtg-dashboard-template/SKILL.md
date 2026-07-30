---
name: mtg-dashboard-template
description: Shared visual design system for Magic The Gathering dashboard/widget output — color palette, Chart.js option defaults, stat-card grid CSS, badge components, dark-mode detection, and accessibility conventions. Used internally by mtg-visualization and mtg-budget-swaps so both skills render from one consistent look instead of independently inventing colors and layout. Also trigger this directly if the user asks about this project's dashboard styling or wants a new MTG dashboard-producing skill to match the existing visual style.
compatibility: Pure reference skill, no workflow of its own — mirrors mtg-card-taxonomy's role as a shared dependency, this time for visual design rather than card categorization. If the general-purpose `dataviz` skill is present this session, defer to its palette-contrast/layout heuristics for anything not covered here; this skill exists to carry the MTG-domain-specific tokens a general skill can't know, and must work fully standalone when `dataviz` isn't installed.
---

# MTG Dashboard Template

A single shared reference — `references/Dashboard-Style-Guide.md` — for the visual system behind every MTG dashboard/widget this suite produces. `mtg-visualization` and `mtg-budget-swaps` both render interactive HTML widgets via `visualize:show_widget`; this skill exists so they draw from one palette and one set of layout primitives instead of each restating (and slowly diverging from) its own copy.

**If you're mtg-visualization or mtg-budget-swaps:** read `references/Dashboard-Style-Guide.md` for colors, CSS, and component patterns. Don't inline your own copy of the palette or stat-card CSS — if the visual system changes, it should only need to change here.

## Scope — what this skill owns vs. doesn't

**Owns:** color palette and semantic tokens, dark-mode detection, Chart.js option defaults, the stat-card grid pattern, the badge component, accessibility conventions. Pure look-and-feel primitives.

**Does not own:** which charts to draw or what data goes in them (`mtg-visualization`'s job), the expensive-card-selection algorithm or per-swap copy (`mtg-budget-swaps`'s job). Never add domain/data logic here — if a design decision requires knowing what a mana curve or a price swap *is*, it belongs in the consuming skill, not this one.

See `references/Dashboard-Style-Guide.md` for the full palette, CSS blocks, and component specs.
