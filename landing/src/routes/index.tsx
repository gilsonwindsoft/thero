import { createFileRoute } from "@tanstack/react-router";
import {
  ArrowDown,
  ArrowRight,
  Check,
  ChevronRight,
  CircleCheck,
  Clock3,
  Code2,
  Copy,
  ExternalLink,
  FileCode2,
  Github,
  Linkedin,
  Menu,
  Network,
  ShieldCheck,
  Sparkles,
  Terminal,
  X,
  Zap,
} from "lucide-react";
import { useState } from "react";

import profileAssetUrl from "../assets/anthero-profile.jpg";
import theroMark from "../assets/thero-mark.png";
import systemImage from "../assets/thero-system.jpg";

const GITHUB = "https://github.com/netovieira/thero";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Thero — Claude Code pronto para trabalho sério" },
      {
        name: "description",
        content:
          "Configure o Claude Code com regras profissionais, skills sob demanda, contexto de arquitetura com Athena e planejamento com Zeus.",
      },
      { property: "og:title", content: "Thero — menos contexto perdido, mais código certo" },
      {
        property: "og:description",
        content: "Uma suíte open-source para preparar, contextualizar e planejar seu trabalho com Claude Code.",
      },
      { property: "og:type", content: "website" },
      { property: "og:url", content: "https://netovieira.github.io/thero/" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [{ rel: "canonical", href: "https://netovieira.github.io/thero/" }],
  }),
  component: Index,
});

const skills = [
  ["Caveman", "Respostas comprimidas por padrão"],
  ["Impeccable", "Qualidade visual e revisão de interface"],
  ["React + Next.js", "Arquitetura e práticas modernas"],
  ["TypeScript", "Tipos seguros no trabalho diário"],
  ["Tailwind + shadcn", "Sistemas de interface consistentes"],
  ["TanStack Query", "Estado assíncrono bem estruturado"],
  ["Vitest + Playwright", "Testes de unidade e ponta a ponta"],
  ["Supabase", "Banco, segurança e boas práticas"],
  ["Firebase + Stripe", "Integrações de produto"],
  ["Acessibilidade", "Experiências que incluem mais pessoas"],
  ["Performance web", "Software rápido e mensurável"],
  ["Code review", "Revisão técnica antes da entrega"],
];

function CopyCommand({ command, compact = false }: { command: string; compact?: boolean }) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    await navigator.clipboard.writeText(command);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  };

  return (
    <div className={`command ${compact ? "command-compact" : ""}`}>
      <code><span>$</span> {command}</code>
      <button type="button" onClick={copy} aria-label="Copiar comando" title="Copiar comando">
        {copied ? <Check size={17} /> : <Copy size={17} />}
      </button>
    </div>
  );
}

function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="site-header">
      <a href="#top" className="brand" aria-label="Thero, início">
        <img src={theroMark} alt="" width={40} height={40} />
        <span>thero</span>
      </a>
      <nav className="desktop-nav" aria-label="Navegação principal">
        <a href="#suite">A suíte</a>
        <a href="#skills">Skills</a>
        <a href="#comparativo">Comparativo</a>
        <a href="#autor">Autor</a>
      </nav>
      <a className="header-cta" href={GITHUB} target="_blank" rel="noreferrer">
        <Github size={17} /> GitHub <ExternalLink size={13} />
      </a>
      <button className="menu-button" type="button" onClick={() => setOpen(!open)} aria-label={open ? "Fechar menu" : "Abrir menu"}>
        {open ? <X /> : <Menu />}
      </button>
      {open && (
        <nav className="mobile-nav" aria-label="Navegação móvel">
          <a href="#suite" onClick={() => setOpen(false)}>A suíte</a>
          <a href="#skills" onClick={() => setOpen(false)}>Skills</a>
          <a href="#comparativo" onClick={() => setOpen(false)}>Comparativo</a>
          <a href="#autor" onClick={() => setOpen(false)}>Autor</a>
          <a href={GITHUB} target="_blank" rel="noreferrer">Abrir no GitHub</a>
        </nav>
      )}
    </header>
  );
}

function Index() {
  return (
    <main id="top">
      <Header />

      <section className="hero shell">
        <div className="hero-copy">
          <div className="eyebrow"><span /> Open source · Python 3.10+ · MIT</div>
          <h1>Seu Claude Code.<br /><em>Pronto para trabalho sério.</em></h1>
          <p className="hero-lede">
            Pare de reexplicar regras, reler o projeto inteiro e corrigir trabalho fora de contexto. O Thero prepara seu Claude como se um time sênior tivesse revisado o ambiente antes da primeira mensagem.
          </p>
          <div className="hero-actions">
            <a className="button button-primary" href="#instalar">Instalar o Thero <ArrowDown size={18} /></a>
            <a className="button button-secondary" href={GITHUB} target="_blank" rel="noreferrer"><Github size={18} /> Ver código</a>
          </div>
          <div className="hero-proof">
            <span><CircleCheck size={16} /> Zero dependências Python</span>
            <span><CircleCheck size={16} /> Backup antes de mudar</span>
            <span><CircleCheck size={16} /> Global ou por projeto</span>
          </div>
        </div>

        <div className="hero-visual" aria-label="Demonstração do fluxo Thero, Athena e Zeus">
          <div className="terminal-window">
            <div className="terminal-bar"><i /><i /><i /><span>~/seu-projeto — thero</span></div>
            <div className="terminal-body">
              <p><b>$</b> python thero.py</p>
              <p className="muted">Preparando Claude Code...</p>
              <p><strong>✓</strong> Engineering Operating System</p>
              <p><strong>✓</strong> Agent Skills sob demanda</p>
              <p><strong>✓</strong> CLAUDE.md consolidado</p>
              <div className="terminal-divider" />
              <p><b>$</b> thero index</p>
              <p><span className="athena-dot">●</span> Athena mapeou a arquitetura</p>
              <p><b>$</b> thero --plan "implementar auth"</p>
              <p><span className="zeus-dot">●</span> Zeus criou o plano de execução</p>
              <p className="ready">Pronto. Contexto antes de código. <span className="cursor" /></p>
            </div>
          </div>
          <div className="floating-chip chip-one"><Network size={15} /> contexto persistente</div>
          <div className="floating-chip chip-two"><ShieldCheck size={15} /> mudanças verificáveis</div>
        </div>
      </section>

      <section className="trust-strip" aria-label="Benefícios principais">
        <div className="shell trust-grid">
          <div><strong>1 comando</strong><span>para preparar o ambiente</span></div>
          <div><strong>3 ferramentas</strong><span>do contexto à execução</span></div>
          <div><strong>Skills sob demanda</strong><span>só quando a tarefa precisa</span></div>
          <div><strong>Sem lock-in</strong><span>arquivos abertos no seu projeto</span></div>
        </div>
      </section>

      <section className="problem-section shell">
        <div className="section-kicker">O problema não é o Claude</div>
        <div className="problem-heading">
          <h2>É tudo que ele precisa<br />adivinhar antes de começar.</h2>
          <p>Um modelo poderoso sem contexto de projeto, critérios de qualidade e especialidades certas ainda pode tomar o caminho mais longo.</p>
        </div>
        <div className="before-after">
          <article className="pain-column">
            <span className="state-label">Sem Thero</span>
            <ul>
              <li><X size={16} /> Você repete as mesmas regras em toda sessão</li>
              <li><X size={16} /> O projeto é relido sem memória de arquitetura</li>
              <li><X size={16} /> A implementação começa antes do plano</li>
              <li><X size={16} /> Correções viram novas rodadas de contexto</li>
            </ul>
          </article>
          <div className="transformation-arrow"><ArrowRight /></div>
          <article className="gain-column">
            <span className="state-label">Com a suíte Thero</span>
            <ul>
              <li><Check size={16} /> Regras profissionais desde a primeira mensagem</li>
              <li><Check size={16} /> Contexto da arquitetura já disponível</li>
              <li><Check size={16} /> Skills ativadas somente quando necessárias</li>
              <li><Check size={16} /> Plano ancorado nos arquivos reais do projeto</li>
            </ul>
          </article>
        </div>
      </section>

      <section id="suite" className="suite-section">
        <div className="shell">
          <div className="section-head light">
            <div><span className="section-kicker">Uma suíte. Três responsabilidades.</span><h2>Prepare. Entenda. Planeje.</h2></div>
            <p>Use cada ferramenta sozinha ou conecte as três em um fluxo que reduz suposições antes de tocar no código.</p>
          </div>
          <div className="suite-flow">
            <article className="suite-item thero-item">
              <div className="suite-number">01</div>
              <div className="suite-icon"><img src={theroMark} alt="" width={52} height={52} /></div>
              <div className="suite-copy"><span>Prepare</span><h3>Thero</h3><p>Instala skills, consolida suas regras, preserva configurações existentes, cria backups e audita sem alterar código.</p></div>
              <a href={GITHUB} target="_blank" rel="noreferrer">Conhecer o Thero <ArrowRight size={16} /></a>
            </article>
            <article className="suite-item athena-item">
              <div className="suite-number">02</div>
              <div className="suite-icon"><Network /></div>
              <div className="suite-copy"><span>Entenda</span><h3>Athena</h3><p>Transforma o repositório em uma planta baixa: resumos de arquivos e pastas, de baixo para cima, com cache incremental por hash.</p></div>
              <a href="https://github.com/netovieira/athena" target="_blank" rel="noreferrer">Conhecer a Athena <ArrowRight size={16} /></a>
            </article>
            <article className="suite-item zeus-item">
              <div className="suite-number">03</div>
              <div className="suite-icon"><Zap /></div>
              <div className="suite-copy"><span>Planeje</span><h3>Zeus</h3><p>Cruza sua tarefa com o índice da Athena, identifica arquivos relevantes, riscos e passos antes de pedir a execução.</p></div>
              <a href="https://github.com/netovieira/zeus" target="_blank" rel="noreferrer">Conhecer o Zeus <ArrowRight size={16} /></a>
            </article>
          </div>
          <div className="system-image-wrap">
            <img src={systemImage} alt="Representação abstrata do código sendo condensado em contexto e transformado em plano" width={1600} height={1008} loading="lazy" />
            <div className="system-caption"><span>código real</span><ChevronRight /><span>contexto indexado</span><ChevronRight /><span>plano verificável</span></div>
          </div>
        </div>
      </section>

      <section id="comparativo" className="comparison-section shell">
        <div className="section-head">
          <div><span className="section-kicker">Menos desperdício por design</span><h2>O ganho vem do processo,<br />não de uma promessa mágica.</h2></div>
          <p>Caveman reduz verbosidade. Athena evita releituras desnecessárias. Zeus antecipa decisões. Juntos, atacam fontes reais de desperdício.</p>
        </div>
        <div className="scenario-note"><Sparkles size={15} /> Cenário ilustrativo — os números abaixo demonstram o mecanismo, não um benchmark universal.</div>
        <div className="comparison-grid">
          <div className="comparison-card without">
            <div className="comparison-title"><span>Uma tarefa sem a suíte</span><small>fluxo reativo</small></div>
            <div className="metric"><div><span>Contexto reenviado</span><strong>48k</strong><small>tokens ilustrativos</small></div><div className="meter"><i style={{ width: "88%" }} /></div></div>
            <div className="metric"><div><span>Rodadas até acertar</span><strong>4</strong><small>tentativas</small></div><div className="meter"><i style={{ width: "72%" }} /></div></div>
            <div className="timeline"><Clock3 /><span>ler → tentar → corrigir → reler → ajustar</span></div>
          </div>
          <div className="comparison-card with">
            <div className="comparison-title"><span>A mesma tarefa com Thero</span><small>fluxo orientado</small></div>
            <div className="metric"><div><span>Contexto enviado</span><strong>17k</strong><small>tokens ilustrativos</small></div><div className="meter"><i style={{ width: "31%" }} /></div></div>
            <div className="metric"><div><span>Rodadas até acertar</span><strong>1</strong><small>tentativa</small></div><div className="meter"><i style={{ width: "18%" }} /></div></div>
            <div className="timeline"><Zap /><span>indexar → planejar → executar → verificar</span></div>
          </div>
        </div>
        <div className="mechanism-row">
          <div><Code2 /><strong>Caveman</strong><span>respostas compactas por padrão</span></div>
          <div><Network /><strong>Athena</strong><span>reutiliza o mapa do projeto</span></div>
          <div><FileCode2 /><strong>Zeus</strong><span>define o caminho antes do código</span></div>
        </div>
      </section>

      <section id="skills" className="skills-section">
        <div className="shell skills-layout">
          <div className="skills-copy">
            <span className="section-kicker">Especialistas quando você precisa</span>
            <h2>Skills para o trabalho que chega de verdade.</h2>
            <p>Em vez de colocar um manual inteiro em toda conversa, o Thero instala conhecimento especializado que o Claude carrega quando reconhece a tarefa.</p>
            <div className="context-rule"><Terminal /><div><strong>Contexto enxuto</strong><span>Comportamento no CLAUDE.md. Conhecimento nas skills.</span></div></div>
          </div>
          <div className="skills-list">
            {skills.map(([name, description]) => (
              <div className="skill-row" key={name}><span className="skill-check"><Check size={14} /></span><div><strong>{name}</strong><span>{description}</span></div></div>
            ))}
          </div>
        </div>
      </section>

      <section id="instalar" className="install-section shell">
        <div className="install-grid">
          <div>
            <span className="section-kicker">Comece em minutos</span>
            <h2>Um comando hoje.<br />Menos explicações amanhã.</h2>
            <p>Clone o projeto, rode o script e reinicie o Claude Code. O Thero cuida do restante sem apagar o que você já configurou.</p>
            <div className="requirements"><span><Check /> Python 3.10+</span><span><Check /> Node.js + npx</span><span><Check /> Claude Code autenticado</span></div>
          </div>
          <div className="install-terminal">
            <div className="terminal-bar"><i /><i /><i /><span>instalação</span></div>
            <div className="install-commands">
              <CopyCommand command="git clone https://github.com/netovieira/thero.git" compact />
              <CopyCommand command="cd thero" compact />
              <CopyCommand command="python thero.py" compact />
            </div>
            <div className="install-result"><CircleCheck /> Skills instaladas · CLAUDE.md consolidado · comando thero pronto</div>
          </div>
        </div>
        <div className="mode-grid">
          <div><code>thero audit-only</code><span>Audite sem modificar o código</span></div>
          <div><code>thero index</code><span>Mapeie o projeto com Athena</span></div>
          <div><code>thero --plan "tarefa"</code><span>Planeje com Zeus</span></div>
          <div><code>thero --local</code><span>Mantenha tudo dentro do projeto</span></div>
        </div>
      </section>

      <section id="autor" className="author-section">
        <div className="shell author-grid">
          <div className="author-photo-wrap"><img src={profileAssetUrl} alt="Anthero Vieira Neto" width={200} height={200} loading="lazy" /><span>18 anos<br />construindo<br />software</span></div>
          <div className="author-copy">
            <span className="section-kicker">Código nascido de experiência real</span>
            <h2>Construído por quem já viveu o problema.</h2>
            <p className="author-lede">Sou <strong>Anthero Vieira Neto</strong>, arquiteto de software sênior e DevOps Engineer. Trabalho com TypeScript, Python, Kubernetes e IA aplicada a produtos reais — do código à cultura de entrega.</p>
            <p>O Thero, a Athena e o Zeus nasceram de uma necessidade recorrente: dar contexto confiável à IA sem desperdiçar tempo, tokens ou a experiência acumulada por um time. Esta suíte transforma esse aprendizado em ferramentas abertas para qualquer developer.</p>
            <div className="author-links">
              <a href="https://www.linkedin.com/in/anthero-vieira-neto-aa7a6b8a" target="_blank" rel="noreferrer"><Linkedin size={18} /> LinkedIn <ExternalLink size={13} /></a>
              <a href="https://github.com/netovieira" target="_blank" rel="noreferrer"><Github size={18} /> GitHub <ExternalLink size={13} /></a>
            </div>
          </div>
        </div>
      </section>

      <section className="final-cta">
        <div className="shell final-inner">
          <img src={theroMark} alt="" width={72} height={72} loading="lazy" />
          <span className="section-kicker">Seu Claude já é poderoso</span>
          <h2>Dê a ele contexto,<br />especialistas e um plano.</h2>
          <p>Open source, transparente e pronto para seu próximo projeto.</p>
          <div className="hero-actions">
            <a className="button button-primary" href={GITHUB} target="_blank" rel="noreferrer"><Github size={18} /> Começar no GitHub</a>
            <a className="button button-dark-outline" href="https://github.com/netovieira/thero/blob/master/README.md" target="_blank" rel="noreferrer">Ler documentação <ArrowRight size={17} /></a>
          </div>
        </div>
      </section>

      <footer>
        <div className="shell footer-inner">
          <a href="#top" className="brand"><img src={theroMark} alt="" width={36} height={36} loading="lazy" /><span>thero</span></a>
          <p>Claude Code pronto para trabalho sério.</p>
          <div><a href="https://github.com/netovieira/athena" target="_blank" rel="noreferrer">Athena</a><a href="https://github.com/netovieira/zeus" target="_blank" rel="noreferrer">Zeus</a><a href="https://github.com/netovieira/thero/blob/master/LICENSE" target="_blank" rel="noreferrer">MIT License</a></div>
          <small>© 2026 Anthero Vieira Neto</small>
        </div>
      </footer>
    </main>
  );
}