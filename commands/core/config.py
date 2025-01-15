import os
import json
from typing import Dict, Any

# Constants
WORKSPACE_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "workspace_config.json"
)


# Existing functions
def get_workspaces() -> Dict[str, Any]:
    """Get all workspaces configuration"""
    if os.path.exists(WORKSPACE_CONFIG):
        with open(WORKSPACE_CONFIG, "r") as f:
            return json.load(f)
    return {"workspaces": {}}


# New functions
def get_workspace(name: str) -> Dict[str, Any]:
    """Get configuration for a specific workspace"""
    config = get_workspaces()
    return config["workspaces"].get(name, {})
