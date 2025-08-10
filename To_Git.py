import subprocess
import os

# ===== CONFIGURATION =====
REMOTE_URL = "https://github.com/preethi-thota/Testing"  # Change this
BRANCH_NAME = "main"  # Change if different
COMMIT_MESSAGE = "Commit with all non-empty folders and files"

def run_cmd(cmd, cwd=None, exit_on_error=True):
    """Run a shell command and return its output."""
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, shell=True)
    if result.returncode != 0:
        print(f"❌ Error running: {cmd}")
        print(result.stderr)
        if exit_on_error:
            exit(1)
    return result.stdout.strip()

def remove_empty_folders(folder_path):
    """Remove empty folders so Git doesn't track them."""
    for root, dirs, files in os.walk(folder_path, topdown=False):
        if not files and not dirs:  # Empty folder
            print(f"🗑️ Removing empty folder: {root}")
            os.rmdir(root)

if __name__ == "__main__":
    LOCAL_FOLDER = os.getcwd()
    print(f"📂 Working in: {LOCAL_FOLDER}")

    # Step 1: Remove empty folders before commit
    remove_empty_folders(LOCAL_FOLDER)

    # Step 2: Initialize git if needed
    if not os.path.exists(os.path.join(LOCAL_FOLDER, ".git")):
        run_cmd("git init", cwd=LOCAL_FOLDER)

    # Step 3: Add remote if not already linked
    remotes = run_cmd("git remote -v", cwd=LOCAL_FOLDER, exit_on_error=False)
    if REMOTE_URL not in remotes:
        run_cmd(f"git remote add origin {REMOTE_URL}", cwd=LOCAL_FOLDER)

    # Step 4: Ensure correct branch
    run_cmd(f"git branch -M {BRANCH_NAME}", cwd=LOCAL_FOLDER)

    # Step 5: Try pulling from remote (merge if needed)
    print("🔄 Checking remote for existing content...")
    run_cmd(f"git fetch origin {BRANCH_NAME}", cwd=LOCAL_FOLDER, exit_on_error=False)
    run_cmd(f"git pull origin {BRANCH_NAME} --allow-unrelated-histories", cwd=LOCAL_FOLDER, exit_on_error=False)

    # Step 6: Add all files except empty folders
    run_cmd("git add .", cwd=LOCAL_FOLDER)

    # Step 7: Commit changes
    run_cmd(f'git commit -m "{COMMIT_MESSAGE}"', cwd=LOCAL_FOLDER, exit_on_error=False)

    # Step 8: Push to remote
    run_cmd(f"git push -u origin {BRANCH_NAME}", cwd=LOCAL_FOLDER)

    print("✅ Push completed successfully! Empty folders excluded.")
