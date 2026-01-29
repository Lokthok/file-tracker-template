# File Tracker Template

[![AI-Assisted Development](https://img.shields.io/badge/Development-AI--Assisted-blue)]()
[![Python 3.x](https://img.shields.io/badge/Python-3.x-green)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> A universal file tracking system that monitors directories, detects changes, and generates changelog-style reports – without forcing you into rigid folder structures or naming conventions.

## The Problem

Whether you're:
- 📚 Managing course materials with frequent updates
- 📸 Organizing photo backups across multiple devices
- 📥 Tracking downloads without manual sorting
- 🗂️ Monitoring project assets

...you face the same challenge: **How do you know what's new without constantly checking file dates or restructuring folders?**

Traditional solutions require rigid organization or manual file naming. This template offers a different approach: **automatic tracking with human-readable reports**.

## The Solution

A lightweight Python script that:
- ✅ Scans directories recursively and tracks all files
- ✅ Maintains a JSON-based inventory with timestamps
- ✅ Generates changelog-style Markdown reports (newest first)
- ✅ Groups changes by day – one entry per scan session
- ✅ Detects new, modified, and deleted files automatically
- ✅ Works universally – adapt folder names to your use case

**No database required. No complex setup. Just Python 3.x.**

## Quick Start

1. **Clone or use this template**
```bash
   git clone https://github.com/yourusername/file-tracker-template.git
   cd file-tracker-template
```

2. **Adjust folder names** (optional)
    - `00-archive/` – Your main directory to track
    - `10-active/` – Working files
    - `20-completed/` – Finished items
3. **Edit configuration** in `track_material.py`

```python
ARCHIVEDIR = BASEDIR / "00-archive"  # Change to your target folder
```

4. **Run the tracker**

```bash
python3 track_material.py
```

5. **Check the report**
    - Open `00-scan-report.md` – see what's new today
    - Check `material_inventory.json` – full file database

## Use Cases

This template adapts to many scenarios:

### 📚 Course Materials (Original Use Case)

- **Track daily uploads** from learning platforms (Teams, Moodle, etc.)
- See at a glance what lectures/assignments are new
- **Preserve originals as pristine backups** – work only with copies
- Archive completed modules without losing history
- Share clean, unmodified materials with classmates easily
- Never accidentally distribute your solved assignments or notes

**Workflow:** Download → Track with script → Copy to `10-active/` → Work on copies → Archive when done. Your `00-archive/` stays pristine for backups or sharing.

### 📸 Photo Management

- Monitor photo imports from multiple devices
- Track backups without renaming files
- Detect duplicates or missing files


### 📥 Download Monitoring

- Keep tabs on your Downloads folder chaos
- See what you downloaded when
- Archive processed files with history


### 🗂️ Project Assets

- Track resource updates in collaborative projects
- Monitor shared folders for team changes
- Maintain changelog without manual documentation


### 💾 Backup Verification

- Verify backup completeness
- Detect file corruption (via size/modification changes)
- Document backup history automatically
- **...or invent your own use case – let your creativity run wild!**


## Project Structure

```
file-tracker-template/
├── 00-archive/                 # Main directory to track
├── 10-active/                  # Currently working on
├── 20-completed/               # Finished items
├── 10-progress-tracker.md      # Manual notes, todos, reflections (optional)
├── 00-scan-report.md           # Auto-generated changelog report
├── material_inventory.json     # Auto-generated file database
└── track_material.py           # Main tracking script
```

**Naming Convention Notes:**

- Folders prefixed with numbers (`00-`, `10-`, `20-`) sort first in file explorers
- Files prefixed with numbers (`00-`, `10-`) float to the top for easy access
- Both `00-`, `10-` files sort together – your "dashboard" stays at the top
- Script and JSON files have no prefix – they sort below your important docs
- Use 10-step increments (00, 10, 20) to leave room for future additions

**About `10-progress-tracker.md`:**
This is YOUR manual workspace for:

- Tracking which modules you've completed
- Writing todos and study notes
- Documenting your learning journey
- Planning next steps

The script ignores it – it's purely for human use. Think of it as your project journal that lives alongside the automated reports.

## How It Works

1. **Scanning**: Recursively walks `00-archive/` and catalogs all files
2. **Comparison**: Compares current scan against `material_inventory.json`
3. **Detection**: Identifies new, modified (size/date changed), and deleted files
4. **Reporting**: Generates/updates `00-scan-report.md` with today's changes
5. **History**: Maintains changelog – one entry per day, newest first
6. **Progress Tracking** (optional): Use `10-progress-tracker.md` to manually document your sorting progress, todos, notes, or learning reflections

**What We Track Per File:**

- `added`: When you first ran the script and it found this file
- `size`: File size in bytes
- `modified`: File system's "last modified" timestamp
- `changed`: When we detected the file had changed (size or timestamp different)

**Smart Changelog:**

- Running multiple scans on the same day updates the same entry
- No redundant entries – clean daily summaries
- Old entries preserved – full historical record


## Design Philosophy

### Simplicity by Design

This tool does **one thing well**: track files and report changes. That's intentional.

**What we deliberately left out:**

- ❌ Real-time monitoring (file watchers, daemons)
- ❌ Minute-by-minute timestamps
- ❌ Complex filtering rules or regex patterns
- ❌ Database backends or web interfaces
- ❌ Cloud sync or notifications

**Why?**

- **Lower barrier to entry** – just Python, no dependencies
- **Easier to understand** – read the code in 10 minutes
- **Harder to break** – fewer moving parts
- **More maintainable** – you can fix it yourself
- **More portable** – works anywhere Python runs

The challenge wasn't making it complex. The challenge was keeping it simple enough that anyone can use it, understand it, and adapt it to their needs.

**Philosophy:** Tools should solve problems, not create new ones. Adding features is easy. Knowing which features to leave out – that's the hard part.

### Why Daily Granularity?

This tool operates on a **daily rhythm by design**, not hourly or by-the-minute:

**Cognitive Benefits:**

- Reduces decision fatigue from constant micro-decisions
- Prevents cognitive overload from excessive detail
- Enables pattern recognition over time (not noise)

**Practical Benefits:**

- Aligns with natural work rhythms (daily reviews are proven effective)
- Focuses on outcomes, not timekeeping
- Simplifies mental model – "What changed today?" not "What changed at 2:47pm?"

**Why No Timestamps?**
We deliberately omit exact discovery times because:

- **You don't need them** – knowing something arrived "today" is sufficient
- **They create clutter** – 15 entries all from the same day with timestamps are harder to scan than one consolidated entry
- **They encourage over-monitoring** – checking constantly defeats the purpose of automation

This isn't a surveillance tool. It's a **sanity-preservation tool** that respects your time and cognitive load.

If you need minute-by-minute tracking, this isn't the right tool – and that's intentional.

## Customization

### Change Tracked Directory

Edit line 15 in `track_material.py`:

```python
ARCHIVE_DIR = BASE_DIR / "your-folder-name"
```


### Rename Output Files

Edit lines 16-17:

```python
INVENTORYFILE = BASEDIR / "your-inventory.json"
REPORTFILE = BASEDIR / "your-report.md"
```


### Modify Folder Structure

Rename folders to fit your workflow:

- `inbox/` instead of `00-archive/`
- `processing/` instead of `10-active/`
- `done/` instead of `20-completed/`

The script only tracks `00-archive/` by default – other folders are just organizational suggestions.

## Requirements

- **Python 3.x** (tested on 3.10+)
- **Standard library only** – no external dependencies
- **Cross-platform** – works on Windows, macOS, Linux

> **Design Note:** The lack of dependencies isn't laziness – it's intentional. Tools that do one thing well, with no external moving parts, are easier to understand, debug, and maintain. Simplicity is a feature, not a limitation.

## Installation

No installation needed! Just:

1. Have Python 3.x installed
2. Download/clone this template
3. Run the script

## Development Story

### Context

This project emerged from a real need during my **vocational retraining in software development**. Managing course materials that updated frequently became overwhelming – I needed a system that could track changes automatically without forcing me into rigid folder structures.

### Approach

Rather than spending weeks building this from scratch while juggling coursework, I used **AI-assisted development** (Perplexity AI) as a force multiplier. This allowed me to:

- Focus on **system design and architecture**
- Iterate rapidly on requirements and edge cases
- Deliver a working solution in hours instead of weeks
- Maintain full understanding of the codebase


### Why This Matters

**AI is a tool, not a replacement.** Using it effectively requires:

- Clear problem identification
- Solid architectural thinking
- Ability to guide and validate AI output
- Understanding the generated code for maintenance and debugging

I believe the future of development isn't about typing every line manually – it's about **working smarter, delivering results faster, and solving real problems efficiently**. That said, understanding remains critical.

### The Balance

This project represents my philosophy on modern development:

- ✅ Use AI to accelerate implementation
- ✅ Maintain code comprehension for quality control and maintenance
- ✅ Prioritize results and problem-solving over manual labor
- ✅ Keep learning – understanding the "why" behind the code

**My Current Level:** I'm 7 months into a 2-year vocational retraining program (started June 25, 2025). I understand the core logic, structure, and flow of this code, though I'm still deepening my knowledge of Python's standard libraries and best practices. I can debug, modify, and extend this project – and importantly, I know when I need to look something up or ask for clarification. That's not a weakness; that's how professional developers actually work.

Blindly insisting on typing every character when AI can assist is neither competitive nor sustainable. But blindly trusting AI output without understanding is equally dangerous. **The balance matters.**

### Learning Project → Real Tool

What started as a personal learning project turned out to be genuinely useful beyond my immediate needs. Since the solution appears universal, I'm open-sourcing it.

**Feedback, suggestions, improvements, and critique are highly welcome.** If you find this useful or have ideas for enhancements, please open an issue or pull request!

## Contributing

This is a learning project that turned into a real tool. Contributions are welcome:

- 🐛 Bug reports
- 💡 Feature suggestions
- 🔧 Code improvements
- 📖 Documentation enhancements

Please open an issue or pull request – I'm here to learn and improve!

## License

MIT License – use freely, modify as needed, share improvements.

See [LICENSE](LICENSE) for full details.

## Author

**[Your Name]** – Currently in vocational retraining for software development

*This project demonstrates modern development practices: using AI tools effectively while maintaining code understanding, focusing on problem-solving over manual labor, and sharing solutions that might help others.*

## Acknowledgments

Developed with AI assistance from Perplexity AI. The problem identification, system architecture, testing, and quality assurance were human-driven. The implementation benefited from AI-accelerated development.

## Future Ideas

Considering for future versions:
- Configuration file support (YAML/JSON)
- Ignore patterns for files/folders
- Statistics and upload rhythm analysis

Feedback and suggestions welcome via issues!
