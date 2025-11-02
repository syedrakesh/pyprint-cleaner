import os
import shutil


def get_backup_dir(project_dir):
    """Return backup folder path inside project."""
    return os.path.join(project_dir, ".print_backups")


def restore_backups(root_dir):
    """Restore all .bak files from the .print_backups folder."""
    backup_dir = get_backup_dir(root_dir)

    if not os.path.exists(backup_dir):
        print("⚠️ No backup folder found — nothing to restore.")
        return

    restored = 0
    for filename in os.listdir(backup_dir):
        if not filename.endswith(".bak"):
            continue

        backup_path = os.path.join(backup_dir, filename)
        original_name = filename[:-4]  # remove .bak

        # Locate and restore
        for subdir, _, files in os.walk(root_dir):
            if backup_dir in subdir:
                continue
            if original_name in files:
                dest_path = os.path.join(subdir, original_name)
                shutil.copy(backup_path, dest_path)
                print(f"♻️ Restored: {dest_path}")
                restored += 1
                break

    if restored == 0:
        print("⚠️ No .bak files restored.")
    else:
        print(f"✅ Restored {restored} file(s) from backup.")


def main():
    project_dir = os.getcwd()
    restore_backups(project_dir)


if __name__ == "__main__":
    main()
