from typing import List, Dict
import os
from notion_client import Client
from datetime import datetime

import traceback


def get_notion_client() -> Client:
    """Initialize and return Notion client."""
    token = os.getenv("NOTION_API_TOKEN")
    if not token:
        raise ValueError("NOTION_API_TOKEN environment variable is not set")
    return Client(auth=token)


def extract_notion_properties(
    page: dict, properties_to_extract: List[str] = None
) -> dict:
    """
    Extract properties from a Notion page object.
    """
    if not page:
        return {}

    properties = page.get("properties", {})

    # Define all available property extractors with better null handling
    property_extractors = {
        "id": lambda p: p.get("id", ""),
        "url": lambda p: p.get("url", ""),
        "title": lambda p: next(
            (
                text.get("plain_text", "")
                for text in properties.get("Name", {}).get("title", [])
            ),
            "",
        ),
        "description": lambda p: next(
            (
                text.get("plain_text", "")
                for text in properties.get("Description", {}).get("rich_text", [])
            ),
            "",
        ),
        "status": lambda p: (
            properties.get("Resolution Details", {})
            .get("status", {})
            .get("name", "Unknown")
            if properties.get("Resolution Details")
            else "Unknown"
        ),
        "severity": lambda p: (
            properties.get("Severity Level", {})
            .get("select", {})
            .get("name", "Unknown")
            if properties.get("Severity Level")
            else "Unknown"
        ),
        "type": lambda p: (
            [
                t.get("name", "")
                for t in properties.get("Issue Type", {}).get("multi_select", [])
            ]
            if properties.get("Issue Type")
            else []
        ),
        "reporter": lambda p: next(
            (
                person.get("name", "")
                for person in properties.get("Reporter", {}).get("people", [])
            ),
            "",
        ),
        "assigned_to": lambda p: next(
            (
                person.get("name", "")
                for person in properties.get("Assigned To", {}).get("people", [])
            ),
            "",
        ),
        "date_reported": lambda p: (
            properties.get("Date Reported", {}).get("date", {}).get("start", "")
            if properties.get("Date Reported")
            and properties["Date Reported"].get("date")
            else ""
        ),
        "last_updated": lambda p: (
            properties.get("Last Updated", {}).get("date", {}).get("start", "")
            if properties.get("Last Updated") and properties["Last Updated"].get("date")
            else ""
        ),
    }

    # If no specific properties requested, extract all
    if properties_to_extract is None:
        properties_to_extract = list(property_extractors.keys())

    # Extract requested properties with error handling
    result = {}
    for prop in properties_to_extract:
        if prop in property_extractors:
            try:
                result[prop] = property_extractors[prop](page)
            except Exception as e:
                print(f"Error extracting property {prop}: {e}")
                result[prop] = ""

    return result


def list_tasks(database_id: str = None, properties: List[str] = None) -> List[Dict]:
    """List tasks from Notion database with proper property handling."""
    try:
        client = get_notion_client()
        if not database_id:
            database_id = os.getenv("NOTION_DATABASE_ID")
            if not database_id:
                raise ValueError("NOTION_DATABASE_ID environment variable is not set")

        response = client.databases.query(database_id=database_id)

        if not response:
            print("No response from Notion API")
            return []

        results = []
        for page in response.get("results", []):
            try:
                task = extract_notion_properties(page, properties)
                results.append(task)
            except Exception as e:
                print(f"Error processing page: {e}")
                continue

        return results

    except Exception as e:
        print(f"Error listing tasks: {e}")
        traceback.print_exc()
        return []


def create_bug_report(title: str, description: str = None, status: str = None):
    """Create a new bug report in Notion."""
    client = get_notion_client()
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not database_id:
        raise ValueError("NOTION_DATABASE_ID environment variable is not set")

    properties = {
        "Title": {"title": [{"text": {"content": title}}]},
        "Resolution Details": {"select": {"name": status}} if status else None,
        "Description": (
            {"rich_text": [{"text": {"content": description}}]} if description else None
        ),
        "Issue Type": {"select": {"name": "Bug"}},
        "Date Reported": {"date": {"start": datetime.now().isoformat()}},
    }

    # Remove None values
    properties = {k: v for k, v in properties.items() if v is not None}

    response = client.pages.create(
        parent={"database_id": database_id}, properties=properties
    )

    return response["id"]


def update_bug_status(bug_id: str, new_status: str):
    """Update the status of an existing bug."""
    client = get_notion_client()

    response = client.pages.update(
        page_id=bug_id,
        properties={"Resolution Details": {"select": {"name": new_status}}},
    )

    return response["id"]
