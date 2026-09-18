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
        "name": "React / Frontend",
        "repo": "PyModel/react-frontend-skills",
        "wanted": [
            "react",
            "react-hooks",
            "nextjs",
            "typescript",
            "tailwind",
            "shadcn",
            "ui-design",
            "accessibility",
            "performance",
            "feature-architecture",
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
        "name": "Agents Inc",
        "repo": "agents-inc/skills",
        "wanted": [
            "typescript",
            "react",
            "nextjs",
            "python",
            "firebase",
            "stripe",
            "supabase",
            "tailwind",
            "mui",
            "testing",
            "security",
            "code-review",
            "performance",
            "accessibility",
        ],
    },
]


# ------------------------------------------------------------
# Skills que o usuário já utiliza.
#
# NÃO removemos nem substituímos.
#
# O skills CLI normalmente mantém skills existentes.
# ------------------------------------------------------------

EXISTING_SKILLS = [
    "caveman",
    "impeccable",
]
