from thero.settings import COMMAND_MARKER_END, COMMAND_MARKER_START

GLOBAL_COMMAND_TEMPLATE = r"""# >>> setup_claude global command >>>
# Gerado automaticamente por thero.py --install-command
# Nao edite manualmente entre estes marcadores; rode novamente
# "python thero.py --install-command" para atualizar.
function %s {
    param(
        [Parameter(Position = 0)]
        [string]$Command,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Rest
    )

    $scriptPath = '%s'

    $flagMap = @{
        'install'    = @()
        'skills'     = @('--skills-only')
        'merge'      = @('--merge-only')
        'audit'      = @('--audit')
        'audit-only' = @('--audit-only')
        'help'       = @('--help')
    }

    if ([string]::IsNullOrEmpty($Command)) {
        $flags = @()
    }
    elseif ($flagMap.ContainsKey($Command)) {
        $flags = $flagMap[$Command]
    }
    else {
        # Argumento desconhecido: repassa cru para o script
        # (ex.: --skills-only, -h).
        $flags = @($Command) + $Rest
        $Rest = @()
    }

    python $scriptPath @flags @Rest
}
# <<< setup_claude global command <<<
"""

LOCAL_COMMAND_TEMPLATE = r"""# Comando local do projeto: %(project_dir)s
# Gerado automaticamente por thero.py --install-command --local
# Nao versione segredos aqui; este arquivo so referencia caminhos
# locais da sua maquina. Carregue nesta sessao com:
#     . .\%(local_filename)s
function %(command_name)s {
    param(
        [Parameter(Position = 0)]
        [string]$Command,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Rest
    )

    $projectDir = '%(project_dir)s'
    $currentDir = (Get-Location).Path

    if (
        $currentDir -ne $projectDir -and
        -not $currentDir.StartsWith("$projectDir\")
    ) {
        Write-Error (
            "'%(command_name)s' e um comando local do projeto " +
            "'$projectDir'. Rode a partir dessa pasta (ou de " +
            "uma subpasta dela)."
        )
        return
    }

    $scriptPath = '%(script_path)s'

    $flagMap = @{
        'install'    = @()
        'skills'     = @('--skills-only')
        'merge'      = @('--merge-only')
        'audit'      = @('--audit')
        'audit-only' = @('--audit-only')
        'help'       = @('--help')
    }

    if ([string]::IsNullOrEmpty($Command)) {
        $flags = @()
    }
    elseif ($flagMap.ContainsKey($Command)) {
        $flags = $flagMap[$Command]
    }
    else {
        # Argumento desconhecido: repassa cru para o script
        # (ex.: --skills-only, -h).
        $flags = @($Command) + $Rest
        $Rest = @()
    }

    python $scriptPath --local @flags @Rest
}

Write-Host (
    "[OK] Comando local '%(command_name)s' carregado " +
    "(valido em '%(project_dir)s')."
)
"""

assert GLOBAL_COMMAND_TEMPLATE.startswith(COMMAND_MARKER_START)
assert COMMAND_MARKER_END in GLOBAL_COMMAND_TEMPLATE
