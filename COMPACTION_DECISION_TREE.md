# Compaction Decision Tree

**Purpose**: Simple flowchart - know exactly what to do in 10 seconds

---

```
┌─────────────────────────────────────────────────┐
│  Need to compact context?                      │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
         Is current phase 100% complete?
                  │
        ┌─────────┴─────────┐
        │                   │
       YES                 NO
        │                   │
        ▼                   ▼
   ┌─────────┐      ┌──────────────┐
   │ Phase   │      │ Mid-Phase    │
   │ Complete│      │ Compaction   │
   └────┬────┘      └──────┬───────┘
        │                   │
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│ YOU SAY:      │   │ YOU SAY:         │
│               │   │                  │
│ "Check        │   │ "Create          │
│ PRE_          │   │ checkpoint       │
│ COMPACTION_   │   │ using            │
│ CHECKLIST.md" │   │ GUIDE template.  │
│               │   │ Save as:         │
│               │   │ docs/PHASE_1_    │
│               │   │ CHECKPOINT_      │
│               │   │ 2025-11-07.md"   │
│               │   │                  │
│ Model: ✅     │   │ (Fill in actual  │
│               │   │ phase & date)    │
│ YOU: /compact │   │                  │
│               │   │ Model: Creates   │
│ ↓             │   │                  │
│ New session   │   │ YOU: /compact    │
│ ↓             │   │ ↓                │
│ Open:         │   │ New session      │
│ READY_TO_     │   │ ↓                │
│ PASTE_        │   │ "Resume Phase N  │
│ PROMPTS.md    │   │ from checkpoint  │
│               │   │ 2025-11-07.md"   │
│ Copy Phase    │   │                  │
│ N+1 prompt    │   │ (Use MID_PHASE_  │
│               │   │ QUICK_PROMPT.md  │
│ Paste to      │   │ for exact words) │
│ Claude        │   │                  │
└───────────────┘   └──────────────────┘
```

---

## 🎯 Super Simple Version

### Phase Complete?
```
You: "Check PRE_COMPACTION_CHECKLIST.md"
You: /compact
You: [Copy from READY_TO_PASTE_PROMPTS.md]
```

### Phase Incomplete?
```
You: [Copy from MID_PHASE_QUICK_PROMPT.md]
     (Fill in phase number and today's date)
You: /compact
You: [Copy resume prompt from MID_PHASE_QUICK_PROMPT.md]
     (Fill in phase number and checkpoint date)
```

---

## 📚 Document Roles

| Document | Type | Who Uses It | When |
|----------|------|-------------|------|
| **PRE_COMPACTION_CHECKLIST.md** | Checklist | YOU read | Phase complete |
| **READY_TO_PASTE_PROMPTS.md** | Prompts | YOU copy | After phase complete compact |
| **MID_PHASE_COMPACTION_PROCESS.md** | Process guide | YOU read | Learn mid-phase process |
| **MID_PHASE_COMPACTION_GUIDE.md** | Template | MODEL uses | Create checkpoint |
| **MID_PHASE_QUICK_PROMPT.md** | Quick prompts | YOU copy | Need mid-phase compact |

---

## 💡 Key Insight

**You ALWAYS fill in**:
- Phase number: `1`, `2`, `3`, etc. (not `[N]`)
- Date: `2025-11-07`, `2025-11-08`, etc. (not `[YYYY-MM-DD]`)

**The model can't guess these** - you must provide actual values!

---

## ✅ Examples

### ❌ WRONG:
```
"Save as docs/PHASE_[N]_CHECKPOINT_[YYYY-MM-DD].md"
```
**Why**: Model doesn't know what [N] and [YYYY-MM-DD] mean

### ✅ RIGHT:
```
"Save as docs/PHASE_1_CHECKPOINT_2025-11-07.md"
```
**Why**: Clear, specific filename

---

## 🔍 After Compaction - How to Tell

```bash
head -30 IMPLEMENTATION_PLAN.md
```

**Look for**:
- `Complete ✅` → Was end-of-phase
- `In Progress 🔄` → Was mid-phase
- `Checkpoint: docs/PHASE_X_CHECKPOINT_DATE.md` → Tells you which checkpoint to read

---

## 📞 Emergency: Completely Lost?

1. Read: `QUICKSTART_AFTER_COMPACTION.md`
2. Run: `head -30 IMPLEMENTATION_PLAN.md`
3. It will tell you if there's a checkpoint
4. Read the checkpoint or completion report it references
5. Follow instructions in that document

---

**Created**: 2025-11-07
**Purpose**: Ultra-simple decision tree
**Use**: When you can't remember which process to follow
