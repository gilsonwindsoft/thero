from __future__ import annotations

from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"

GLOBAL_CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"

BACKUP_PREFIX = "CLAUDE.md.backup"

AUDIT_FILENAME = "CLAUDE_AUDIT.md"

SKILLS_FAILED_FILENAME = "SKILLS_INSTALL_FAILED.md"

DEFAULT_COMMAND_NAME = "thero"

# Mantido como "setup_claude" por compatibilidade: perfis do
# PowerShell que ja tinham o comando instalado (antes do projeto se
# chamar "thero") sao migrados automaticamente ao reconhecer este
# marcador, em vez de duplicar o bloco.
COMMAND_MARKER_START = "# >>> setup_claude global command >>>"

COMMAND_MARKER_END = "# <<< setup_claude global command <<<"
