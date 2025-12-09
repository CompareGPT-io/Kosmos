# Resume Prompt - Post Compaction

## Context

You are resuming work on the Kosmos project after a context compaction. The previous sessions implemented **15 paper implementation gaps** (3 BLOCKER + 5 Critical + 5 High + 2 Medium).

## What Was Done

### All Fixed Issues

| Issue | Description | Implementation |
|-------|-------------|----------------|
| #66 | CLI Deadlock | Full async refactor of message passing |
| #67 | SkillLoader | Domain-to-bundle mapping fixed |
| #68 | Pydantic V2 | Model config migration complete |
| #54 | Self-Correcting Code Execution | Enhanced RetryStrategy with 11 error handlers + LLM repair |
| #55 | World Model Update Categories | UpdateType enum (CONFIRMATION/CONFLICT/PRUNING) + conflict detection |
| #56 | 12-Hour Runtime Constraint | `max_runtime_hours` config + runtime tracking in ResearchDirector |
| #57 | Parallel Task Execution | Changed `max_concurrent_experiments` default from 4 to 10 |
| #58 | Agent Rollout Tracking | New RolloutTracker class + integration in ResearchDirector |
| #59 | h5ad/Parquet Data Formats | `DataLoader.load_h5ad()` and `load_parquet()` methods |
| #69 | R Language Execution | `RExecutor` class + Docker image with TwoSampleMR |
| #60 | Figure Generation | `FigureManager` class + code template integration |
| #61 | Jupyter Notebook Generation | `NotebookGenerator` class + nbformat integration |
| #70 | Null Model Statistical Validation | `NullModelValidator` class + ScholarEval integration |
| #63 | Failure Mode Detection | `FailureDetector` class (over-interp, invented metrics, rabbit hole) |
| #62 | Code Line Provenance | `CodeProvenance` class + hyperlinks to notebook cells |

### Key Files Created/Modified (Recent)

| File | Changes |
|------|---------|
| `kosmos/execution/provenance.py` | **NEW** - CodeProvenance, CellLineMapping (~280 lines) |
| `kosmos/execution/__init__.py` | Exported provenance classes |
| `kosmos/world_model/artifacts.py` | Added code_provenance field to Finding |
| `kosmos/execution/notebook_generator.py` | Added cell_line_mappings to NotebookMetadata |
| `kosmos/workflow/research_loop.py` | Updated generate_report() with hyperlinks |
| `tests/unit/execution/test_provenance.py` | **NEW** - 47 unit tests |
| `tests/integration/execution/test_code_provenance_pipeline.py` | **NEW** - 24 integration tests |

## Remaining Work (2 gaps)

### Implementation Order

| Phase | Order | Issue | Description | Status |
|-------|-------|-------|-------------|--------|
| 4 | 7 | #62 | Code Line Provenance | ✅ Complete |
| 5 | 8 | #64 | Multi-Run Convergence | **Next** |
| 5 | 9 | #65 | Paper Accuracy Validation | Pending |

### Testing Requirements

- All tests must pass (no skipped tests except environment-dependent)
- Mock tests must be accompanied by real-world tests
- Do not proceed until current task is fully working

## Key Documentation

- `docs/CHECKPOINT.md` - Full session summary
- `docs/PAPER_IMPLEMENTATION_GAPS.md` - 17 tracked gaps (15 complete)
- `/home/jim/.claude/plans/groovy-questing-allen.md` - Code line provenance plan
- GitHub Issues #54-#70 - Detailed tracking

## Quick Verification Commands

```bash
# Verify code provenance
python -c "
from kosmos.execution import CodeProvenance, CellLineMapping, create_provenance_from_notebook
from kosmos.world_model.artifacts import Finding

# Test CodeProvenance
provenance = CodeProvenance(
    notebook_path='artifacts/cycle_1/notebooks/task_5_correlation.ipynb',
    cell_index=3,
    start_line=1,
    end_line=15,
    code_snippet='import pandas as pd\ndf = pd.read_csv(\"data.csv\")',
    hypothesis_id='hyp_001',
)
print(f'Hyperlink: {provenance.to_hyperlink()}')
print(f'Citation: {provenance.get_citation_string()}')
print(f'Markdown: {provenance.to_markdown_link()}')
print('All imports successful')
"

# Run tests
python -m pytest tests/unit/execution/test_provenance.py -v --tb=short
python -m pytest tests/integration/execution/test_code_provenance_pipeline.py -v --tb=short
```

## Resume Command

Start by reading the checkpoint:
```
Read docs/CHECKPOINT.md and docs/PAPER_IMPLEMENTATION_GAPS.md, then continue with the next item: #64 - Multi-Run Convergence Framework
```

## Progress Summary

**15/17 gaps fixed (88% complete)**

| Priority | Status |
|----------|--------|
| BLOCKER | 3/3 complete ✅ |
| Critical | 5/5 complete ✅ |
| High | 5/5 complete ✅ |
| Medium | 2/2 complete ✅ |
| Low | 0/2 remaining |

## Next Step

Continue with **#64 - Multi-Run Convergence Framework**:
- Implement `EnsembleRunner.run(n_runs, research_objective)` function
- Calculate convergence metrics across runs
- Report showing findings that appeared in N/M runs
- Non-deterministic validation through replication
