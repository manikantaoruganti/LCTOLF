import requests
import os
import json
import re
import time

# ====== UPDATE WITH YOUR COOKIES ======
COOKIES = {
    "csrftoken": "placeholdertextplaceholdertext",#replace wtih actual csrf token 
    "LEETCODE_SESSION": "placeholderauthenticationtokenvalue"#replace with your actual session
}
USERNAME = "placeholderusername"  # Replace with your LeetCode username
SAVE_ROOT = "Specify the name of a folder on your device.This folder will be treated as the root directory, and all submissions will be saved inside it.Ensure that the script is running from the same location where the SAVE_ROOT folder exists."

API_URL = "https://leetcode.com/api/submissions/"
GRAPHQL_URL = "https://leetcode.com/graphql"

# Ensure root folder exists
os.makedirs(SAVE_ROOT, exist_ok=True)

# Map LeetCode language names to file extensions
LANG_EXTENSIONS = {
    "cpp": "cpp",
    "c": "c",
    "java": "java",
    "python": "py",
    "python3": "py",
    "csharp": "cs",
    "javascript": "js",
    "typescript": "ts",
    "kotlin": "kt",
    "golang": "go",
    "swift": "swift",
    "ruby": "rb",
    "rust": "rs",
    "php": "php",
    "scala": "scala",
    "r": "r",
    "mysql": "sql",
}

def fetch_submissions(offset=0, limit=20):
    """Fetch a page of submissions."""
    params = {"offset": offset, "limit": limit}
    response = requests.get(API_URL, params=params, cookies=COOKIES)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching submissions:", response.status_code, response.text)
        return None

def fetch_problem_details(slug):
    """Fetch problem details for README.md."""
    query = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            difficulty
            content
            topicTags {
              name
            }
            stats
            likes
            dislikes
          }
        }
        """
    }
    response = requests.post(GRAPHQL_URL, json=query, cookies=COOKIES)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("question", None)
    else:
        print(f"Error fetching details for {slug}: {response.status_code}")
        return None

def sanitize_name(name):
    """Make folder-safe names."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def save_submission(problem_slug, problem_title, submission_id, code, lang, problem_url, problem_details):
    """Save a single submission with folder structure."""
    safe_problem_name = sanitize_name(problem_title)
    problem_folder = os.path.join(SAVE_ROOT, safe_problem_name)
    os.makedirs(problem_folder, exist_ok=True)

    # Determine correct file extension
    extension = LANG_EXTENSIONS.get(lang.lower(), lang)

    # Save code
    filename = f"{submission_id}.{extension}"
    filepath = os.path.join(problem_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Saved: {filepath}")

    # Generate README.md for the problem if not exists
    readme_path = os.path.join(problem_folder, "README.md")
    if not os.path.exists(readme_path) and problem_details:
        tags = ", ".join(tag["name"] for tag in problem_details.get("topicTags", []))
        content = problem_details.get("content", "")
        difficulty = problem_details.get("difficulty", "Unknown")

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {problem_title}\n\n")
            f.write(f"**Difficulty:** {difficulty}\n\n")
            f.write(f"[View problem on LeetCode]({problem_url})\n\n")
            f.write(f"**Tags:** {tags}\n\n")
            f.write("---\n\n")
            f.write(content)

        print(f"Generated README.md for {problem_title}")

def main():
    offset = 0
    limit = 20

    while True:
        data = fetch_submissions(offset, limit)
        if not data or "submissions_dump" not in data:
            break

        submissions = data["submissions_dump"]
        if not submissions:
            break  # No more submissions

        for sub in submissions:
            if sub["status_display"] == "Accepted":
                problem_title = sub["title"]
                problem_slug = sub["title_slug"]
                submission_id = sub["id"]
                code = sub["code"]
                lang = sub["lang"]
                problem_url = f"https://leetcode.com/problems/{problem_slug}/"

                # Fetch problem details for README.md
                problem_details = fetch_problem_details(problem_slug)
                save_submission(problem_slug, problem_title, submission_id, code, lang, problem_url, problem_details)

                time.sleep(0.5)  # To avoid being blocked by LeetCode

        offset += limit

    print("✅ All submissions downloaded with folder structure!")

if __name__ == "__main__":
    main()
