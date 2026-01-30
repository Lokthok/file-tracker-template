# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-30

### Added
- **Hash-based change detection** using MD5 content hashing
- Files are now compared by content, not just modification timestamps
- More reliable tracking with cloud sync services (OneDrive, Teams, Dropbox, etc.)

### Changed
- `material_inventory.json` now stores `hash` field for each file
- Change detection logic switched from `mtime` comparison to hash comparison
- `modified` timestamp kept for informational purposes but no longer used for change detection

### Fixed
- False positives when re-downloading identical files from cloud services
- Incorrect "changed" reports due to timestamp updates during file transfers
- Reliability issues with files synced via OneDrive/Teams/SharePoint

### Technical Details
- Added `get_file_hash()` function with MD5 implementation
- Hash computation uses 4KB chunks for memory efficiency
- No performance degradation for typical file counts (tested with 150+ files)

### Migration Notes
- First scan after update will report all existing files as "changed" (hash field missing in old inventory)
- Subsequent scans will work correctly with hash-based detection
- No manual migration needed – hashes are computed automatically

## [1.0.0] - 2026-01-29

### Added
- Initial release
- Recursive directory scanning
- JSON-based file inventory
- Markdown changelog reports
- Daily change grouping
- Detection of new, modified, and deleted files
- Smart daily report updates (multiple scans update same day's entry)
- Cross-platform support (Windows, macOS, Linux)

### Features
- No external dependencies (Python 3.x standard library only)
- Modular folder structure with numeric prefixes
- Hidden file/folder filtering
- Timezone-aware timestamps
- Human-readable reports

---

## Version History Summary

- **v1.1.0** (2026-01-30): Hash-based change detection for cloud sync reliability
- **v1.0.0** (2026-01-29): Initial public release
