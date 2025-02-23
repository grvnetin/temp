import json
import logging
from operator import itemgetter

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SPRINT_DATA_FILE_NAME = 'sprint_data.json'

# Generate Markdown Reports
def generate_markdown(issues):
    project_groups = {}
    
    # Group issues by project
    for issue in issues:
        fields = issue.get("fields", {})
        project = fields.get("project", {})
        issue_key = issue.get("key", "Unknown")
        fix_version = fields.get("fixVersions", [{}])[0].get("name", "Unknown")
        project_key = project.get("key", "Uncategorized")
        issue_type = fields.get("issuetype", {}).get("name", "Unknown")
        summary = fields.get("summary", "No Summary")
        priority = fields.get("priority", {}).get("name", "Not Set")
        issue_link = f"[**{issue_key}**](#{issue_key.lower()})"
        
        # Store issue data
        issue_data = {
            "issue_type": issue_type,
            "issue_key": issue_link,
            "summary": summary,
            "priority": priority,
            "fix_version": fix_version
        }
        
        if project_key not in project_groups:
            project_groups[project_key] = []
        project_groups[project_key].append(issue_data)

    # Generate Markdown content
    markdown_reports = {}
    
    # Extract YYYY_SprintMM from the first issue's fix version
    if issues:
        first_fix_version = issues[0].get("fields", {}).get("fixVersions", [{}])[0].get("name", "Unknown")
        sprint_header = first_fix_version.split("-")[0] if first_fix_version != "Unknown" else "Unknown"
    else:
        sprint_header = "Unknown"

    markdown_content = f"# {sprint_header} Sprint Summary\n\n"

    # Generate markdown for each project
    for project_key, project_issues in project_groups.items():
        # Sort issues by fix version in descending order
        project_issues.sort(key=itemgetter("fix_version"), reverse=True)

        markdown_content += f"## {project_key}\n\n"
        markdown_content += "| Issue Type | Issue Key | Summary | Priority | Fix Version |\n"
        markdown_content += "|------------|-----------|---------|----------|-------------|\n"

        for issue in project_issues:
            markdown_content += (
                f"| {issue['issue_type']} | {issue['issue_key']} | {issue['summary']} | {issue['priority']} | {issue['fix_version']} |\n"
            )

        markdown_content += "\n"

    logger.debug(markdown_content)
    return markdown_content

# Save Markdown file
def save_markdown(content, filename="jira_release_report.md"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)
    logger.info(f"Markdown report saved: {filename}")

# Example usage
if __name__ == "__main__":
    with open(SPRINT_DATA_FILE_NAME, "r") as file:
        issues = json.load(file)
    markdown_content = generate_markdown(issues)
    save_markdown(markdown_content)
