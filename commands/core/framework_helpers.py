from commands.core.config import get_workspaces


def get_framework_specific_prompt(workspace, codebase_structure, file_description):
    config = get_workspaces()
    workspace_config = config["workspaces"].get(workspace, {})
    frameworks = workspace_config.get("frameworks", {})

    framework_prompts = []

    for name, framework_config in frameworks.items():
        framework_type = framework_config.get("type", "generic")
        framework_root = framework_config.get("root", "")

        if framework_type == "nextjs":
            framework_prompts.append(
                f"""
            For the {name} (Next.js) in {framework_root}:
            1. Pages are in {framework_root}/src/app or {framework_root}/src/pages
            2. Layout files are typically named layout.tsx
            3. Page components are typically named page.tsx
            4. Configuration files are often in {framework_root}/src/app
            or {framework_root}/src/config
            5. Special files like favicon.ico are in {framework_root}/public/
            """
            )
        elif framework_type == "django":
            framework_prompts.append(
                f"""
            For the {name} (Django) in {framework_root}:
            1. Views are in {framework_root}/views.py files
            2. URLs are in {framework_root}/urls.py files
            3. Templates are in {framework_root}/templates/
            4. Static files are in {framework_root}/static/
            5. Configuration is in {framework_root}/settings.py
            """
            )

    if not framework_prompts:
        framework_prompts.append(
            """
        This is a generic project, looking for common patterns:
        1. Configuration files in config/ or settings/ directories
        2. Main application files in src/ or app/ directories
        3. Common configuration file extensions (.json, .yaml, .env)
        """
        )

    return f"""
    Given this codebase structure: {codebase_structure}
    Find files matching: "{file_description}".
    This is a {"monorepo" if len(framework_prompts) > 1 else "project"} with
    the following frameworks:
    {"".join(framework_prompts)}
    When determining file types:
    1. For Next.js projects:
       - layout.tsx files are layout components
       - page.tsx files are page components
       - Other .tsx files in components/ are UI components
    2. For Django projects:
       - views.py files are view components
       - urls.py files are URL configurations
       - models.py files are database models
    Return the results in JSON format with the following structure:
    {{
        "results": [
            {{
                "file": "path/to/file",
                "context": "why it matches",
                "confidence_score": 0.0 to 1.0,
                "file_type": "component_type"  # e.g., "page", "layout",
                "view", "model"
            }}
        ]
    }}
    The response must use exactly this structure.
    """
