from __future__ import annotations

from pathlib import Path

from thero.system.process import command_exists, run_command
from thero.system.prompt import confirm

DEFAULT_TOOLS_ROOT = Path.home() / ".thero" / "tools"


def _local_head(repo_dir: Path) -> str | None:

    result = run_command(["git", "-C", str(repo_dir), "rev-parse", "HEAD"])

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def _remote_head(repo_url: str) -> str | None:

    result = run_command(["git", "ls-remote", repo_url, "HEAD"])

    if result.returncode != 0 or not result.stdout.strip():
        return None

    return result.stdout.split()[0]


def ensure_tool_repo(
    name: str,
    repo_url: str,
    entry_script: str,
    *,
    tools_root: Path = DEFAULT_TOOLS_ROOT,
) -> Path | None:
    """
    Garante uma copia local gerenciada de uma ferramenta thero (ex.:
    Athena, Zeus), clonando ou atualizando via git quando necessario.

    Generico: recebe nome da ferramenta, URL do repo git e caminho do
    script de entrada relativo a raiz do repo clonado. Nao depende do
    layout do monorepo myscripts.

    Antes de clonar: se ja existir uma copia gerenciada em
    "tools_root/name", so clona/atualiza quando o HEAD local estiver
    atras do HEAD remoto (comparando commits via git); se ja estiver
    em dia, nao faz nada.
    """

    if not command_exists("git"):
        print(
            f"[ERROR] git nao encontrado. Instale o git para "
            f"permitir a instalacao automatica de {name}."
        )
        return None

    repo_dir = tools_root / name
    entry_path = repo_dir / entry_script

    if not repo_dir.is_dir():

        if not confirm(
            f"{name} nao encontrado. Clonar {repo_url} em {repo_dir}?",
            default=False,
        ):
            return None

        tools_root.mkdir(parents=True, exist_ok=True)

        clone_result = run_command(
            ["git", "clone", repo_url, str(repo_dir)],
            capture=False,
        )

        if clone_result.returncode != 0:
            print(f"[ERROR] falha ao clonar {name}.")
            return None

        return entry_path if entry_path.is_file() else None

    local_sha = _local_head(repo_dir)
    remote_sha = _remote_head(repo_url)

    if local_sha and remote_sha and local_sha != remote_sha:

        if confirm(
            f"{name} desatualizado ({local_sha[:7]} -> "
            f"{remote_sha[:7]}). Atualizar agora?",
            default=False,
        ):
            update_result = run_command(
                ["git", "-C", str(repo_dir), "pull", "--ff-only"],
                capture=False,
            )

            if update_result.returncode != 0:
                print(
                    f"[WARN] falha ao atualizar {name}; usando "
                    "copia local existente."
                )

    return entry_path if entry_path.is_file() else None
