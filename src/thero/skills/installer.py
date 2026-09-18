from __future__ import annotations

import datetime
from pathlib import Path

from thero.settings import SKILLS_FAILED_FILENAME
from thero.skills.catalog import SKILL_REPOSITORIES
from thero.system.process import run_command


def build_skill_install_command(
    repo: str,
    skill: str,
    global_install: bool = True,
) -> list[str]:

    command = [
        "npx",
        "skills",
        "add",
        repo,
        "--skill",
        skill,
        "--agent",
        "claude-code",
    ]

    if global_install:
        command.append("--global")

    command.append("--yes")

    return command


def install_single_skill(
    repo: str,
    skill: str,
    global_install: bool = True,
) -> bool:

    command = build_skill_install_command(
        repo,
        skill,
        global_install,
    )

    result = run_command(
        command,
        capture=False,
    )

    if result.returncode == 0:
        print(
            f"[OK] Installed {skill}"
        )
        return True

    print(
        f"[WARN] Could not install "
        f"{skill} from {repo}"
    )

    return False


def install_repository_skills(
    repository: dict,
    global_install: bool = True,
) -> list[dict]:

    repo = repository["repo"]
    wanted = repository["wanted"]

    print()
    print("=" * 70)
    print(
        f"Skill group: {repository['name']}"
    )
    print(
        f"Repository: {repo}"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Cada skill é instalada individualmente.
    #
    # Isso é proposital.
    #
    # Se uma skill foi removida/renomeada, as demais continuam.
    # --------------------------------------------------------

    successful = 0
    failed_skills: list[dict] = []

    for skill in wanted:

        if install_single_skill(
            repo,
            skill,
            global_install,
        ):
            successful += 1
        else:
            command = " ".join(
                build_skill_install_command(
                    repo,
                    skill,
                    global_install,
                )
            )
            failed_skills.append(
                {
                    "group": repository["name"],
                    "repo": repo,
                    "skill": skill,
                    "command": command,
                }
            )

    print()
    print(
        f"[SUMMARY] {repo}: "
        f"{successful} installed, "
        f"{len(failed_skills)} unavailable/failed"
    )

    return failed_skills


def install_impeccable() -> dict | None:
    """
    "impeccable" não usa o CLI genérico "npx skills add" — tem o
    próprio instalador ("npx impeccable install"). Instalar de novo
    é seguro mesmo se já estiver instalada (o próprio pacote decide
    o que fazer); não tentamos detectar presença antes.

    Retorna um dict de falha (mesmo formato usado por
    write_failed_skills_report) em caso de erro, ou None se ok.
    """

    print()
    print("=" * 70)
    print("Skill: impeccable")
    print("=" * 70)

    command = ["npx", "impeccable", "install"]

    result = run_command(
        command,
        capture=False,
    )

    if result.returncode == 0:
        print(
            "[OK] Installed impeccable"
        )
        return None

    print(
        "[WARN] Could not install impeccable"
    )

    return {
        "group": "Impeccable",
        "repo": "(npm package: impeccable)",
        "skill": "impeccable",
        "command": " ".join(command),
    }


def write_failed_skills_report(
    failed_skills: list[dict],
    report_dir: Path,
) -> None:

    report_path = report_dir / SKILLS_FAILED_FILENAME

    if not failed_skills:

        # Remove relatório antigo para não sugerir falhas que já
        # não existem mais.
        if report_path.exists():
            report_path.unlink()

        print()
        print(
            "[OK] All skills installed successfully."
        )

        return

    lines = [
        "# Skills que falharam na instalação",
        "",
        f"Gerado em: {datetime.datetime.now().isoformat(timespec='seconds')}",
        "",
        "Envie este arquivo para o Claude corrigir os nomes/repos "
        "das skills.",
        "",
    ]

    for item in failed_skills:

        lines.append(
            f"- [{item['group']}] repo={item['repo']} "
            f"skill={item['skill']}"
        )
        lines.append(
            f"  comando: {item['command']}"
        )

    report_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print()
    print("=" * 70)
    print(
        f"[WARN] {len(failed_skills)} skill(s) failed to install."
    )
    print(
        f"[WARN] Report saved to: {report_path}"
    )
    print("=" * 70)


def install_all_skills(
    entry_path: Path,
    global_install: bool = True,
) -> None:

    failed_skills: list[dict] = []

    for repository in SKILL_REPOSITORIES:
        failed_skills.extend(
            install_repository_skills(
                repository,
                global_install,
            )
        )

    impeccable_failure = install_impeccable()

    if impeccable_failure is not None:
        failed_skills.append(impeccable_failure)

    report_dir = entry_path.parent if global_install else Path.cwd()

    write_failed_skills_report(
        failed_skills,
        report_dir,
    )


def build_skills_check_command(
    global_install: bool = True,
) -> list[str]:

    command = ["npx", "skills", "check"]

    if global_install:
        command.append("--global")

    return command


def build_skills_update_command(
    global_install: bool = True,
) -> list[str]:

    command = ["npx", "skills", "update"]

    if global_install:
        command.append("--global")

    return command


def check_skills(
    global_install: bool = True,
) -> bool:
    """
    Verifica se ha skills instaladas (via "npx skills add") com
    atualizacao disponivel. Nao cobre "impeccable", que nao usa o
    CLI generico de skills.
    """

    print()
    print("=" * 70)
    print("Checking for skill updates")
    print("=" * 70)

    result = run_command(
        build_skills_check_command(global_install),
        capture=False,
    )

    return result.returncode == 0


def update_skills(
    global_install: bool = True,
) -> bool:
    """
    Atualiza as skills instaladas (via "npx skills add") para a
    versao mais recente. Nao cobre "impeccable"; rode
    "npx impeccable install" de novo manualmente para isso.
    """

    print()
    print("=" * 70)
    print("Updating skills")
    print("=" * 70)

    result = run_command(
        build_skills_update_command(global_install),
        capture=False,
    )

    return result.returncode == 0
