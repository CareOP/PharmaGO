import json
import os
from datetime import datetime

# 1. Load incoming event
try:
    with open("event.json", "r") as f:
        event = json.load(f)
except FileNotFoundError:
    print("Error: event.json not found")
    exit(1)

repo = event.get("repo", "Unknown").split("/")[-1]
commit = event.get("commit", "-------")[:7]
author = event.get("author", "Automated")
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

# 2. Ensure progress directory exists
os.makedirs("progress", exist_ok=True)

# 3. Load or Create existing data
def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default

activity = load_json("progress/activity-log.json", {"events": []})
status = load_json("progress/repo-status.json", {})

# 4. Update activity log
activity["events"].insert(0, {
    "repo": repo,
    "commit": commit,
    "author": author,
    "timestamp": timestamp
})
activity["events"] = activity["events"][:20] # Limit history

# 5. Update repo status
status[repo] = {
    "last_commit": commit,
    "last_updated": timestamp
}

# 6. Save updated files
with open("progress/activity-log.json", "w") as f:
    json.dump(activity, f, indent=2)

with open("progress/repo-status.json", "w") as f:
    json.dump(status, f, indent=2)

# 7. Generate README Content
readme_content = f"""# PharmaGO Central Dashboard

## 🚀 Repositories Status

| Repo | Last Commit | Last Updated |
|------|------------|-------------|
"""

for repo_name, data in status.items():
    readme_content += f"| {repo_name} | `{data['last_commit']}` | {data['last_updated']} |\n"

readme_content += "\n---\n\n## 📊 Activity Feed\n\n"

for ev in activity["events"][:10]:
    readme_content += f"- **{ev['repo']}** updated by {ev['author']} (`{ev['commit']}`) at {ev['timestamp']}\n"

# 8. Write the final README
with open("README.md", "w") as f:
    f.write(readme_content)

print(f"Dashboard updated successfully for {repo}.")
