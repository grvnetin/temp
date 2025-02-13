jira_issues = []
for issue in jira_issues_data.get("issues", []):
    fields = issue.get("fields", {})
    jira_issues.append({
        "Key": issue.get("key"),
        "Summary": fields.get("summary", "No summary provided"),
        "Status": fields.get("status", {}).get("name", "Unknown"),
        "Issue Type": fields.get("issuetype", {}).get("name", "Unknown"),
        "Assignee": fields.get("assignee", {}).get("displayName", "Unassigned"),
        "Reporter": fields.get("reporter", {}).get("displayName", "Unknown"),
        "Story Points": fields.get("customfield_10016", None),
        "FixVersion": JIRA_FIX_VERSION,
        "Sprint": fields.get("customfield_10007", [{}])[0].get("name", "Not Assigned"),
        "Priority": fields.get("priority", {}).get("name", "Not Set"),
        "Components": [component.get("name", "Unknown") for component in fields.get("components", [])],
        "Labels": fields.get("labels", []),
        "Resolution": fields.get("resolution", {}).get("name", "Unresolved"),
        "Created": fields.get("created"),
        "Updated": fields.get("updated"),
        "Description": fields.get("description", "No description provided"),
        "Linked Issues": [link.get("inwardIssue", {}).get("key", "N/A") for link in fields.get("issuelinks", []) if "inwardIssue" in link]
    })
