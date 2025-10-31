import os
import re

def comment_unnecessary_prints(root_dir):
    """
    Comments out all print() statements in Python files within the given directory.
    Handles inline prints and single-line block prints safely (adds 'pass' if needed).
    """

    block_keywords = ("if", "elif", "else", "for", "while", "try", "except", "finally", "with", "def", "class")

    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.endswith('.py'):
                continue

            file_path = os.path.join(subdir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            modified = False
            inside_multiline = False

            for i, line in enumerate(lines):
                stripped = line.strip()

                # Track multiline strings
                if stripped.startswith(("'''", '"""')):
                    inside_multiline = not inside_multiline
                    new_lines.append(line)
                    continue

                if inside_multiline or stripped.startswith("#"):
                    new_lines.append(line)
                    continue

                # Handle print detection
                if "print(" in stripped:
                    indent = len(line) - len(line.lstrip())

                    # comment the print safely (preserving indentation)
                    commented_line = re.sub(
                        r'^(\s*)print\s*\(.*\)',
                        r'\1# [auto] print(' + line.strip()[6:] if line.strip().startswith("print(") else line,
                        line,
                    )

                    if commented_line == line:  # maybe inline print
                        commented_line = re.sub(r'(\s|:)print\s*\(', r'\1# [auto] print(', line)

                    new_lines.append(commented_line)
                    modified = True

                    # check next line indent to see if this was the only line in a block
                    next_line = lines[i + 1] if i + 1 < len(lines) else ""
                    next_indent = len(next_line) - len(next_line.lstrip())

                    if (
                        i > 0
                        and any(lines[i - 1].lstrip().startswith(k + ":") for k in block_keywords)
                        and (not next_line.strip() or next_indent <= indent)
                    ):
                        new_lines.append(" " * (indent + 4) + "pass\n")

                else:
                    new_lines.append(line)

            if modified:
                backup_path = file_path + ".bak"
                os.rename(file_path, backup_path)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"📝 Commented prints in: {file_path}")


def main():
    project_dir = os.getcwd()
    print(f"📂 Using current directory: {project_dir}")
    comment_unnecessary_prints(project_dir)
    print("\n🎉 Done! All unnecessary prints have been commented.")
