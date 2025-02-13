def extract_text_from_description(description):
    """Recursively extract all text where type is 'text' and format lists properly."""
    if not description:
        return "No description available."

    extracted_text = []
    
    def recursive_extract(content, prefix=""):
        if isinstance(content, list):
            for item in content:
                recursive_extract(item, prefix)
        elif isinstance(content, dict):
            if content.get("type") == "text":
                extracted_text.append(prefix + content.get("text", ""))
            elif content.get("type") == "listItem":
                recursive_extract(content.get("content", []), prefix="- ")  # Bullet point format
            elif content.get("type") in ["paragraph", "bulletList", "orderedList"]:
                recursive_extract(content.get("content", []))

    recursive_extract(description.get("content", []))

    return "\n".join(extracted_text)

# Example Usage
jira_description = {
    "type": "doc",
    "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": "This is the first line."}]},
        {"type": "paragraph", "content": [{"type": "text", "text": "This is the second line."}]},
        {"type": "bulletList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Bullet point 1"}]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Bullet point 2"}]}]}
        ]}
    ]
}

formatted_description = extract_text_from_description(jira_description)
print(formatted_description)
