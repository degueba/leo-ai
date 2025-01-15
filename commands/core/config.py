import os
import json
from typing import Dict, Any

# Constants
WORKSPACE_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "workspace_config.json",
)


def get_workspaces() -> Dict[str, Any]:
    """Get all workspaces configuration"""
    print(f"DEBUG: Looking for workspace config at: {WORKSPACE_CONFIG}")
    try:
        if os.path.exists(WORKSPACE_CONFIG):
            with open(WORKSPACE_CONFIG, "r") as f:
                config = json.load(f)
                print(f"DEBUG: Config loaded successfully: {config}")
                return config
        print("DEBUG: No workspace config found, returning empty config")
        return {"workspaces": {}}
    except Exception as e:
        print(f"DEBUG: Error loading config: {str(e)}")
        return {"workspaces": {}}


def get_workspace(name: str) -> Dict[str, Any]:
    """Get configuration for a specific workspace"""
    config = get_workspaces()
    workspace = config["workspaces"].get(name, {})
    if workspace:
        # Ensure the path is absolute
        workspace["path"] = os.path.abspath(os.path.expanduser(workspace["path"]))
    return workspace
