# Mid-Phase Compaction: Quick Prompt

**Use this when you need to compact before a phase is done**

---

## 🎯 What You Say (Copy This)

### Step 1: Create Checkpoint
```
We need to compact mid-phase. Please create a checkpoint document.

Instructions:
1. Use @MID_PHASE_COMPACTION_GUIDE.md as the template structure
2. Fill in all sections with current state:
   - Current task in progress
   - What's complete vs partial vs not started
   - Files modified and their status
   - Next immediate steps
   - Open questions and issues
   - TodoWrite snapshot
3. Save as: docs/PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md

Replace [N] with current phase number (e.g., 1, 2, 3...)
Replace [YYYY-MM-DD] with today's date (e.g., 2025-11-07)

Example: docs/PHASE_1_CHECKPOINT_2025-11-07.md
```

### Step 2: Update IMPLEMENTATION_PLAN.md
```
Update IMPLEMENTATION_PLAN.md:

1. Mark completed tasks with [x]
2. Leave in-progress tasks as [ ] with comment:
   <!-- In progress: see PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md -->
3. Update phase status line to:
   **Status**: 🔄 In Progress | **Progress**: [X]/[Y] tasks ([Z]%)
   **Checkpoint**: docs/PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md
4. Update dashboard section:
   **Current Phase**: Phase [N] In Progress ([X]% - see checkpoint)
   **Overall Progress**: [percentage]
   **Checkpoint**: docs/PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md
```

### Step 3: Verify Checkpoint
```
Please read back the checkpoint and confirm it includes:
1. Clear "Next Immediate Steps" section
2. All modified files listed
3. Current vs. remaining work clearly marked
4. Any open questions or blockers noted
```

### Step 4: Ready to Compact
```
Once verified, tell me: "Checkpoint complete. Ready to compact."
```

---

## 📋 Example: Phase 1 Mid-Compaction (November 7)

**What you'd actually say**:

```
We need to compact mid-phase. Please create a checkpoint document.

Instructions:
1. Use @MID_PHASE_COMPACTION_GUIDE.md as the template structure
2. Fill in all sections with current state
3. Save as: docs/PHASE_1_CHECKPOINT_2025-11-07.md

Then update IMPLEMENTATION_PLAN.md:
- Mark completed tasks [x]
- Note in-progress tasks with: <!-- In progress: see PHASE_1_CHECKPOINT_2025-11-07.md -->
- Update Phase 1 status to: 🔄 In Progress with checkpoint reference
- Update dashboard to reference checkpoint

Then read back and confirm checkpoint is complete.
```

---

## 🔄 After Compacting - Resume Prompt

**What you'd say after /compact**:

```
I need to resume Phase [N] which was interrupted mid-phase.

Recovery:
1. Read @QUICKSTART_AFTER_COMPACTION.md for general context
2. Read @docs/PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md for exact state
3. Review @IMPLEMENTATION_PLAN.md Phase [N] section

Please confirm you've recovered context from the checkpoint and tell me:
- What's been completed
- What's partially done
- What the next immediate steps are
- Any open questions or blockers

Then continue from "Next Immediate Steps" in the checkpoint.
```

**Example for Phase 1**:
```
I need to resume Phase 1 which was interrupted mid-phase.

Recovery:
1. Read @QUICKSTART_AFTER_COMPACTION.md
2. Read @docs/PHASE_1_CHECKPOINT_2025-11-07.md
3. Review @IMPLEMENTATION_PLAN.md Phase 1 section

Confirm you've recovered context and continue from checkpoint.
```

---

## 🎯 Key Points

1. **YOU fill in the specific numbers**:
   - Phase number: 1, 2, 3, etc.
   - Today's date: 2025-11-07, 2025-11-08, etc.

2. **Model uses the template**:
   - You reference: `@MID_PHASE_COMPACTION_GUIDE.md`
   - Model creates: `docs/PHASE_[N]_CHECKPOINT_[DATE].md`

3. **For process details**, YOU read:
   - `MID_PHASE_COMPACTION_PROCESS.md` (full instructions)
   - THIS file (quick prompts to copy)

---

## 📞 Quick Decision

**Need to compact?**

```
Is phase complete?
├─ YES → Say: "Check PRE_COMPACTION_CHECKLIST.md"
└─ NO → Copy prompt from THIS file
```

---

**Created**: 2025-11-07
**Purpose**: Exact prompts to use for mid-phase compaction
**No editing needed**: Just copy and fill in phase number and date
