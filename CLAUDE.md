# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python service that automatically adds pinyin sorting and date metadata to Chinese media titles in Jellyfin/Emby media servers. It runs as a Docker container that periodically scans media libraries and updates item metadata via the Jellyfin/Emby API.

## Development Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test individual components
python -c "from src.PinyinUtil import PinyinUtil; print(PinyinUtil.get_pingyin('测试'))"
python -c "from src.DateUtil import DateUtil; print(DateUtil.extract_date_from_filename('[2024-03] test.mp4'))"

# Run the main service (requires environment variables)
python src/JellyfinHandler.py
```

## Docker Build

```bash
# Build from project root directory
docker build -f src/Dockerfile -t jellyfin_pinyin .

# Multi-platform builds (from src/ directory)
docker build -t wizzer/jellyfin_pinyin:v2.1 . --platform=linux/amd64
docker build -t wizzer/jellyfin_pinyin:v2.1_arm . --platform=linux/arm64
```

## Architecture

### Core Components

- **JellyfinHandler.py**: Main orchestrator that manages the scanning lifecycle, loads configuration from environment variables, and coordinates all processing
- **JellyfinUtil.py**: Jellyfin/Emby API wrapper with methods for getting users, media libraries, items, and updating metadata
- **PinyinUtil.py**: Chinese text to pinyin conversion utilities using pypinyin library
- **DateUtil.py**: Extracts dates from video filenames in `[YYYY-MM]` format and formats them for Jellyfin API

### Processing Flow

1. Load configuration from environment variables (URL, API_KEY, MEDIA libraries, TIME interval)
2. Get admin user ID from Jellyfin/Emby
3. Retrieve media library views, optionally filtered by MEDIA setting
4. For each library, recursively process items:
   - Folders: recurse into contents
   - Media objects: extract pinyin for SortName, extract dates from filename, update via API
5. Handle special cases for music libraries (albums and artists)
6. Emby-specific: lock metadata fields to prevent overwrites

### Key Behaviors

- **Automatic date extraction**: Videos with filenames like `[2024-03] movie.mp4` get PremiereDate set to `2024-03-01T00:00:00.0000000` and ProductionYear to `2024`
- **Emby vs Jellyfin**: Emby requires `LockedFields` to prevent metadata overwrites; detection is based on "emby" in the domain URL
- **Skip logic**: Items with existing correct pinyin sorting are automatically skipped to avoid unnecessary API calls
- **Periodic execution**: After initial run, service sleeps for TIME seconds (default 3600) before next scan

## Environment Variables

- `URL`: Jellyfin/Emby server address (e.g., `http://127.0.0.1:8096` or `http://127.0.0.1:8096/emby`)
- `KEY`: API key from Jellyfin/Emby admin panel
- `MEDIA`: Comma-separated library names to process (empty = all libraries)
- `TIME`: Scan interval in seconds (default: 3600)

## Important Implementation Details

- All API timeouts are set to 3 seconds (3000ms converted to seconds)
- Pinyin sorting names are truncated to 50 characters maximum
- The service includes a 10-second startup delay to ensure Jellyfin/Emby is ready
- Date extraction only processes filenames starting with `[YYYY-MM]` pattern
- Music libraries have special handling for both albums (`get_music_items`) and artists (`get_artists`)