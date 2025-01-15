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


def get_codebase_structure(root_path, use_cache=True):
    """Generate a compact tree representation of the codebase structure with caching"""
    # Generate a cache key based on the root path and modification time
    cache_key = f"structure_{os.path.basename(root_path)}"
    cache_file = os.path.join(os.path.dirname(__file__), ".structure_cache")

    if use_cache:
        # Check if we have a cached structure
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                cached_data = f.read()
                if cached_data.startswith(cache_key):
                    return cached_data[len(cache_key) + 1 :]

    # Generate fresh structure if no cache or cache is invalid
    config = get_workspaces()
    exclude_dirs = set(config.get("exclude_dirs", []))
    include_types = set(config.get("include_file_types", []))

    def build_tree(path, prefix=""):
        if os.path.basename(path) in exclude_dirs:
            return ""

        if os.path.isfile(path):
            if any(path.endswith(ext) for ext in include_types):
                return f"{prefix}📄 {os.path.basename(path)}\n"
            return ""

        output = f"{prefix}📁 {os.path.basename(path)}\n"
        try:
            contents = sorted(os.listdir(path))
            for i, item in enumerate(contents):
                is_last = i == len(contents) - 1
                new_prefix = prefix + ("└── " if is_last else "├── ")
                output += build_tree(os.path.join(path, item), new_prefix)
        except PermissionError:
            pass
        return output

    structure = build_tree(root_path).strip()

    # Cache the structure with the cache key
    with open(cache_file, "w") as f:
        f.write(f"{cache_key}:{structure}")

    return structure
