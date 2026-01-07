import requests
import os
import json
import re
import time

# ====== UPDATE WITH YOUR COOKIES ======
COOKIES = {
    "csrftoken": "placeholdertextplaceholdertext",  # replace with actual csrf token
    "LEETCODE_SESSION": "placeholderauthenticationtokenvalue"  # replace with actual session
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
    params = {"offset": offset, "limit": limit}
    response = requests.get(API_URL, params=params, cookies=COOKIES)
    if response.status_code == 200:
        return response.json()
    print("Error fetching submissions:", response.status_code)
    return None

def fetch_problem_details(slug):
    query = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionFrontendId
            title
            difficulty
            content
            topicTags {
              name
            }
          }
        }
        """
    }
    response = requests.post(GRAPHQL_URL, json=query, cookies=COOKIES)
    if response.status_code == 200:
        return response.json().get("data", {}).get("question", None)
    return None

def format_title(title):
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "_".join(word.capitalize() for word in words)

def save_submission(problem_slug, problem_title, submission_id, code, lang, problem_url, problem_details):
    problem_id = problem_details.get("questionFrontendId", "0")
    formatted_title = format_title(problem_title)

    base_name = f"{problem_id}_{formatted_title}"
    problem_folder = os.path.join(SAVE_ROOT, base_name)
    os.makedirs(problem_folder, exist_ok=True)

    extension = LANG_EXTENSIONS.get(lang.lower(), lang.lower())
    code_path = os.path.join(problem_folder, f"{base_name}.{extension}")

    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"Saved: {code_path}")

    readme_path = os.path.join(problem_folder, f"{base_name}.md")
    if not os.path.exists(readme_path):
        tags = ", ".join(tag["name"] for tag in problem_details.get("topicTags", []))
        difficulty = problem_details.get("difficulty", "Unknown")
        content = problem_details.get("content", "")

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {problem_id}. {problem_title}\n\n")
            f.write(f"**Difficulty:** {difficulty}\n\n")
            f.write(f"[View problem on LeetCode]({problem_url})\n\n")
            f.write(f"**Tags:** {tags}\n\n")
            f.write("---\n\n")
            f.write(content)

        print(f"Generated README: {readme_path}")

def main():
    offset = 0
    limit = 20

    while True:
        data = fetch_submissions(offset, limit)
        if not data or "submissions_dump" not in data:
            break

        submissions = data["submissions_dump"]
        if not submissions:
            break

        for sub in submissions:
            if sub["status_display"] == "Accepted":
                problem_title = sub["title"]
                problem_slug = sub["title_slug"]
                code = sub["code"]
                lang = sub["lang"]
                problem_url = f"https://leetcode.com/problems/{problem_slug}/"

                problem_details = fetch_problem_details(problem_slug)
                if not problem_details:
                    continue

                save_submission(
                    problem_slug,
                    problem_title,
                    sub["id"],
                    code,
                    lang,
                    problem_url,
                    problem_details
                )

                time.sleep(0.5)

        offset += limit

    print("✅ All submissions downloaded with numbered folder structure!")

if __name__ == "__main__":
    main()

