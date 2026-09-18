def discover_repo_skills(
    repo: str,
) -> set[str]:

    """
    Tenta descobrir os nomes das skills disponíveis.

    Não depende exclusivamente de uma implementação específica
    do CLI.

    Estratégia:

    1. tenta `npx skills add` apenas para repositórios onde
       sabemos que a instalação global é suportada;
    2. se o CLI não expuser discovery facilmente, retorna
       conjunto vazio e o instalador pode tentar os nomes
       desejados individualmente.

    O objetivo principal aqui é evitar quebrar todo o processo
    porque uma skill individual deixou de existir.
    """

    # O skills CLI possui diferentes versões com comandos de
    # discovery diferentes. Não assumimos uma API específica.
    #
    # Retornamos vazio para usar instalação individual segura.

    return set()
