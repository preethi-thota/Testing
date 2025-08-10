import subprocess
import os

# ===== CONFIGURATION =====
REMOTE_URL = "https://github.com/preethi-thota/Testing"  # Change this
BRANCH_NAME = "main"  # Change if different
COMMIT_MESSAGE = "Initial commit with all files"

# ===== FUNCTION TO RUN GIT COMMANDS =====
def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, shell=True)
    if result.returncode != 0:
        print(f"❌ Error running: {cmd}")
        print(result.stderr)
        exit(1)
    return result.stdout.strip()

if __name__ == "__main__":
    # Detect the folder where the script is run
    LOCAL_FOLDER = os.getcwd()
    print(f"📂 Working in: {LOCAL_FOLDER}")

    # Step 1: Initialize Git
    run_cmd("git init", cwd=LOCAL_FOLDER)

    # Step 2: Add remote if not exists
    remotes = run_cmd("git remote -v", cwd=LOCAL_FOLDER)
    if REMOTE_URL not in remotes:
        run_cmd(f"git remote add origin {REMOTE_URL}", cwd=LOCAL_FOLDER)

    # Step 3: Add all files in this folder
    run_cmd("git add .", cwd=LOCAL_FOLDER)

    # Step 4: Commit
    run_cmd(f'git commit -m "{COMMIT_MESSAGE}"', cwd=LOCAL_FOLDER)

    # Step 5: Rename branch
    run_cmd(f"git branch -M {BRANCH_NAME}", cwd=LOCAL_FOLDER)

    # Step 6: Push to remote
    try:
        run_cmd(f"git push -u origin {BRANCH_NAME}", cwd=LOCAL_FOLDER)
        print("✅ Push completed successfully!")
    except SystemExit:
        print("⚠️ Push failed. You may need to run:")
        print(f"git pull origin {BRANCH_NAME} --allow-unrelated-histories")
