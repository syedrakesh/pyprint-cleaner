import os
import shutil

def get_backup_dir(project_dir):
    """Return (and create) the backup directory inside the project."""
    backup_dir = os.path.join(project_dir, ".print_backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def is_block_start(line: str) -> bool:
    """Detects Python block starters."""
    stripped = line.strip()
    return stripped.startswith((
        "if ", "else:", "elif ", "try:", "except", "finally:",
        "for ", "while ", "with ", "def ", "class "
    )) and stripped.endswith(":")


def comment_unnecessary_prints(root_dir):
    """
    Comments out print() calls safely while keeping single-print-only blocks untouched.
    Backs up each modified file into a .print_backups folder at project root.
    """
    backup_dir = get_backup_dir(root_dir)

    for subdir, _, files in os.walk(root_dir):
        if backup_dir in subdir:
            continue  # skip backup folder itself

        for filename in files:
            if not filename.endswith(".py"):
                continue

            file_path = os.path.join(subdir, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            modified = False
            block_stack = []

            for i, line in enumerate(lines):
                stripped = line.strip()
                indent = len(line) - len(line.lstrip())

                # Skip comments and blank lines
                if not stripped or stripped.startswith("#"):
                    new_lines.append(line)
                    continue

                # Track block start
                if is_block_start(line):
                    block_stack.append(indent)
                    new_lines.append(line)
                    continue

                # Detect block end
                while block_stack and indent <= block_stack[-1]:
                    block_stack.pop()

                # Detect print or f-string print
                if stripped.startswith("print(") or stripped.startswith("print(f"):
                    block_indent = block_stack[-1] if block_stack else -1
                    block_lines = []

                    # Collect all lines in same block
                    j = i
                    while j < len(lines):
                        next_line = lines[j].strip()
                        next_indent = len(lines[j]) - len(lines[j].lstrip())
                        if next_indent <= block_indent and j != i:
                            break
                        if next_line and not next_line.startswith("#"):
                            block_lines.append(next_line)
                        j += 1

                    # Skip if print is the only statement in the block
                    if len(block_lines) == 1:
                        new_lines.append(line)
                        continue

                    # Safe to comment
                    commented_line = line.replace("print(", "# [auto] print(", 1)
                    new_lines.append(commented_line)
                    modified = True
                else:
                    new_lines.append(line)

            # Save modified file + backup
            if modified:
                backup_path = os.path.join(backup_dir, os.path.basename(file_path) + ".bak")
                shutil.copy(file_path, backup_path)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"📝 Commented prints in: {file_path}")
            else:
                new_lines = None


def main():
    project_dir = os.getcwd()
    print(f"📂 Scanning project: {project_dir}")
    comment_unnecessary_prints(project_dir)
    print("✅ Done! All safe print() statements commented.")
