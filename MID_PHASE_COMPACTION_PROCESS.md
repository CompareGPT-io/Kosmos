# Mid-Phase Compaction Process

**Purpose**: How to safely compact context in the middle of a phase and resume exactly where you left off

---

## 🚨 When to Use This

Use mid-phase compaction when:
- ❌ Context is running low but phase isn't complete
- ❌ Session is taking too long and you need a break
- ❌ Unexpected interruption before phase completion
- ❌ Need to switch Claude instances mid-phase

**Do NOT use if**: Phase is complete (use normal PRE_COMPACTION_CHECKLIST.md instead)

---

## 📋 Step-by-Step Process

### Before Compacting (10 minutes)

#### Step 1: Create Checkpoint Document
```
You: "We need to compact mid-phase. Please create a checkpoint using MID_PHASE_COMPACTION_GUIDE.md as template. Save it as docs/PHASE_[N]_CHECKPOINT_[DATE].md"

Model: [Creates detailed checkpoint with current state]
```

**The checkpoint should include**:
- ✅ Current task in progress
- ✅ What's complete vs. partial vs. not started
- ✅ Files modified and their status
- ✅ Code snippets showing what's done
- ✅ Open questions and issues
- ✅ Exact next steps to resume
- ✅ TodoWrite snapshot

#### Step 2: Update IMPLEMENTATION_PLAN.md
```
You: "Update IMPLEMENTATION_PLAN.md to reflect current progress:
- Mark completed tasks with [x]
- Leave in-progress tasks as [ ] with comment: <!-- In progress: see PHASE_[N]_CHECKPOINT_[DATE].md -->
- Update progress counter for phase"

Model: [Updates IMPLEMENTATION_PLAN.md]
```

Example:
```markdown
## Phase 1: Core Infrastructure Setup
**Status**: 🔄 In Progress | **Progress**: 3/6 tasks

### 1.1 Project Structure
- [x] Create Python package structure (`kosmos/`, `tests/`, `docs/`)
- [x] Set up `pyproject.toml` with project metadata and dependencies
- [x] Create `.env.example` for configuration template
- [ ] Initialize git repository with proper `.gitignore` <!-- In progress: see PHASE_1_CHECKPOINT_2025-11-07.md -->
- [ ] Create `README.md` with project overview
```

#### Step 3: Commit Current State (if using git)
```bash
git add .
git commit -m "WIP: Phase [N] checkpoint - [brief description]

See docs/PHASE_[N]_CHECKPOINT_[DATE].md for details"
```

#### Step 4: Quick Verification
```
You: "Run these verification commands and add output to checkpoint:
- git status
- pytest tests/ -v (or note which tests don't exist yet)
- ls -la [modified directories]"

Model: [Adds verification output to checkpoint]
```

#### Step 5: Final Checkpoint Review
```
You: "Read back the checkpoint document and confirm:
1. Can I resume exactly where we left off?
2. Are all in-progress tasks clearly marked?
3. Are next steps explicit?"

Model: [Reviews and confirms/updates checkpoint]
```

---

### Compacting

```
You: /compact
```

---

### After Compacting (5 minutes)

#### Step 1: Recovery Prompt
```
I need to resume Phase [N] which was interrupted mid-phase.

Recovery Steps:
1. Read @QUICKSTART_AFTER_COMPACTION.md for general context
2. Read @docs/PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md for exact current state
3. Review @IMPLEMENTATION_PLAN.md Phase [N] section to see what's complete

Current Status:
- Phase [N] is IN PROGRESS ([X]/[Y] tasks complete)
- Last working on: [brief description from checkpoint]
- Resume from: "Next Immediate Steps" in checkpoint document

Tasks:
4. Verify current environment state using commands in checkpoint
5. Review "Files Modified" and "Code Changes Summary" sections
6. Review "Open Questions" and "Issues Encountered"
7. Create TodoWrite list with remaining tasks (referencing checkpoint)
8. Continue from "Next Immediate Steps"
9. When tasks are complete, mark them in BOTH TodoWrite and IMPLEMENTATION_PLAN.md

Please confirm you've recovered the context and present your understanding of:
- What was completed
- What's partially done
- What's next
- Any open questions or blockers
```

#### Step 2: Model Recovers Context
Model reads checkpoint and confirms understanding

#### Step 3: You Approve & Continue
```
You: "Correct. Please continue from [specific next step]"
```

---

## 📁 File Organization for Mid-Phase Compaction

### Checkpoint Files
```
docs/
├── PHASE_0_COMPLETION.md          # Full phase completions
├── PHASE_1_CHECKPOINT_2025-11-07.md   # Mid-phase checkpoint
├── PHASE_1_CHECKPOINT_2025-11-08.md   # Another checkpoint if needed
├── PHASE_1_COMPLETION.md          # Final completion (when phase done)
└── PHASE_2_CHECKPOINT_2025-11-09.md   # Phase 2 checkpoint
```

**Naming Convention**: `PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md`

**When Phase Completes**: Create normal `PHASE_[N]_COMPLETION.md` and checkpoints become archive

---

## 🎯 Checkpoint vs. Completion Report

| Aspect | Checkpoint (Mid-Phase) | Completion (Phase Done) |
|--------|----------------------|------------------------|
| **When** | Context runs out mid-phase | Phase 100% complete |
| **Status** | 🔄 In Progress | ✅ Complete |
| **Focus** | Current task, next steps | All deliverables, success |
| **Detail** | Very specific (file level) | High-level summary |
| **Purpose** | Resume exactly where left off | Document what was achieved |
| **File Name** | `PHASE_[N]_CHECKPOINT_[DATE].md` | `PHASE_[N]_COMPLETION.md` |

---

## 📊 IMPLEMENTATION_PLAN.md Updates

### Normal Completion
```markdown
## Phase 1: Core Infrastructure Setup
**Status**: ✅ Complete | **Progress**: 6/6 tasks
```

### Mid-Phase Checkpoint
```markdown
## Phase 1: Core Infrastructure Setup
**Status**: 🔄 In Progress | **Progress**: 3/6 tasks
**Checkpoint**: docs/PHASE_1_CHECKPOINT_2025-11-07.md
```

### Dashboard Updates

**Normal (Phase Complete)**:
```markdown
**Current Phase**: Phase 1 Complete ✅
**Overall Progress**: 12% (35/285 tasks)
```

**Mid-Phase**:
```markdown
**Current Phase**: Phase 1 In Progress (50% - see checkpoint)
**Overall Progress**: 9% (27/285 tasks)
**Checkpoint**: docs/PHASE_1_CHECKPOINT_2025-11-07.md
```

---

## ⚡ Quick Reference Card

### Before Compacting Mid-Phase:
1. ✅ Create checkpoint using MID_PHASE_COMPACTION_GUIDE.md template
2. ✅ Update IMPLEMENTATION_PLAN.md (mark complete tasks, note in-progress)
3. ✅ Commit to git (if using): "WIP: Phase N checkpoint"
4. ✅ Run verification commands
5. ✅ Review checkpoint for completeness
6. ✅ /compact

### After Compacting Mid-Phase:
1. ✅ Paste recovery prompt (includes reading checkpoint)
2. ✅ Model recovers context from checkpoint
3. ✅ Verify understanding
4. ✅ Continue from "Next Immediate Steps"

---

## 🔄 Multiple Checkpoints Per Phase

If you need multiple checkpoints in one phase:

```
docs/
├── PHASE_1_CHECKPOINT_2025-11-07.md  # First checkpoint (3/6 tasks)
├── PHASE_1_CHECKPOINT_2025-11-08.md  # Second checkpoint (4/6 tasks)
└── PHASE_1_COMPLETION.md             # Final completion (6/6 tasks)
```

**Always reference the LATEST checkpoint** in IMPLEMENTATION_PLAN.md and recovery prompts.

**Old checkpoints**: Keep for history, but clearly mark which is current:
```markdown
## Phase 1: Core Infrastructure Setup
**Status**: 🔄 In Progress | **Progress**: 4/6 tasks
**Current Checkpoint**: docs/PHASE_1_CHECKPOINT_2025-11-08.md
**Previous Checkpoint**: docs/PHASE_1_CHECKPOINT_2025-11-07.md (archived)
```

---

## 🎓 Best Practices

### DO ✅
- Create checkpoint **before** context runs out
- Be **very specific** about current state
- Include **code snippets** of partial work
- List **exact next steps**
- Update IMPLEMENTATION_PLAN.md to match reality
- Commit to git with clear "WIP" message
- Reference latest checkpoint in IMPLEMENTATION_PLAN.md

### DON'T ❌
- Wait until context is critical to checkpoint
- Be vague about what's done ("mostly finished")
- Forget to mark in-progress tasks clearly
- Leave broken code without noting it
- Forget to snapshot TodoWrite list
- Compact without creating checkpoint first

---

## 🧪 Example: Mid-Phase Compaction

### Scenario
You're in Phase 1, subsection 1.3 (Configuration System). You've finished subsection 1.1 and 1.2, and are halfway through 1.3 when context runs low.

### What You Do:

**Step 1**: Create checkpoint
```
You: "Create checkpoint using MID_PHASE_COMPACTION_GUIDE.md template.
We're in Phase 1, have completed subsections 1.1 and 1.2 fully.
Currently working on 1.3 Configuration System:
- ✅ Created kosmos/config.py
- ✅ Added environment variable support
- 🔄 Working on configuration validation (half done)
- ❌ Haven't started logging configuration yet

Save as docs/PHASE_1_CHECKPOINT_2025-11-07.md"
```

**Step 2**: Update IMPLEMENTATION_PLAN.md
```markdown
## Phase 1: Core Infrastructure Setup
**Status**: 🔄 In Progress | **Progress**: 2.5/6 tasks (42%)
**Checkpoint**: docs/PHASE_1_CHECKPOINT_2025-11-07.md

### 1.1 Project Structure
- [x] Create Python package structure
- [x] Set up pyproject.toml
- [x] Create .env.example
- [x] Initialize git repository
- [x] Create README.md

### 1.2 Claude API Integration
- [x] Create kosmos/core/llm.py
- [x] Implement rate limiting
- [x] Add error handling
- [x] Create prompt template system
- [x] Add token usage tracking
- [x] Write unit tests

### 1.3 Configuration System
- [x] Create kosmos/config.py
- [x] Add support for environment variables
- [ ] Implement research parameter configuration <!-- In progress: see checkpoint -->
- [ ] Create configuration validation <!-- PARTIALLY DONE: see checkpoint -->
- [ ] Add logging configuration

### 1.4-1.6 Not Started Yet
```

**Step 3**: Git commit
```bash
git add .
git commit -m "WIP: Phase 1 checkpoint - config validation in progress

Completed: subsections 1.1, 1.2, partial 1.3
In progress: Configuration validation
See docs/PHASE_1_CHECKPOINT_2025-11-07.md"
```

**Step 4**: Compact
```
You: /compact
```

**Step 5**: Resume (after compaction)
```
I need to resume Phase 1 which was interrupted mid-phase.

Recovery Steps:
1. Read @QUICKSTART_AFTER_COMPACTION.md for general context
2. Read @docs/PHASE_1_CHECKPOINT_2025-11-07.md for exact state
3. Review @IMPLEMENTATION_PLAN.md Phase 1 section

Current Status:
- Phase 1 is IN PROGRESS (2.5/6 tasks complete, 42%)
- Last working on: Configuration validation in kosmos/config.py
- Resume from: Adding validation rules for configuration parameters

Tasks:
4. Verify environment using checkpoint verification commands
5. Review kosmos/config.py to see current implementation
6. Continue from "Next Immediate Steps" in checkpoint
7. Mark tasks complete in TodoWrite and IMPLEMENTATION_PLAN.md as you finish

Please confirm you've recovered context and present:
- What subsections are complete (1.1, 1.2)
- What's partially done (1.3 config validation)
- Exact next steps
```

---

## 🆘 Emergency Quick Checkpoint

If context is **critically low** and you don't have time for full checkpoint:

```
You: "Emergency checkpoint! Capture:
1. Current file being edited: [filename]
2. What's done in this file
3. What's NOT done yet
4. Next 3 steps
Save as docs/PHASE_[N]_EMERGENCY_[TIME].md"
```

**Then immediately**: `/compact`

**After recovery**: Expand emergency checkpoint into proper checkpoint before continuing.

---

## 📝 Checkpoint Template Location

**Template**: `MID_PHASE_COMPACTION_GUIDE.md` (root directory)
**Filled Checkpoints**: `docs/PHASE_[N]_CHECKPOINT_[DATE].md`
**Completion Reports**: `docs/PHASE_[N]_COMPLETION.md`

---

**Last Updated**: 2025-11-07
**Version**: 1.0
**Use For**: Any mid-phase compaction situation
