from __future__ import annotations

import datetime
from pathlib import Path

from thero.settings import SKILLS_FAILED_FILENAME
from thero.skills.catalog import EXISTING_SKILLS, SKILL_REPOSITORIES
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
            failed_skills.append(
                {
                    "group": repository["name"],
                    "repo": repo,
                    "skill": skill,
                }
            )

    print()
    print(
        f"[SUMMARY] {repo}: "
        f"{successful} installed, "
        f"{len(failed_skills)} unavailable/failed"
    )

    return failed_skills


def install_existing_skill_notice() -> None:

    print()
    print("=" * 70)
    print("Existing skills")
    print("=" * 70)

    for skill in EXISTING_SKILLS:
        print(
            f"[KEEP] {skill}"
        )

    print(
        "\nExisting skills are intentionally preserved."
    )


def write_failed_skills_report(
    failed_skills: list[dict],
    report_dir: Path,
    global_install: bool = True,
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

        command = " ".join(
            build_skill_install_command(
                item["repo"],
                item["skill"],
                global_install,
            )
        )

        lines.append(
            f"- [{item['group']}] repo={item['repo']} "
            f"skill={item['skill']}"
        )
        lines.append(
            f"  comando: {command}"
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

    install_existing_skill_notice()

    failed_skills: list[dict] = []

    for repository in SKILL_REPOSITORIES:
        failed_skills.extend(
            install_repository_skills(
                repository,
                global_install,
            )
        )

    report_dir = entry_path.parent if global_install else Path.cwd()

    write_failed_skills_report(
        failed_skills,
        report_dir,
        global_install,
    )
