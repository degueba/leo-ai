# Bob, Your Personal AI Assistant
> A pattern for an always on AI Assistant powered by Deepseek-V3, RealtimeSTT, and Typer for engineering
>
> Checkout [the demo](https://youtu.be/zoBwIi4ZiTA) where we walk through using this always-on-ai-assistant.

![leo_ai_deepseek.jpg](./images/leo_ai_deepseek.jpg)

## Setup
- `cp .env.sample .env`
  - Update with your keys `DEEPSEEK_API_KEY` and `ELEVEN_API_KEY`
- `uv sync`
- (optional) install python 3.11 (`uv python install 3.11`)
- Install VS Code Tasks Runner extension (optional but recommended)

## Workflow Overview

The Bob AI Assistant follows a structured workflow to help you with development tasks:

1. **Awakening the Assistant**  
   - The assistant starts in a listening state, ready to receive voice commands
   - It uses RealtimeSTT to convert speech to text
   - Commands are processed through Deepseek-V3 for understanding

2. **Command Processing**  
   - The assistant analyzes the command using the Typer command framework
   - It determines the appropriate action based on the command structure
   - Commands can be either direct execution or planning tasks

3. **Task Execution**  
   - For execution commands, the assistant:
     - Generates the necessary code or configuration
     - Updates the scratchpad with the current state
     - Executes the command through the Typer interface
   - For planning tasks, it:
     - Creates a detailed plan in the scratchpad
     - Waits for user confirmation before execution

4. **Feedback Loop**  
   - The assistant maintains state in the scratchpad.md file
   - You can review and modify the scratchpad between commands
   - The assistant uses this context for subsequent commands

5. **VS Code Integration**  
   - Preconfigured tasks are available in VS Code:
     - Agent: Awaken - Starts the assistant in execute mode
     - Agent: Plan - Starts the assistant in planning mode
     - Agent: Execute - Runs the assistant in execution mode
   - Access these tasks through the VS Code Command Palette (Ctrl+Shift+P) or Task Runner

## Workspace Configuration

The assistant uses a workspace configuration file (`workspace_config.json`) to manage project settings:

```json
{
    "current_workspace": "your_workspace_name",
    "workspaces": {
        "your_workspace_name": {
            "path": "/path/to/your/workspace",
            "frameworks": {
                "frontend": {
                    "type": "nextjs",
                    "root": "frontend"
                },
                "backend": {
                    "type": "django",
                    "root": "backend"
                }
            }
        }
    },
    "exclude_dirs": [
        "node_modules",
        ".venv",
        "venv",
        ".git",
        "dist",
        "build",
        "coverage",
        ".idea",
        ".vscode",
        ".cursor",
        "api",
        ".next",
        ".cache"
    ],
    "include_file_types": [
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".py",
        ".java",
        ".html",
        ".css",
        ".json"
    ]
}
```

## Available Commands

### Core Commands
1. **show_config**
   - Displays the assistant configuration
   - Usage: `show_config [--verbose]`
   - Options:
     - `--verbose`: Show detailed configuration

2. **list_files**
   - Lists files in a directory
   - Usage: `list_files <path> [--all]`
   - Arguments:
     - `path`: Path to list files from
   - Options:
     - `--all`: Include hidden files

3. **diff_files**
   - Shows differences between two files
   - Usage: `diff_files <file_a> <file_b> [--diff-only]`
   - Arguments:
     - `file_a`: First file to compare
     - `file_b`: Second file to compare
   - Options:
     - `--diff-only`: Show only differences

4. **edit_file**
   - Opens a file for editing based on description
   - Usage: `edit_file <file_description> [--workspace WORKSPACE]`
   - Arguments:
     - `file_description`: Description of file to edit
   - Options:
     - `--workspace`: Specify workspace to use



### Framework-Specific Features
The workspace supports both Next.js (frontend) and Django (backend) frameworks:

**Next.js Features:**
- Pages in `frontend/src/app` or `frontend/src/pages`
- Layout files named `layout.tsx`
- Page components named `page.tsx`
- Configuration files in `frontend/src/app` or `frontend/src/config`
- Static files in `frontend/public/`

**Django Features:**
- Views in `backend/views.py`
- URLs in `backend/urls.py`
- Templates in `backend/templates/`
- Static files in `backend/static/`
- Configuration in `backend/settings.py`

## Integrations & Integrations Commands
## Notion Integration
### Bug Tracker Setup
To use the Notion integration:

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Copy the integration token
3. Add the token to your `.env` file as `NOTION_API_TOKEN`
4. Share your Notion database with the integration
5. Copy your database ID (from the database URL) and add it to `.env` as `NOTION_DATABASE_ID`

The database ID is the part of your Notion database URL after the workspace name and before the question mark:
```
https://notion.so/workspace/83jk2h3d-721d-4892-8827-9e2d0b8f5d9e?v=...
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        This is your database ID
```

### Database Structure
The integration expects a Notion database with the following properties:
- Title (title) - Bug report title
- Resolution Details (select) - Status of the bug
- Reporter (rich text) - Who reported the bug
- Description (rich text) - Detailed bug description
- Severity Level (select) - Bug severity
- Date Reported (date) - When the bug was reported
- Issue Type (select) - Type of issue (defaults to "Bug")

### Available Commands
1. **list_notion_tasks**
   - Lists all bugs from your Notion database
   - Usage: `list_notion_tasks [--database-id ID] [--show-url] [--status STATUS]`
   - Options:
     - `--database-id`: Optional Notion database ID (defaults to NOTION_DATABASE_ID env var)
     - `--show-url`: Show Notion page URLs for each task
     - `--status`: Filter bugs by status

2. **create_bug_report**
   - Creates a new bug report in Notion
   - Usage: `create_bug_report <title> [--description DESC] [--status STATUS]`
   - Arguments:
     - `title`: Bug report title
   - Options:
     - `--description`: Detailed bug description
     - `--status`: Initial status

3. **update_bug_status**
   - Updates the status of an existing bug
   - Usage: `update_bug_status <bug_id> <new_status>`
   - Arguments:
     - `bug_id`: Notion page ID of the bug
     - `new_status`: New status to set

### Example Usage
```bash
# List all bugs
python commands/template.py list-notion-tasks

# List bugs with URLs
python commands/template.py list-notion-tasks --show-url

# List bugs with specific status
python commands/template.py list-notion-tasks --status "Can't Reproduce"

# Create a new bug report
python commands/template.py create-bug-report "Login button not working" --description "Users cannot click the login button" --status "Open"

# Update bug status
python commands/template.py update-bug-status "83jk2h3d-721d-4892-8827-9e2d0b8f5d9e" "In Progress"
```

### Environment Variables
Required environment variables in your `.env` file:
```bash
NOTION_API_TOKEN=your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

## Resources
- LOCAL SPEECH TO TEXT: https://github.com/KoljaB/RealtimeSTT
- faster whisper (support for RealtimeSTT) https://github.com/SYSTRAN/faster-whisper
- whisper https://github.com/openai/whisper
- examples https://github.com/KoljaB/RealtimeSTT/blob/master/tests/realtimestt_speechendpoint_binary_classified.py
- elevenlabs voice models: https://elevenlabs.io/docs/developer-guides/models#older-models