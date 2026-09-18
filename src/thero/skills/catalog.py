# ------------------------------------------------------------
# Repositórios de skills
#
# Não usamos slugs fixos para tudo.
#
# O script tenta descobrir as skills disponíveis no repositório
# e instala apenas aquilo que estiver realmente disponível.
# ------------------------------------------------------------

SKILL_REPOSITORIES = [
    {
        "name": "Engineering / Reasoning",
        "repo": "darasoba/agent-skills",
        "wanted": [
            "fable-reasoning",
            "engineering-manager",
        ],
    },
    {
        "name": "Supabase",
        "repo": "supabase/agent-skills",
        "wanted": [
            "supabase",
            "supabase-postgres-best-practices",
        ],
    },
    {
        # "react-hooks", "accessibility" e "performance" nao existem
        # neste repo (confirmado rodando o install real e lendo a
        # lista de skills que o proprio CLI devolve no erro).
        # "feature-architecture" foi renomeada para "feature-arch".
        "name": "React / Frontend",
        "repo": "PyModel/react-frontend-skills",
        "wanted": [
            "react",
            "nextjs",
            "typescript",
            "tailwind",
            "shadcn",
            "ui-design",
            "feature-arch",
            "vercel-react-best-practices",
            "react-hook-form",
            "zod",
            "tanstack-query",
            "vitest",
            "playwright",
            "msw",
            "tdd",
        ],
    },
    {
        # Repo migrou pra nomes prefixados por categoria (confirmado
        # rodando o install real). "python" e "testing" genericos nao
        # tem equivalente direto neste repo — removidos.
        "name": "Agents Inc",
        "repo": "agents-inc/skills",
        "wanted": [
            "shared-tooling-typescript-config",
            "web-framework-react",
            "web-meta-framework-nextjs",
            "api-baas-firebase",
            "api-commerce-stripe",
            "api-baas-supabase",
            "web-styling-tailwind",
            "web-ui-mui",
            "shared-security-auth-security",
            "meta-reviewing-reviewing",
            "web-performance-web-performance",
            "web-accessibility-web-accessibility",
        ],
    },
    {
        "name": "Caveman",
        "repo": "JuliusBrussee/caveman",
        "wanted": [
            "caveman",
        ],
    },
]
