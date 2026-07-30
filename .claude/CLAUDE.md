# MTG Deckbuilder — Instructions

Always verify every card via Scryfall before including it in any output. Never use assumed or memorized set codes or collector numbers.

## Output Convention (all skills)
Save files to `/mnt/user-data/outputs/`. Call `present_files` once after all files for a task are saved.

## Skill routing

This project's skills self-declare their own trigger conditions in each `SKILL.md`'s frontmatter `description` — that's what actually drives routing, so it isn't duplicated here as a lookup table (a hand-maintained copy of that routing previously went stale and pointed at two skills that no longer exist). For the current skill list, functional-role tagging reference, and how the skills depend on each other, see `.claude/skills/` and the project README.
