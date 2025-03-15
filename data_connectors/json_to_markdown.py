import json

def convert_slack_to_md(input_file, output_file):
    """Converts Slack messages JSON to Markdown."""
    with open(input_file, "r", encoding="utf-8") as file:
        messages = json.load(file)

    markdown_content = "# Slack Messages\n\n"
    for message in messages:
        markdown_content += f"**Channel:** #{message.get('channel', 'unknown')}\n\n"
        markdown_content += f"> {message.get('text', 'No message')}\n\n"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(markdown_content)

def convert_gdrive_to_md(input_file, output_file):
    """Converts Google Drive results JSON (key-value format) to Markdown."""
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    markdown_content = "# Google Drive Emails Extracted\n\n"
    for filename, content in data.items():
        markdown_content += f"## {filename}\n"
        markdown_content += f"```\n{content}\n```\n\n"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(markdown_content)

def convert_gmail_to_md(input_file, output_file):
    """Converts Gmail messages JSON (dictionary format) to Markdown."""
    with open(input_file, "r", encoding="utf-8") as file:
        emails = json.load(file)

    markdown_content = "# Gmail Messages\n\n"
    for email in emails:
        markdown_content += f"## Subject: {email.get('subject', 'No Subject')}\n"
        markdown_content += f"- **From:** {email.get('from', 'Unknown')}\n"
        markdown_content += f"- **To:** {email.get('to', 'Unknown')}\n"
        markdown_content += f"- **Date:** {email.get('date', 'Unknown')}\n"
        markdown_content += f"- **Thread ID:** {email.get('threadId', 'N/A')}\n\n"
        markdown_content += f"> {email.get('snippet', 'No snippet available')}\n\n"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(markdown_content)

# Convert all files
convert_slack_to_md("slack_messages.json", "slack_messages.md")
convert_gdrive_to_md("gdrive_results.json", "gdrive_results.md")
convert_gmail_to_md("gmail_results.json", "gmail_results.md")

print("Markdown files created successfully.")
