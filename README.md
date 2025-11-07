# Kosmos AI Scientist

> **Fully autonomous AI scientist powered by Claude for hypothesis generation, experimental design, and iterative scientific discovery**

Kosmos is an open-source implementation of an autonomous AI scientist that can conduct complete research cycles: from literature analysis and hypothesis generation through experimental design, execution, analysis, and iterative refinement.

## Features

- **Autonomous Research Cycle**: Complete end-to-end scientific workflow
- **Multi-Domain Support**: Biology, physics, chemistry, neuroscience, materials science
- **Claude-Powered Intelligence**: Uses Claude Sonnet 4 for hypothesis generation and analysis
- **Flexible Integration**: Supports both Anthropic API and Claude Code CLI
- **Proven Analysis Patterns**: Integrates battle-tested statistical methods from kosmos-figures
- **Literature Integration**: Automated paper search, summarization, and novelty checking
- **Agent-Based Architecture**: Modular agents for each research task
- **Safety-First Design**: Sandboxed execution, validation, reproducibility checks

## Quick Start

### Prerequisites

- Python 3.11 or 3.12
- One of the following:
  - **Option A**: Anthropic API key (pay-per-use)
  - **Option B**: Claude Code CLI installed (Max subscription)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/kosmos-ai-scientist.git
cd kosmos-ai-scientist

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# For Claude Code CLI support (Option B)
pip install -e ".[router]"
```

### Configuration

#### Option A: Using Anthropic API

```bash
# Copy example config
cp .env.example .env

# Edit .env and set your API key
# ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

Get your API key from [console.anthropic.com](https://console.anthropic.com/)

#### Option B: Using Claude Code CLI (Recommended)

```bash
# 1. Install Claude Code CLI
# Follow instructions at https://claude.ai/download

# 2. Authenticate Claude CLI
claude auth

# 3. Copy example config
cp .env.example .env

# 4. Edit .env and set API key to all 9s (triggers CLI routing)
# ANTHROPIC_API_KEY=999999999999999999999999999999999999999999999999
```

This routes all API calls to your local Claude Code CLI, using your Max subscription with no per-token costs.

### Initialize Database

```bash
# Run database migrations
alembic upgrade head

# Verify database created
ls -la kosmos.db
```

### Run Your First Research Project

```python
from kosmos import ResearchDirector

# Initialize the research director
director = ResearchDirector()

# Pose a research question
question = "What is the relationship between sleep deprivation and memory consolidation?"

# Run autonomous research
results = director.conduct_research(
    question=question,
    domain="neuroscience",
    max_iterations=5
)

# View results
print(results.summary)
print(results.key_findings)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Research Director                        │
│          (Orchestrates autonomous research cycle)            │
└──────────────┬──────────────────────────────────────────────┘
               │
    ┌──────────┴──────────┬───────────────┬──────────────┐
    │                     │               │              │
┌───▼────┐    ┌──────────▼──────────┐   ┌▼──────────┐ ┌▼─────────────┐
│Literature│   │Hypothesis Generator│   │Experiment │ │Data Analyst  │
│Analyzer  │   │    (Claude)         │   │Designer   │ │  (Claude)    │
└───┬────┘    └──────────┬──────────┘   └┬──────────┘ └┬─────────────┘
    │                     │               │              │
    └─────────────────────┴───────────────┴──────────────┘
                          │
                ┌─────────▼──────────┐
                │  Execution Engine  │
                │ (kosmos-figures    │
                │  proven patterns)  │
                └────────────────────┘
```

### Core Components

- **Research Director**: Master orchestrator managing research workflow
- **Literature Analyzer**: Searches and analyzes scientific papers (arXiv, Semantic Scholar, PubMed)
- **Hypothesis Generator**: Uses Claude to generate testable hypotheses
- **Experiment Designer**: Designs computational experiments
- **Execution Engine**: Runs experiments using proven statistical methods
- **Data Analyst**: Interprets results using Claude
- **Feedback Loop**: Iteratively refines hypotheses based on results

## Usage Modes

### Mode 1: Claude Code CLI (Max Subscription)

**Pros:**
- No per-token costs
- Unlimited usage
- Latest Claude model
- Local execution

**Cons:**
- Requires Claude CLI installation
- Requires Max subscription

**Setup:**
```bash
pip install -e ".[router]"
# Set ANTHROPIC_API_KEY=999999999999999999999999999999999999999999999999
```

### Mode 2: Anthropic API

**Pros:**
- Pay-as-you-go
- No CLI installation needed
- Works anywhere

**Cons:**
- Per-token costs
- Rate limits apply

**Setup:**
```bash
# Set ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

## Configuration

All configuration is via environment variables (see `.env.example`):

### Core Settings
- `ANTHROPIC_API_KEY`: API key or `999...` for CLI mode
- `CLAUDE_MODEL`: Model to use (API mode only)
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging verbosity

### Research Settings
- `MAX_RESEARCH_ITERATIONS`: Max autonomous iterations
- `ENABLED_DOMAINS`: Which scientific domains to support
- `ENABLED_EXPERIMENT_TYPES`: Types of experiments allowed
- `MIN_NOVELTY_SCORE`: Minimum novelty threshold

### Safety Settings
- `ENABLE_SAFETY_CHECKS`: Code safety validation
- `MAX_EXPERIMENT_EXECUTION_TIME`: Timeout for experiments
- `ENABLE_SANDBOXING`: Sandbox code execution
- `REQUIRE_HUMAN_APPROVAL`: Manual approval gates

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=kosmos --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

### Code Quality

```bash
# Format code
black kosmos/ tests/

# Lint
ruff check kosmos/ tests/

# Type check
mypy kosmos/
```

### Project Structure

```
kosmos/
├── core/           # Core infrastructure (LLM, config, logging)
├── agents/         # Agent implementations
├── db/             # Database models and operations
├── execution/      # Experiment execution engine
├── analysis/       # Result analysis and visualization
├── hypothesis/     # Hypothesis generation and management
├── experiments/    # Experiment templates
├── literature/     # Literature search and analysis
├── knowledge/      # Knowledge graph and semantic search
├── domains/        # Domain-specific tools (biology, physics, etc.)
├── safety/         # Safety checks and validation
└── cli/            # Command-line interface

tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/            # End-to-end tests

docs/
├── kosmos-figures-analysis.md  # Analysis patterns from kosmos-figures
├── integration-plan.md         # Integration strategy
└── domain-roadmaps/            # Domain-specific guides
```

## Documentation

- [Architecture Overview](docs/architecture.md) - System design and components
- [Integration Plan](docs/integration-plan.md) - How we integrate kosmos-figures patterns
- [Domain Roadmaps](docs/domain-roadmaps/) - Domain-specific implementation guides
- [API Reference](docs/api/) - API documentation
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## Roadmap

### Phase 1: Core Infrastructure (Current)
- [x] Project structure
- [x] Claude integration (API + CLI)
- [ ] Configuration system
- [ ] Agent framework
- [ ] Database setup

### Phase 2: Knowledge & Literature
- [ ] Literature APIs (arXiv, Semantic Scholar, PubMed)
- [ ] Literature analyzer agent
- [ ] Vector database for semantic search
- [ ] Knowledge graph

### Phase 3: Hypothesis Generation
- [ ] Hypothesis generator agent
- [ ] Novelty checking
- [ ] Hypothesis prioritization

### Phase 4: Experimental Design
- [ ] Experiment designer agent
- [ ] Protocol templates
- [ ] Resource estimation

### Phase 5: Execution
- [ ] Sandboxed execution environment
- [ ] Integration of kosmos-figures patterns
- [ ] Statistical analysis

### Phase 6: Analysis & Interpretation
- [ ] Data analyst agent
- [ ] Visualization generation
- [ ] Result summarization

### Phase 7: Iterative Learning
- [ ] Research director agent
- [ ] Feedback loops
- [ ] Convergence detection

### Phases 8-10: Safety, Multi-Domain, Production
- [ ] Safety validation
- [ ] Domain-specific tools
- [ ] Production deployment

## Based On

This project is inspired by:
- **Paper**: [Kosmos: An AI Scientist for Autonomous Discovery](https://arxiv.org/pdf/2511.02824) (Nov 2025)
- **Analysis Patterns**: [kosmos-figures repository](https://github.com/EdisonScientific/kosmos-figures)
- **Claude Router**: [claude_n_codex_api_proxy](https://github.com/jimmc414/claude_n_codex_api_proxy)

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas We Need Help

- Domain-specific tools and APIs
- Experiment templates for different domains
- Literature API integrations
- Safety validation
- Documentation
- Testing

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use Kosmos in your research, please cite:

```bibtex
@software{kosmos_ai_scientist,
  title={Kosmos AI Scientist: Autonomous Scientific Discovery with Claude},
  author={Kosmos Contributors},
  year={2025},
  url={https://github.com/your-org/kosmos-ai-scientist}
}
```

## Acknowledgments

- **Anthropic** for Claude and Claude Code
- **Edison Scientific** for kosmos-figures analysis patterns
- **Open science community** for literature APIs and tools

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/kosmos-ai-scientist/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/kosmos-ai-scientist/discussions)
- **Discord**: [Join our community](https://discord.gg/your-invite)

---

**Status**: Alpha - Under active development (Phase 1)

**Last Updated**: 2025-11-07
