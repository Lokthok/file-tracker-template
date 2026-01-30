#!/usr/bin/env python3

"""
Material Inventory Tracker
Scans 00-archive/ and detects new/changed/deleted files.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
ARCHIVE_DIR = BASE_DIR / "00-archive"
INVENTORY_FILE = BASE_DIR / "material_inventory.json"
REPORT_FILE = BASE_DIR / "00-scan-report.md"


def get_file_hash(filepath):
    """Calculate MD5 hash of file content."""
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_file_info(filepath):
    """Returns file size, modification timestamp, and content hash."""
    stat = filepath.stat()
    return {
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "hash": get_file_hash(filepath)
    }


def scan_archive():
    """Scans ARCHIVE_DIR and returns dict with all files."""
    files = {}
    if not ARCHIVE_DIR.exists():
        print(f"❌ Error: {ARCHIVE_DIR} does not exist!")
        return files

    for root, dirs, filenames in os.walk(ARCHIVE_DIR):
        # Skip hidden folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

        for filename in filenames:
            # Skip hidden files and Python cache
            if filename.startswith('.') or filename.endswith('.pyc'):
                continue

            filepath = Path(root) / filename
            rel_path = str(filepath.relative_to(ARCHIVE_DIR))
            files[rel_path] = get_file_info(filepath)

    return files


def load_inventory():
    """Loads existing inventory."""
    if INVENTORY_FILE.exists():
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_inventory(inventory):
    """Saves inventory."""
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False, sort_keys=True)


def write_report(stats):
    """Writes/updates Markdown report in changelog style."""
    today_date = datetime.now().strftime("%Y-%m-%d")
    today_full = stats['timestamp']

    # Load existing report and parse today's entry
    existing_entries = []
    today_existing = {'new': set(), 'changed': set(), 'deleted': set()}

    if REPORT_FILE.exists():
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract changelog entries
        if "## Changelog" in content:
            changelog_part = content.split("## Changelog", 1)[1]

            # Split individual entries by "### 📅"
            entries = changelog_part.split("### 📅 ")
            for entry in entries[1:]:  # First is empty
                if entry.strip():
                    # Check if today's entry
                    if entry.startswith(today_date):
                        # Parse today's entry to extract files
                        lines = entry.split('\n')
                        current_section = None
                        for line in lines:
                            if '**🆕 New Files' in line:
                                current_section = 'new'
                            elif '**🔄 Changed Files' in line:
                                current_section = 'changed'
                            elif '**🗑️ Deleted Files' in line:
                                current_section = 'deleted'
                            elif line.strip().startswith('- `') and current_section:
                                # Extract file
                                filepath = line.strip()[3:-1]  # Remove "- `" and "`"
                                today_existing[current_section].add(filepath)
                    else:
                        # Old entry (not today)
                        existing_entries.append("### 📅 " + entry.strip())

    # Add new changes to today's
    all_new = today_existing['new'] | set(stats['new'])
    all_changed = today_existing['changed'] | set(stats['changed'])
    all_deleted = today_existing['deleted'] | set(stats['deleted'])

    # Write new report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Material Scan Report\n\n")
        f.write(f"**Last Scan:** {today_full}\n\n")
        f.write(f"<br>\n\n")

        # Summary (current state)
        f.write(f"## Summary\n\n")
        f.write(f"- 📁 **Total:** {stats['total']} files in `{ARCHIVE_DIR.name}/`\n")
        f.write(f"- 🆕 **New today:** {len(all_new)}\n")
        f.write(f"- 🔄 **Changed today:** {len(all_changed)}\n")
        f.write(f"- 🗑️ **Deleted today:** {len(all_deleted)}\n\n")
        f.write(f"<br>\n\n")

        # Changelog
        f.write(f"## Changelog\n\n")

        # Today's entry (collected)
        if all_new or all_changed or all_deleted:
            f.write(f"### 📅 {today_date}\n\n")

            if all_new:
                f.write(f"**🆕 New Files ({len(all_new)}):**\n\n")
                for file in sorted(all_new):
                    f.write(f"- `{file}`\n")
                f.write(f"\n")

            if all_changed:
                f.write(f"**🔄 Changed Files ({len(all_changed)}):**\n\n")
                for file in sorted(all_changed):
                    f.write(f"- `{file}`\n")
                f.write(f"\n")

            if all_deleted:
                f.write(f"**🗑️ Deleted Files ({len(all_deleted)}):**\n\n")
                for file in sorted(all_deleted):
                    f.write(f"- `{file}`\n")
                f.write(f"\n")

            f.write(f"<br>\n\n")

        # Append old entries (from other days)
        for entry in existing_entries:
            f.write(entry)
            f.write(f"\n\n<br>\n\n")


def main():
    print(f"🔍 Scanning {ARCHIVE_DIR.name}/...")

    # Run current scan
    current_files = scan_archive()
    if not current_files:
        print(f"⚠️ No files found in {ARCHIVE_DIR.name}/")
        return

    # Load existing inventory
    old_inventory = load_inventory()

    # Build new inventory
    new_inventory = {}
    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Lists for report
    stats = {
        'timestamp': today,
        'total': len(current_files),
        'new': [],
        'changed': [],
        'unchanged': [],
        'deleted': []
    }

    # Process currently found files
    for filepath, fileinfo in current_files.items():
        if filepath not in old_inventory:
            # New file
            new_inventory[filepath] = {
                "added": today,
                "size": fileinfo["size"],
                "modified": fileinfo["modified"],
                "hash": fileinfo["hash"]
            }
            stats['new'].append(filepath)
        else:
            # File exists - check if changed (by hash)
            old_info = old_inventory[filepath]
            if fileinfo["hash"] != old_info.get("hash"):
                # File changed (content is different)
                new_inventory[filepath] = {
                    "added": old_info.get("added", "unknown"),
                    "changed": today,
                    "size": fileinfo["size"],
                    "modified": fileinfo["modified"],
                    "hash": fileinfo["hash"]
                }
                stats['changed'].append(filepath)
            else:
                # Unchanged (update metadata but keep history)
                new_inventory[filepath] = {
                    "added": old_info.get("added", "unknown"),
                    "size": fileinfo["size"],
                    "modified": fileinfo["modified"],
                    "hash": fileinfo["hash"]
                }
                if "changed" in old_info:
                    new_inventory[filepath]["changed"] = old_info["changed"]
                stats['unchanged'].append(filepath)

    # Find deleted files
    stats['deleted'] = [f for f in old_inventory if f not in current_files]

    # Save inventory
    save_inventory(new_inventory)

    # Write report
    write_report(stats)

    # Console output (brief)
    print(f"✅ Scan completed: {today}")
    if stats['new'] or stats['changed'] or stats['deleted']:
        print(f"📊 {stats['total']} files | 🆕 {len(stats['new'])} new | 🔄 {len(stats['changed'])} changed | 🗑️ {len(stats['deleted'])} deleted")
    else:
        print(f"📊 {stats['total']} files | ✅ No changes")
    print(f"📄 Report: {REPORT_FILE.name}")


if __name__ == "__main__":
    main()
