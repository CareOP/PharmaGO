import json
from datetime import datetime

# Load incoming event (from GitHub Actions)
with open("event.json", "r") as f:
    event = json.load(f)

repo = event["repo"].split("/")[-1]
commit = event["commit"][:7]
author = event["author"]
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# Load existing data
with open("progress/activity-log.json", "r") as f:
    activity = json.load(f)

with open("progress/repo-status.json", "r") as f:
    status = json.load(f)

# Update activity log
activity["events"].insert(0, {
    "repo": repo,
    "commit": commit,
    "author": author,
    "timestamp": timestamp
})

# Keep only last 20 events
activity["events"] = activity["events"][:20]

# Update repo status
status[repo] = {
    "last_commit": commit,
    "last_updated": timestamp
}

# Save updated files
with open("progress/activity-log.json", "w") as f:
    json.dump(activity, f, indent=2)

with open("progress/repo-status.json", "w") as f:
    json.dump(status, f, indent=2)

# Generate README dashboard
readme_content = """# PharmaGO Central Dashboard

## 🚀 Repositories Status

| Repo | Last Commit | Last Updated |
|------|------------|-------------|
"""

for repo_name, data in status.items():
    readme_content += f"| {repo_name} | {data['last_commit']} | {data['last_updated']} |\n"

readme_content += "\n---\n\n## 📊 Activity Feed\n\n"

for event in activity["events"][:10]:
    readme_content += f"- {event['repo']} updated by {event['author']} ({event['commit']})\n"

# Write README
with open("README.md", "w") as f:
    f.write(readme_content)

print("Dashboard updated successfully.")