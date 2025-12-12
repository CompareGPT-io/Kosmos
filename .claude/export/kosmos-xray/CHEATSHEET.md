# Kosmos X-Ray Cheatsheet

Quick reference for context-efficient codebase exploration.

## Quick Start (Full Feature Usage)

```bash
# 1. Survey codebase
python .claude/skills/kosmos-xray/scripts/mapper.py --summary

# 2. Extract critical interfaces (with Pydantic fields + line numbers)
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/ --priority critical

# 3. Generate architecture diagram
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --root kosmos --mermaid

# 4. Verify imports work
python3 -c "from kosmos.workflow import ResearchWorkflow; print('✓')"
```

## Commands

### mapper.py
```bash
mapper.py [dir]              # Full tree with token counts
mapper.py --summary          # Summary only (RECOMMENDED START)
mapper.py --json             # Machine-readable output
```

### skeleton.py (Enhanced)
```bash
skeleton.py <file>           # Single file with line numbers
skeleton.py <dir>            # All .py files
skeleton.py --priority critical  # Core architecture (USE THIS)
skeleton.py --priority high      # Domain logic
skeleton.py --pattern "*.py"     # Pattern filter
skeleton.py --private            # Include _private methods
skeleton.py --no-line-numbers    # Omit L{n} references
skeleton.py --json               # JSON output
```

### dependency_graph.py
```bash
dependency_graph.py [dir]        # Text output
dependency_graph.py --root kosmos    # With package name
dependency_graph.py --focus workflow # Focus on area
dependency_graph.py --mermaid        # Mermaid diagram (USE FOR DOCS)
dependency_graph.py --mermaid --focus workflow  # Combined
dependency_graph.py --json           # JSON output
```

## Enhanced Features (v2)

| Feature | What It Shows | Example |
|---------|---------------|---------|
| Pydantic fields | Class attributes | `name: str = Field(...)  # L51` |
| Decorators | `@dataclass`, `@property` | `@dataclass` above class |
| Global constants | Module-level vars | `CONFIG = "value"  # L17` |
| Line numbers | Code location | `def method(): ...  # L42` |
| Mermaid diagrams | Visual architecture | `graph TD ...` |

## Priority Levels

| Level | What | When |
|-------|------|------|
| **critical** | Orchestration, workflows | Understand system flow FIRST |
| **high** | Domain logic, data models | Deep feature work |
| **medium** | Infrastructure, validation | Supporting changes |
| **low** | Utils, tests, CLI | Only when needed |

## What Skeleton Reveals Now

**Before (data blind):**
```python
class Hypothesis(BaseModel):
    pass  # Fields invisible!
```

**After (enhanced):**
```python
class Hypothesis(BaseModel):  # L32
    id: Optional[str] = None  # L50
    research_question: str = Field(...)  # L51
    statement: str = Field(...)  # L52
    status: HypothesisStatus  # L56
```

## Context Hazards (DO NOT READ)

```
artifacts/           # Runtime outputs
data/                # Test datasets
.literature_cache/   # PDF caches
kosmos-reference/    # Reference PDFs
logs/                # Execution logs
*.jsonl, *.pkl       # Large data files
```

## Token Budget Reference

| Operation | Tokens | When to Use |
|-----------|--------|-------------|
| mapper.py --summary | ~500 | Always first |
| skeleton.py (1 file) | ~200-500 | Single interface |
| skeleton.py --priority critical | ~5K | Core onboarding |
| dependency_graph.py text | ~2-3K | Architecture |
| dependency_graph.py --mermaid | ~500 | Documentation |

## Full Exploration Path

```bash
# Step 1: Survey (500 tokens)
python .claude/skills/kosmos-xray/scripts/mapper.py --summary

# Step 2: Critical interfaces with fields (5K tokens)
python .claude/skills/kosmos-xray/scripts/skeleton.py kosmos/ --priority critical

# Step 3: Architecture diagram (500 tokens)
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --root kosmos --mermaid

# Step 4: Workflow-focused diagram (500 tokens)
python .claude/skills/kosmos-xray/scripts/dependency_graph.py kosmos/ --root kosmos --mermaid --focus workflow

# Step 5: Verify imports
python3 -c "from kosmos.workflow import ResearchWorkflow; print('✓')"
python3 -c "from kosmos.agents.base import BaseAgent; print('✓')"

# Total: ~6.5K tokens for complete architecture understanding
```

## Using with Agent

```
@kosmos_architect generate    # Create WARM_START.md (uses ALL features)
@kosmos_architect refresh     # Update existing doc
@kosmos_architect query "X"   # Answer specific question
```
