import os
import shutil


def get_backup_dir(project_dir):
    return os.path.join(project_dir, ".print_backups")


def uncomment_prints(root_dir):
    """
    Restores .py files from .print_backups directory in the project root.
    """
    backup_dir = get_backup_dir(root_dir)
    if not os.path.exists(backup_dir):
        print("⚠️ No .print_backups folder found — nothing to restore.")
        return

    for backup_file in os.listdir(backup_dir):
        if not backup_file.endswith(".bak"):
            continue

        original_name = backup_file[:-4]  # remove .bak
        backup_path = os.path.join(backup_dir, backup_file)

        # Find matching file in project
        target_path = None
        for subdir, _, files in os.walk(root_dir):
            if backup_dir in subdir:
                continue
            for f in files:
                if f == original_name:
                    target_path = os.path.join(subdir, f)
                    break

        if target_path:
            shutil.copy(backup_path, target_path)
            print(f"♻️ Restored: {target_path}")
        else:
            print(f"⚠️ No matching file found for {backup_file}")


def main():
    project_dir = os.getcwd()
    print(f"📂 Restoring from: {project_dir}/.print_backups")
    uncomment_prints(project_dir)
    print("✅ Restoration complete.")
