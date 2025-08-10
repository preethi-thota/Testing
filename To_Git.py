import subprocess
import os

# ===== CONFIGURATION =====
LOCAL_FOLDER = r"C:\\Users\\91970\\Desktop\\Git Migration"
REMOTE_URL = "https://github.com/preethi-thota/Testing"  # Change this
BRANCH_NAME = "main"  # Change if your repo uses a different branch
COMMIT_MESSAGE = "Initial commit with local folder contents"

# ===== FUNCTION TO RUN GIT COMMANDS =====
def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, shell=True)
    if result.returncode != 0:
        print(f"Error running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        print(result.stderr)
        exit(1)
    return result.stdout.strip()

# ===== AUTOMATION =====
if __name__ == "__main__":
    # Step 1: Navigate to folder
    if not os.path.isdir(LOCAL_FOLDER):
        print("❌ Folder does not exist!")
        exit(1)

    # Step 2: Initialize Git
    run_cmd("git init", cwd=LOCAL_FOLDER)

    # Step 3: Add remote (if not already added)
    remotes = run_cmd("git remote -v", cwd=LOCAL_FOLDER)
    if REMOTE_URL not in remotes:
        run_cmd(f"git remote add origin {REMOTE_URL}", cwd=LOCAL_FOLDER)

    # Step 4: Add all files
    run_cmd("git add .", cwd=LOCAL_FOLDER)

    # Step 5: Commit
    run_cmd(f'git commit -m "{COMMIT_MESSAGE}"', cwd=LOCAL_FOLDER)

    # Step 6: Rename branch
    run_cmd(f"git branch -M {BRANCH_NAME}", cwd=LOCAL_FOLDER)

    # Step 7: Push to remote
    try:
        run_cmd(f"git push -u origin {BRANCH_NAME}", cwd=LOCAL_FOLDER)
        print("✅ Push completed successfully!")
    except SystemExit:
        print("⚠️ Push failed. You may need to run:")
        print(f"git pull origin {BRANCH_NAME} --allow-unrelated-histories")
