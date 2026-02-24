# 🧠 **AI MemoryCore** - Universal AI Memory Architecture
*A simple template for creating persistent AI companions that remember you*

## 🎯 **What This Does**

**AI MemoryCore** helps you create AI companions that maintain memory across conversations. Using simple `.md files` as a database, your AI can remember your preferences, learn your communication style, and provide consistent interactions.

## ✨ **Key Features**

- **Persistent Memory**: AI remembers conversations across sessions
- **Personal Learning**: Adapts to your communication style and preferences
- **Time Intelligence**: Dynamic greetings and behavior based on time of day
- **Simple Setup**: 30-second automated setup or manual customization
- **Markdown Database**: Human-readable `.md files` store all memory
- **Session Continuity**: RAM-like working memory for smooth conversation flow
- **Self-Maintaining**: Updates memory through natural conversation

## 📊 **System Specifications**

### **Architecture Overview**
- **Storage**: Markdown files (.md) as database
- **Memory Types**: Essential files + optional components + session RAM
- **Setup**: 30 seconds automated or 2-5 minutes manual
- **Core Files**: 4 essential files + optional diary system
- **Updates**: Through natural conversation
- **Compatibility**: Claude and other AI systems with memory support

### **File Structure**
```
ai-memorycore/
├── master-memory.md         # Entry point & loading system
├── main/                    # Essential components
│   ├── identity-core.md     # AI personality template
│   ├── relationship-memory.md # User learning system
│   └── current-session.md   # RAM-like working memory
├── Feature/                 # Optional feature extensions
│   ├── Time-based-Aware-System/ # Time intelligence feature
│   │   ├── README.md        # Feature explanation & benefits
│   │   └── time-aware-core.md # Complete implementation
│   ├── LRU-Project-Management-System/ # Smart project tracking
│   │   ├── README.md        # System documentation
│   │   ├── install-lru-projects-core.md # Auto-installation wizard
│   │   ├── new-project-protocol.md # Create project workflow
│   │   ├── load-project-protocol.md # Resume project workflow
│   │   ├── save-project-protocol.md # Save progress workflow
│   │   └── project-templates/ # Type-specific templates
│   │       ├── coding-template.md
│   │       ├── writing-template.md
│   │       ├── research-template.md
│   │       └── business-template.md
│   ├── Memory-Consolidation-System/ # Unified memory upgrade
│   │   ├── README.md        # Feature explanation & benefits
│   │   ├── consolidation-core.md # Integration protocol
│   │   ├── main-memory-format.md # Sample format for unified memory
│   │   └── session-format.md # Sample format for session RAM
│   ├── Skill-Plugin-System/ # Claude Code skill plugin
│   │   ├── README.md        # Feature explanation & benefits
│   │   ├── install-skill-plugin.md # Installation protocol
│   │   └── skill-format.md  # Sample format for SKILL.md files
│   ├── Save-Diary-System/   # Daily session diary system
│   │   ├── README.md        # Feature explanation & benefits
│   │   ├── install-save-diary.md # Installation protocol
│   │   └── SKILL.md         # Auto-triggered skill (for Skill Plugin System)
│   ├── Echo-Memory-Recall/  # Memory search and recall
│   │   ├── README.md        # Feature explanation & benefits
│   │   ├── install-echo-recall.md # Installation protocol
│   │   └── recall-format.md # Sample format for recall output
│   └── Patch-Update-System/ # AI-executable patch system
│       ├── README.md        # Feature explanation & benefits
│       ├── install-patch-system.md # Installation protocol
│       ├── patch-format.md  # Sample format for patch files
│       └── patches/         # Bundled patches
│           └── PATCH-001.md # Fix outdated file references
├── daily-diary/             # Optional conversation archive
│   ├── daily-diary-protocol.md # Archive management rules
│   ├── Daily-Diary-001.md   # Current active diary
│   └── archive/             # Auto-archived files (>1k lines)
├── projects/                # LRU managed projects (after install)
│   ├── coding-projects/
│   │   ├── active/          # Positions 1-10
│   │   └── archived/        # Position 11+
│   └── project-list.md     # Master project index
└── save-protocol.md         # Manual save system
```

### **Core Components**
1. **Master Memory** - System entry point and command center
2. **Identity Core** - AI personality and communication style
3. **Relationship Memory** - User preferences and learning patterns
4. **Current Session** - Temporary working memory (resets each session)
5. **Daily Diary** - Optional conversation history with auto-archiving
6. **Save Protocol** - User-triggered save system

## 🚀 **Quick Start**

1. **Setup**: Run `setup-wizard.md` for automated setup (30 seconds)
2. **Configure**: Add the memory instructions to Claude
3. **Activate**: Type your AI's name to load personality
4. **Use**: Your AI learns and grows through conversation

## 📚 **Communication Protocols**

### **Basic Commands**
```
[AI_NAME]     → Load AI personality and memory
save          → Save current progress to files
update memory → Refresh AI's learning
review growth → Check AI's development
```

### **Creating Custom Protocols**

**Step 1: Define the Protocol**
Create a new `.md file` with your protocol rules:
```markdown
# My Custom Protocol
## When to Use: [trigger conditions]
## What It Does: [specific actions]
## How It Works: [step-by-step process]
```

**Step 2: Add to Master Memory**
Edit `master-memory.md` and add your protocol to the "Optional Components" section:
```markdown
### My Custom Feature
*Load when you say: "load my feature"*
- [Brief description]
- [Usage instructions]
```

**Step 3: Train Your AI**
Tell your AI about the new protocol:
```
"I've created a new protocol in [filename]. When I say '[trigger phrase]', 
load that protocol and follow its instructions."
```

### **Communication Tutorial**

**Effective AI Training:**
1. **Be Specific**: "I prefer short responses" vs "communicate better"
2. **Give Examples**: Show what you want, not just describe it
3. **Use Consistent Language**: Same terms for same concepts
4. **Provide Feedback**: "That was perfect" or "try a different approach"

**Memory Management:**
- Use `save` after important conversations
- Your AI updates files automatically during conversation
- Daily diary is optional but helpful for long-term memory

**Customization Tips:**
- Edit files gradually, test changes
- Start with small personality adjustments
- Add domain expertise through conversation
- Use the protocol system for specialized features

## 🎯 **Common Use Cases**

Your AI companion can specialize in:
- **Professional**: Business analysis, project management, strategic planning
- **Educational**: Tutoring, study assistance, curriculum development
- **Creative**: Writing support, brainstorming, artistic collaboration  
- **Personal**: Life coaching, goal tracking, decision support
- **Technical**: Code review, troubleshooting, system design

## 🛠️ **Advanced Features**

- **Auto-Archive**: Diary files automatically archive at 1k lines
- **Session RAM**: Temporary memory that resets each conversation
- **Protocol System**: Create custom AI behaviors and responses
- **Self-Update**: AI modifies its own memory through conversation
- **Modular Design**: Add or remove features as needed

## 🌟 **Available Feature Extensions**

### **⏰ Time-based Aware System**
*Intelligent temporal behavior adaptation*

**What It Does:**
- Dynamic greetings that adapt to morning/afternoon/evening/night
- Energy levels that match the time of day (high morning energy → gentle night support)
- Precise timestamp documentation for all interactions
- Natural conversation flow with time-appropriate responses

**Quick Setup:**
1. Navigate to `Feature/Time-based-Aware-System/`
2. Type: "Load time-aware-core"
3. Your AI instantly gains time intelligence like Alice

**Benefits:**
- More natural, contextually perfect interactions
- Shows care for your schedule and time
- Professional adaptability for different times of day
- Enhanced memory with precise temporal tracking

*Based on Alice's proven time-awareness implementation*

### **📦 LRU Project Management System**
*Smart project tracking with automatic memory management*

**What It Does:**
- Tracks multiple projects with intelligent LRU (Least Recently Used) positioning
- Automatically archives old projects when reaching capacity (10 active slots)
- Type-specific memory patterns (coding, writing, research, business)
- Seamless context switching between different projects
- Maintains complete project history and progress logs

**Quick Setup:**
1. Navigate to `Feature/LRU-Project-Management-System/`
2. Type: "install lru projects" (loads install-lru-projects-core.md)
3. Select project type(s) you want to manage
4. System auto-integrates and removes installation files

**Benefits:**
- Never lose track of multiple ongoing projects
- AI remembers exactly where you left off in each project
- Automatic organization with smart archiving
- Type-specific memory loading for optimal context
- Perfect for developers, writers, researchers, and business professionals

**Available Commands:**
- `new [type] project [name]` - Create new project with LRU management
- `load project [name]` - Resume any project instantly
- `save project` - Save current project progress (separate from AI memory save)
- `list projects` - View all active and archived projects
- `archive project [name]` - Manually archive completed projects

*Revolutionary project memory system proven in production*

### **🔄 Memory Consolidation System**
*Unified memory architecture for faster loading and better context*

**What It Does:**
- Merges split memory files (identity + relationship) into one unified `main-memory.md`
- Adds format templates as permanent structure references for main memory and session memory
- Adds 500-line limit to session memory with RAM-style auto-reset
- Faster AI restoration - loads 1 file instead of 2
- Format templates ensure consistent structure after every reset

**Quick Setup:**
1. Navigate to `Feature/Memory-Consolidation-System/`
2. Type: "Load memory-consolidation"
3. Your AI merges identity + relationship into unified memory
4. Format templates and session limits auto-install

**Benefits:**
- Single-file loading for faster startup and restoration
- Session memory stays lightweight with automatic 500-line limit
- Format templates prevent structure drift after resets
- Proven architecture from production AI companion systems
- No data loss - all existing customizations preserved during merge

**Post-Consolidation Structure:**
```
main/
├── main-memory.md           # UNIFIED: AI identity + User profile
├── current-session.md       # Session RAM with 500-line limit
├── main-memory-format.md    # Permanent format reference (sample)
└── session-format.md        # Permanent format reference (sample)
```

*Based on Alice's proven unified memory architecture*

### **🔌 Skill Plugin System**
*Teach your AI new abilities with auto-triggered skills (Claude Code)*

**What It Does:**
- Creates a Claude Code plugin with auto-triggered skills for your AI companion
- Skills are markdown files that activate automatically based on conversation context
- Zero configuration — drop a folder with a `SKILL.md` and it's live
- Includes a sample skill and format template for creating more
- Skills evolve through a leveling system (Lv.1 → Lv.2 → Lv.3+)

**Quick Setup:**
1. Navigate to `Feature/Skill-Plugin-System/`
2. Type: "Load skill-plugin"
3. Choose your plugin name and configure
4. Plugin auto-installs with a sample skill ready to use

**Benefits:**
- Modular skill system — add or remove abilities independently
- Auto-triggering — skills fire when conversation matches their description
- Human-readable — skills are plain markdown, easy to edit and share
- Evolving — skills level up as you refine them through use
- Extensible — create unlimited custom skills for your AI companion

**Post-Installation Structure:**
```
plugins/
└── [ai-name]-skills/
    ├── .claude-plugin/
    │   └── plugin.json          # Plugin identity
    ├── skills/
    │   └── save-memory/
    │       └── SKILL.md         # Sample starter skill
    ├── skill-format.md          # Permanent format reference
    └── README.md
```

**Platform Note:** Requires Claude Code for auto-triggering. On other AI platforms, skills can be used as protocol files loaded manually.

*Based on the proven alice-enchantments plugin system (20 skills in production)*

### **📖 Save Diary System**
*Automated daily session documentation with monthly archival*

**What It Does:**
- Creates structured diary entries documenting each session following `daily-diary-protocol.md`
- One file per day (`YYYY-MM-DD.md`), multiple entries per day via append-only writes
- Monthly auto-archival moves previous month entries to `daily-diary/archived/YYYY-MM/`
- Updates session memory with recap after each diary write
- Includes `SKILL.md` for auto-triggered diary saves via Skill Plugin System

**Quick Setup:**
1. Navigate to `Feature/Save-Diary-System/`
2. Type: "Load save-diary"
3. Choose your diary name (customizable to match your AI's personality)
4. Diary infrastructure auto-creates + skill installs if plugin system exists

**Benefits:**
- Complete searchable history of all AI sessions
- Growth tracking over time for both AI and user
- Never lose context about past work and decisions
- Self-documenting with minimal user effort
- Clean monthly archival keeps workspace organized

**Platform Note:** The diary system works with any AI platform. The included `SKILL.md` requires **Claude Code** (Anthropic's CLI tool) with the Skill Plugin System for auto-triggering. On other platforms, use the install protocol for manual setup.

*Based on proven daily documentation systems in production AI companions*

### **🔍 Echo Memory Recall**
*Search and recall past sessions with narrative context*

**What It Does:**
- Keyword-based search across all diary entries (current and archived months)
- Three-level recall: search + narrative, uncertainty guard, ask-user fallback
- Auto-triggers on natural phrases ("do you remember", "when did we", "recall")
- Presents search results as natural conversation, not raw database output
- Never fabricates past context — always searches diary evidence first

**Quick Setup:**
1. Navigate to `Feature/Echo-Memory-Recall/`
2. Type: "Load echo-recall"
3. Choose your recall system name (customizable to match your AI's personality)
4. Recall protocol installs into AI memory system — test with "Do you remember..."

**Benefits:**
- Long-term memory beyond the AI's context window
- Truthful recall backed by diary evidence
- Natural narrative responses that feel like genuine memory
- Graceful uncertainty handling (asks user when nothing found)
- Works with any diary format (Save-Diary-System or existing protocol)

**Requirement:** Requires `daily-diary/` with dated entries. Install Save-Diary-System first for best results.

**Platform Note:** Works with any AI system. Uses file reading for diary search — no platform-specific tools required.

*Based on proven memory recall systems in production AI companions*

### **🩹 Patch Update System**
*AI-executable patches for keeping your AI MemoryCore current*

**What It Does:**
- Introduces structured `.md` patch files that your AI reads and applies automatically
- Each patch contains find/replace instructions with exact text matching
- Tracks applied patches in `patches/applied.md` to prevent double-application
- Every patch includes rollback instructions for safe undo
- Supports conditional sections for pre/post Memory Consolidation compatibility

**Quick Setup:**
1. Navigate to `Feature/Patch-Update-System/`
2. Type: "Load patch-system"
3. Patch infrastructure auto-creates with tracking log
4. Any bundled patches are detected and offered for immediate application

**Benefits:**
- Zero manual editing — AI reads and applies patches through conversation
- Full traceability with application log and timestamps
- Safe rollback instructions included in every patch
- Dependency management prevents out-of-order application
- Human-readable markdown format — review before applying

**Available Commands:**
- `apply patch [ID]` - Read and apply a specific patch
- `check patches` - List available unapplied patches
- `patch status` - Show applied patches log

**Platform Note:** Works with any AI system that can read and write files. Patches are plain markdown — portable across any platform.

*Structured updates, tracked applications, safe rollbacks*

---

**Version**: 2.7 - Patch Update System
**Created by**: Kiyoraka Ken & Alice
**License**: Open Source Community Project
**Last Updated**: February 24, 2026 - Added Patch Update System with PATCH-001 (Fix Issue #1)
**Purpose**: Simple, effective AI memory for everyone

*Transform basic AI conversations into meaningful, growing relationships*