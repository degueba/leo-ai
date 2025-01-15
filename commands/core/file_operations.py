import os

from .config import get_workspaces


def _cache_recent_file(file_path):
    RECENT_FILES_CACHE = os.path.join(os.path.dirname(__file__), ".recent_files")
    with open(RECENT_FILES_CACHE, "a") as f:
        f.write(f"{file_path}\n")


def _get_recent_files():
    RECENT_FILES_CACHE = os.path.join(os.path.dirname(__file__), ".recent_files")
    if os.path.exists(RECENT_FILES_CACHE):
        with open(RECENT_FILES_CACHE, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []


def get_codebase_structure(root_path, max_files=100):
    """Get codebase structure with configurable exclusions"""
    config = get_workspaces()
    exclude_dirs = set(config.get("exclude_dirs", []))
    include_types = set(config.get("include_file_types", []))

    structure = []
    file_count = 0

    for root, dirs, files in os.walk(root_path):
        # Filter out unwanted directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

        for file in files:
            if not file.startswith(".") and any(
                file.endswith(ext) for ext in include_types
            ):
                rel_path = os.path.relpath(os.path.join(root, file), root_path)
                structure.append(rel_path)
                file_count += 1
                if file_count >= max_files:
                    return structure
    return structure
