MERGE_PROMPT = r"""
You are consolidating a user's global Claude Code instructions.

You have two documents:

1. EXISTING CLAUDE.md
2. NEW ENGINEERING OPERATING SYSTEM

Create one final CLAUDE.md.

IMPORTANT RULES:

- Preserve useful existing instructions.
- Preserve user-specific preferences.
- Preserve existing workflow rules.
- Preserve intentional project conventions.
- Add useful engineering rules from the new system.
- Remove obvious duplication.
- Resolve contradictions intelligently.
- Specific project/user instructions take precedence over generic
  engineering guidance.
- Never weaken security requirements.
- Do not invent facts about the user's projects.
- Keep the final document concise.
- Do not include explanations about the merge.
- Do not include a changelog.
- Do not include markdown fences.
- Output ONLY the final CLAUDE.md contents.

The goal is a high-signal instruction file, not a giant prompt.

Avoid repeating technology-specific knowledge that should be
provided by Agent Skills.

Existing CLAUDE.md:

---BEGIN EXISTING---

{existing}

---END EXISTING---

New Engineering Operating System:

---BEGIN NEW---

{new_rules}

---END NEW---
"""
