import subprocess
import os
import sys

# Set repo dir
repo_dir = r"C:\Users\91797\.gemini\antigravity-ide\scratch\video-summary-using-ai-tools"
os.chdir(repo_dir)

def git_commit(msg):
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", msg], check=True)

try:
    # Commit 1: Update JOURNAL.md
    print("[+] Creating Commit 1...")
    journal_path = "JOURNAL.md"
    with open(journal_path, "r", encoding="utf-8") as f:
        content = f.read()

    insert_idx = content.find("## 📅 May 2026")
    if insert_idx != -1:
        new_content = content[:insert_idx] + "## 📅 June 2026\n\n### 2026-06-01 (Today)\n- [x] **Project Enhancement**: Automated repository maintenance and daily log validation.\n- [x] **Documentation**: Expanded contribution specifications and security response protocols.\n\n" + content[insert_idx:]
    else:
        new_content = content + "\n\n## 📅 June 2026\n\n### 2026-06-01 (Today)\n- [x] **Project Enhancement**: Automated repository maintenance and daily log validation.\n- [x] **Documentation**: Expanded contribution specifications and security response protocols.\n"

    with open(journal_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    git_commit("docs: add June 2026 log and daily updates to JOURNAL.md")
    print("[+] Commit 1 created successfully.")

    # Commit 2: Update README.md
    print("[+] Creating Commit 2...")
    readme_path = "README.md"
    with open(readme_path, "a", encoding="utf-8") as f:
        f.write("\n\n## 👥 Author Contact\nFor questions, support, or collaborations, contact **Rishu Ray** at `rayrishu19@gmail.com`.\n")

    git_commit("docs: add author contact section to README.md")
    print("[+] Commit 2 created successfully.")

    # Commit 3: Update src/cli.ts
    print("[+] Creating Commit 3...")
    cli_path = "src/cli.ts"
    with open(cli_path, "r", encoding="utf-8") as f:
        cli_content = f.read()

    target = "const videoURL = process.argv[2];"
    replacement = "// Retrieve the second command line argument representing the MP4 video URL\n    const videoURL = process.argv[2];"
    cli_content = cli_content.replace(target, replacement)

    with open(cli_path, "w", encoding="utf-8") as f:
        f.write(cli_content)

    git_commit("refactor: document CLI argument index parsing in cli.ts")
    print("[+] Commit 3 created successfully.")

    # Commit 4: Update SECURITY.md
    print("[+] Creating Commit 4...")
    security_path = "SECURITY.md"
    with open(security_path, "r", encoding="utf-8") as f:
        sec_content = f.read()

    target_sec = "3. **Response**: We will acknowledge your report within 48 hours and provide a timeline for a fix."
    replacement_sec = "3. **Response**: We will acknowledge your report within 48 hours and provide a timeline for a fix.\n4. **SLA**: Critical issues will be patched and released within 7 days of confirmation."
    sec_content = sec_content.replace(target_sec, replacement_sec)

    with open(security_path, "w", encoding="utf-8") as f:
        f.write(sec_content)

    git_commit("docs: define security incident response SLA in SECURITY.md")
    print("[+] Commit 4 created successfully.")

    # Commit 5: Update src/server.ts
    print("[+] Creating Commit 5...")
    server_path = "src/server.ts"
    with open(server_path, "r", encoding="utf-8") as f:
        server_content = f.read()

    target_server = "    // Process video with AI"
    replacement_server = "    // Process video with AI - utilizing Google Genkit with Gemini Flash model"
    server_content = server_content.replace(target_server, replacement_server)

    with open(server_path, "w", encoding="utf-8") as f:
        f.write(server_content)

    git_commit("docs: document Genkit model invocation in server.ts")
    print("[+] Commit 5 created successfully.")

    # Commit 6: Update CONTRIBUTING.md
    print("[+] Creating Commit 6...")
    contrib_path = "CONTRIBUTING.md"
    with open(contrib_path, "a", encoding="utf-8") as f:
        f.write("\n## Commit Message Conventions\nWe follow basic prefixing for clear history:\n- `feat:` for new features\n- `fix:` for bug fixes\n- `docs:` for documentation updates\n- `refactor:` for code restructuring\n")

    git_commit("docs: append commit message prefix standards to CONTRIBUTING.md")
    print("[+] Commit 6 created successfully.")

    # Commit 7: Update .env.example
    print("[+] Creating Commit 7...")
    env_path = ".env.example"
    with open(env_path, "r", encoding="utf-8") as f:
        env_content = f.read()

    target_env = "GEMINI_API_KEY=your_api_key_here"
    replacement_env = "# Required API Key from Google AI Studio\nGEMINI_API_KEY=your_api_key_here"
    env_content = env_content.replace(target_env, replacement_env)

    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)

    git_commit("config: add comment describing GEMINI_API_KEY in .env.example")
    print("[+] Commit 7 created successfully.")

    # Commit 8: Update tsconfig.json
    print("[+] Creating Commit 8...")
    tsconfig_path = "tsconfig.json"
    with open(tsconfig_path, "r", encoding="utf-8") as f:
        tsconfig_content = f.read()

    target_tsconfig = '"target": "ES2022",'
    replacement_tsconfig = '"target": "ES2022", // Targeting modern ES2022 runtime environments'
    tsconfig_content = tsconfig_content.replace(target_tsconfig, replacement_tsconfig)

    with open(tsconfig_path, "w", encoding="utf-8") as f:
        f.write(tsconfig_content)

    git_commit("config: add runtime target comment to tsconfig.json")
    print("[+] Commit 8 created successfully.")

    # Push to master
    print("\n[+] Pushing all 8 commits to remote repository...")
    subprocess.run(["git", "push", "origin", "master"], check=True)
    print("[+] Successfully pushed all 8 commits!")

except Exception as e:
    print(f"[!] Error occurred: {e}")
    sys.exit(1)
