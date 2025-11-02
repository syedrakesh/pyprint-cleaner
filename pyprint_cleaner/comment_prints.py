import os
import shutil


def get_backup_dir(project_dir):
    """Return (and create) the backup directory inside the project."""
    backup_dir = os.path.join(project_dir, ".print_backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def is_block_start(line: str) -> bool:
    """Detect Python block starters like if, for, try, etc."""
    stripped = line.strip()
    return stripped.startswith((
        "if ", "elif ", "else:", "try:", "except", "finally:",
        "for ", "while ", "with ", "def ", "class "
    )) and stripped.endswith(":")


def get_block_lines(lines, start_index, block_indent):
    """
    Collect all lines belonging to a given block starting from start_index.
    Returns a list of stripped code lines (non-comments, non-empty).
    """
    collected = []
    for j in range(start_index, len(lines)):
        next_line = lines[j]
        next_stripped = next_line.strip()
        next_indent = len(lines[j]) - len(lines[j].lstrip())

        if next_indent <= block_indent and j != start_index:
            break
        if next_stripped and not next_stripped.startswith("#"):
            collected.append(next_stripped)
    return collected


def comment_unnecessary_prints(root_dir):
    """
    Comments out print() and print(f...) safely.
    Skips blocks where print() is the only statement.
    Creates .bak backups in .print_backups folder at project root.
    """
    backup_dir = get_backup_dir(root_dir)
    print(f"📂 Scanning project: {root_dir}")

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

                if not stripped or stripped.startswith("#"):
                    new_lines.append(line)
                    continue

                # Track block structure
                if is_block_start(line):
                    block_stack.append(indent)
                    new_lines.append(line)
                    continue

                while block_stack and indent <= block_stack[-1]:
                    block_stack.pop()

                # Detect print
                if stripped.startswith("print(") or stripped.startswith("print(f"):
                    block_indent = block_stack[-1] if block_stack else -1
                    block_lines = get_block_lines(lines, i, block_indent)
                    code_line_count = len(block_lines)

                    # Skip single-line print-only blocks
                    if code_line_count == 1:
                        new_lines.append(line)
                        continue

                    commented = line.replace("print(", "# [auto] print(", 1)
                    new_lines.append(commented)
                    modified = True
                else:
                    new_lines.append(line)

            # Save modified + backup original
            if modified:
                backup_path = os.path.join(backup_dir, os.path.basename(file_path) + ".bak")
                shutil.copy(file_path, backup_path)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"📝 Commented prints in: {file_path}")

    print("✅ Done! All safe print() statements commented.")


def main():
    project_dir = os.getcwd()
    comment_unnecessary_prints(project_dir)


if __name__ == "__main__":
    main()
