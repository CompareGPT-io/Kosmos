# Pre-Compaction Checklist

**Purpose**: Ensure all critical information is documented before compacting context

⚠️ **IMPORTANT**: Do NOT compact context until ALL items below are checked ✅

📌 **NOTE**: This checklist is **reusable for all phases**. Check the items relevant to your current phase. You do NOT need to rewrite this file for each phase - just use the appropriate phase-specific sections below.

---

## 🔍 Quick Verification (2 minutes)

Run these commands to verify phase completion:

```bash
# 1. Check current phase status
grep "Current Phase" IMPLEMENTATION_PLAN.md

# 2. Verify completion report exists
ls -lt docs/PHASE_*_COMPLETION.md | head -1

# 3. Count completed tasks
grep -c "\[x\]" IMPLEMENTATION_PLAN.md

# 4. Check if any tasks are in progress
grep "in_progress" IMPLEMENTATION_PLAN.md || echo "No tasks in progress ✓"

# 5. Verify tests pass
pytest tests/ -v --tb=short

# 6. Check git status (if using git)
git status
```

---

## ✅ Phase Completion Verification

### Documentation
- [ ] **Phase completion report exists**: `docs/PHASE_[N]_COMPLETION.md` is created
- [ ] **All sections filled**: Executive summary, deliverables, verification checklist, next steps
- [ ] **Verification commands included**: Checklist has actual commands to verify work
- [ ] **Key files documented**: All important files listed with descriptions
- [ ] **QUICKSTART unchanged**: No need to update QUICKSTART_AFTER_COMPACTION.md (it's generic for all phases)

### IMPLEMENTATION_PLAN.md Updates
- [ ] **All checkboxes marked**: All `[ ]` for current phase are now `[x]`
- [ ] **Phase status updated**: Current phase shows "✅ Complete"
- [ ] **Overall progress updated**: Percentage reflects completed tasks (e.g., "12% (35/285 tasks)")
- [ ] **Current phase indicator**: Shows next phase or "Phase N Complete"
- [ ] **Last Updated date**: Date is current

### Code Quality
- [ ] **All tests pass**: `pytest tests/` runs without errors
- [ ] **No broken imports**: Can import main modules without errors
- [ ] **No TODOs left critical**: All blocking TODOs addressed or documented
- [ ] **Code documented**: Key functions have docstrings
- [ ] **No debug code**: No `print()` statements or debug flags left in

### File Organization
- [ ] **All deliverables exist**: Files listed in completion report actually exist
- [ ] **No temporary files**: No `.tmp`, `.bak`, or similar files left around
- [ ] **Config files ready**: `.env.example` updated if needed
- [ ] **Requirements updated**: `pyproject.toml` or `requirements.txt` current

### Testing & Validation
- [ ] **Unit tests written**: Core functionality has tests
- [ ] **Integration tests work**: Phase integrates with previous phases
- [ ] **Manual verification done**: Ran verification commands from completion report
- [ ] **Example works**: Can run a simple example demonstrating phase functionality

### TodoWrite
- [ ] **Todo list cleared**: No items remain in todo list (all completed)
- [ ] **Or documented**: If items remain, they're documented in completion report as known issues

---

## 🎯 Critical Files Checklist

Verify these core files are in good state:

### Always Required
- [ ] `IMPLEMENTATION_PLAN.md` - Up to date with current progress
- [ ] `QUICKSTART_AFTER_COMPACTION.md` - Exists (no updates needed - generic for all phases)
- [ ] `docs/PHASE_COMPLETION_TEMPLATE.md` - Template exists (no updates needed)
- [ ] `PHASE_IMPLEMENTATION_PROMPT.md` - Prompt template exists (no updates needed)
- [ ] `docs/PHASE_[N]_COMPLETION.md` - **NEW file created for current phase**

### Phase-Specific (check what applies)
- [ ] Phase 0: `docs/kosmos-figures-analysis.md`, `docs/integration-plan.md`, `docs/domain-roadmaps/*.md`
- [ ] Phase 1: `kosmos/core/`, `pyproject.toml`, `.env.example`
- [ ] Phase 2: `kosmos/literature/`, `kosmos/knowledge/`
- [ ] Phase 3: `kosmos/agents/hypothesis_generator.py`, `kosmos/models/hypothesis.py`
- [ ] Phase 4: `kosmos/agents/experiment_designer.py`, `kosmos/experiments/templates/`
- [ ] Phase 5: `kosmos/execution/`, `kosmos/execution/statistics.py`
- [ ] Phase 6: `kosmos/analysis/`, `kosmos/analysis/visualization.py`
- [ ] Phase 7: `kosmos/core/feedback.py`, `kosmos/agents/research_director.py`
- [ ] Phase 8: `kosmos/safety/`, `tests/`
- [ ] Phase 9: `kosmos/domains/*/`
- [ ] Phase 10: Web interface, deployment docs

---

## 📊 Verification Commands by Phase

Run the relevant commands for your current phase:

### Phase 0 (Repository Analysis)
```bash
ls docs/kosmos-figures-analysis.md
ls docs/integration-plan.md
ls docs/domain-roadmaps/biology.md
ls docs/domain-roadmaps/neuroscience.md
ls docs/domain-roadmaps/materials_physics.md
ls -d kosmos-figures/
find kosmos-figures -type f | wc -l  # Should be ~120
```

### Phase 1 (Core Infrastructure)
```bash
ls kosmos/core/llm.py
ls kosmos/core/prompts.py
ls kosmos/config.py
ls kosmos/agents/base.py
ls kosmos/core/logging.py
ls kosmos/db/models.py
python -c "import kosmos; print('✓ Package imports')"
pytest tests/unit/test_core.py -v
```

### Phase 2 (Knowledge & Literature)
```bash
ls kosmos/literature/arxiv_client.py
ls kosmos/literature/semantic_scholar.py
ls kosmos/agents/literature_analyzer.py
ls kosmos/knowledge/vector_db.py
ls kosmos/knowledge/graph.py
python -c "from kosmos.literature import arxiv_client; print('✓ Literature imports')"
pytest tests/unit/test_literature.py -v
```

### Phase 5 (Experiment Execution)
```bash
ls kosmos/execution/sandbox.py
ls kosmos/execution/code_generator.py
ls kosmos/execution/data_analysis.py
ls kosmos/execution/statistics.py
python -c "from kosmos.execution.statistics import DataAnalyzer; print('✓ Can import DataAnalyzer')"
pytest tests/unit/test_execution.py -v
# Compare output with kosmos-figures expected results
python tests/integration/test_kosmos_figures_match.py
```

### Phase 6 (Analysis & Interpretation)
```bash
ls kosmos/analysis/visualization.py
ls kosmos/analysis/statistics.py
ls kosmos/agents/data_analyst.py
python -c "from kosmos.analysis.visualization import PublicationVisualizer; print('✓ Can import PublicationVisualizer')"
pytest tests/unit/test_visualization.py -v
# Generate test plots and visually compare
python tests/visual/generate_test_plots.py
```

### Phase 9 (Multi-Domain)
```bash
ls kosmos/domains/biology/metabolomics.py
ls kosmos/domains/biology/genomics.py
ls kosmos/domains/neuroscience/connectomics.py
ls kosmos/domains/materials/optimization.py
python -c "from kosmos.domains.biology import MetabolomicsAnalyzer; print('✓ Biology imports')"
pytest tests/domains/ -v
```

---

## 🚨 Red Flags - DO NOT COMPACT IF:

### Critical Issues
- ❌ **Tests are failing**: Fix before compacting
- ❌ **No completion report**: Create PHASE_[N]_COMPLETION.md first
- ❌ **Code doesn't run**: Fix import errors or runtime issues
- ❌ **Tasks marked in_progress**: Complete or move to pending first
- ❌ **Checkboxes not updated**: Mark all completed tasks in IMPLEMENTATION_PLAN.md

### Medium Issues (Document if can't fix)
- ⚠️ **Known bugs**: Document in completion report under "Known Issues"
- ⚠️ **Incomplete features**: Document as "Technical Debt" with plan
- ⚠️ **Missing tests**: Note in completion report, plan to add later
- ⚠️ **Performance issues**: Document with measurements and plan

### Low Issues (OK to compact with)
- ✓ **Minor TODOs**: OK if documented in code comments
- ✓ **Optimization opportunities**: Note for future improvement
- ✓ **Code style issues**: Can refactor later
- ✓ **Documentation could be better**: As long as basics are covered

---

## 📝 Pre-Compaction Summary

Fill this out before compacting:

```
Phase Completed: Phase [N] - [Phase Name]
Date: [YYYY-MM-DD]
Completion Report: docs/PHASE_[N]_COMPLETION.md
Overall Progress: [X]% ([Y]/285 tasks)

Key Deliverables:
1. [Deliverable 1]
2. [Deliverable 2]
3. [Deliverable 3]

Tests Status: [PASS/FAIL] ([X] tests, [Y]% coverage)

Known Issues: [None / List issues]

Ready to Compact: [YES/NO]
```

---

## 🔄 Recovery Plan After Compaction

When you resume, new Claude instance should:

1. **Read**: `QUICKSTART_AFTER_COMPACTION.md` (30 seconds)
2. **Verify**: Run commands from `PHASE_[N]_COMPLETION.md` (2 minutes)
3. **Review**: Read `IMPLEMENTATION_PLAN.md` for next phase (2 minutes)
4. **Start**: Use prompt from `PHASE_IMPLEMENTATION_PROMPT.md` for next phase

**Expected Recovery Time**: ~5 minutes

---

## ✅ Final Checklist Before Compacting

```bash
# 1. All documentation complete
[ ] Phase completion report created and complete
[ ] IMPLEMENTATION_PLAN.md updated
[ ] All verification commands pass

# 2. Code is stable
[ ] Tests pass
[ ] No in-progress tasks
[ ] No critical bugs

# 3. Files are organized
[ ] All deliverables exist
[ ] No temporary files
[ ] Requirements/dependencies updated

# 4. Git committed (if using)
[ ] All changes committed
[ ] Commit message describes phase completion
[ ] No uncommitted changes

# 5. Ready for next phase
[ ] Know what next phase is
[ ] Next phase has clear first task
[ ] No blockers for next phase
```

---

## 🎯 Quick Compact Command

Once ALL items above are ✅, you can safely compact by saying:

```
"I've verified the pre-compaction checklist. All items are ✅.
Ready to compact context.

Last completed: Phase [N] - [Name]
Next phase: Phase [N+1] - [Name]
Documentation: docs/PHASE_[N]_COMPLETION.md is complete"
```

---

## 💾 Backup Reminder (Optional but Recommended)

If working on critical phase, consider:

```bash
# Create backup of entire project
tar -czf kosmos_phase_[N]_backup_$(date +%Y%m%d).tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='venv' \
    .

# Or commit to git
git add .
git commit -m "Phase [N] complete - ready for compaction"
git tag "phase-[N]-complete"
```

---

## 📞 If Something Goes Wrong After Compaction

1. **Can't find completion report**:
   - Look in `docs/` directory
   - Check git history: `git log --all --full-history -- docs/PHASE_*_COMPLETION.md`

2. **Tests failing after resume**:
   - Read completion report for known issues
   - Check if environment/dependencies changed
   - May need to re-run last few tasks

3. **Can't remember what was done**:
   - Read `QUICKSTART_AFTER_COMPACTION.md`
   - Read latest `docs/PHASE_[N]_COMPLETION.md`
   - Check git log: `git log --oneline -20`

4. **Deliverables missing**:
   - Check completion report for expected file locations
   - Verify with `ls` commands from verification checklist
   - May need to regenerate (should be rare if checklist was followed)

---

## 🎓 Best Practices

### DO ✅
- Complete one phase fully before starting next
- Create completion report immediately after finishing
- Run all verification commands before marking complete
- Clear todos completely
- Update all progress indicators
- Test everything works before compacting

### DON'T ❌
- Leave tasks in "in_progress" state
- Skip verification commands
- Forget to update IMPLEMENTATION_PLAN.md
- Leave broken tests
- Skip completion report creation
- Compact with uncommitted changes (if using git)

---

**Last Updated**: 2025-11-06 (After Phase 0)
**Checklist Version**: 1.0

**Usage Note**: This checklist applies to ALL phases. When using it:
- Use the "Quick Verification" commands at the top
- Check items in "Phase Completion Verification" section
- Run only the "Verification Commands by Phase" for YOUR current phase
- Optional: Update "Last Updated" date above when you use it (not required)

---

**REMEMBER**: Better to spend 5 extra minutes verifying before compaction than losing hours of work due to incomplete documentation! 🛡️
