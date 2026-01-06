

---

# 🚀 LeetCode Accepted Submissions Fetcher (Automation Script)

## 📌 Overview

This project is a **custom-built Python automation script** designed to fetch **accepted submissions** from a LeetCode account and store them locally in a clean, organized folder structure.

The script authenticates using session cookies, retrieves submission data through LeetCode’s APIs, and saves source code files language-wise under problem-specific directories.
It is intended for **personal archival, learning review, and offline access** to previously solved problems.

This is an **original implementation**, created to solve a personal workflow problem and not derived from any existing repository.

---

## 🧠 What This Script Does

* Connects to LeetCode using authenticated session cookies
* Fetches **only Accepted submissions**
* Automatically creates:

  * One folder per problem
  * One file per accepted submission
* Supports **multiple programming languages**
* Names files using **submission IDs** for uniqueness
* Optionally generates metadata-based README files per problem (configurable)

---

## 📂 Generated Folder Structure

```
SAVE_ROOT/
 ├── Problem_Name_One/
 │    ├── 1875945177.cpp
 │    ├── 1874989247.rs
 │    └── README.md
 ├── Problem_Name_Two/
 │    ├── 1863768767.java
 │    └── README.md
```

Each solution file corresponds to a **real accepted submission**.

---

## ⚙️ Requirements

* Python 3.8+
* `requests` library
* Active LeetCode account
* Valid authentication cookies

Install dependencies:

```bash
pip install requests
```

---

## 🔐 Authentication Setup

Update the following fields in the script before running:

```python
COOKIES = {
    "csrftoken": "your_csrf_token_here",
    "LEETCODE_SESSION": "your_leetcode_session_here"
}

USERNAME = "your_leetcode_username"
SAVE_ROOT = "your_local_folder_name"
```

⚠️ These cookies are **private** and should **never be committed** to a public repository.

---

## ▶️ How to Run

Place the script in your desired directory and run:

```bash
python filename.py
```

The script will:

1. Fetch submissions in batches
2. Filter accepted solutions
3. Save code locally
4. Continue until all submissions are processed

---

## 🌍 Supported Languages

The script automatically maps LeetCode languages to file extensions, including:

* C / C++
* Java
* Python / Python3
* JavaScript / TypeScript
* Rust
* Go
* Kotlin
* Swift
* Ruby
* PHP
* Scala
* SQL
* R

---

## 🛡️ Safety & Usage Notes

* This script is meant for **personal use only**
* Avoid excessive request rates (a delay is included)
* LeetCode may change APIs at any time
* Do not redistribute fetched problem statements or editorial content

---

## 📜 Disclaimer

* All fetched source code belongs to the authenticated user
* No LeetCode editorial content is redistributed
* Problem descriptions are **not copied** into this repository
* This project is **not affiliated with or endorsed by LeetCode**

---

## ✨ Why This Exists

The purpose of this project is to:

* Maintain a personal offline archive of solved problems
* Review past solutions without logging into LeetCode
* Track multi-language implementations
* Improve learning consistency and accountability

---

## 🧑‍💻 Author

Developed as an **independent automation project** for productivity and learning enhancement.

---



