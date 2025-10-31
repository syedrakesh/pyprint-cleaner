import os

def comment_unnecessary_prints(root_dir):
    """
    Safely comments print() statements that are not the only line in a block.
    Leaves single-line blocks untouched to avoid breaking business logic.
    """
    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.endswith('.py'):
                continue

            file_path = os.path.join(subdir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            modified = False
            block_stack = []  # track indentation levels for blocks

            for i, line in enumerate(lines):
                stripped = line.strip()
                indent = len(line) - len(line.lstrip())

                # Skip empty lines or comments
                if not stripped or stripped.startswith("#"):
                    new_lines.append(line)
                    continue

                # Track block start
                if stripped.endswith(":"):
                    block_stack.append(indent)
                    new_lines.append(line)
                    continue

                # Track block end
                while block_stack and indent <= block_stack[-1]:
                    block_stack.pop()

                # Detect print
                if stripped.startswith("print("):
                    # Check if this print is the only statement in the current block
                    block_indent = block_stack[-1] if block_stack else -1
                    block_lines = []
                    j = i
                    while j < len(lines):
                        next_line = lines[j].strip()
                        next_indent = len(lines[j]) - len(lines[j].lstrip())
                        if next_indent <= block_indent and j != i:
                            break
                        if next_line and not next_line.startswith("#"):
                            block_lines.append(next_line)
                        j += 1

                    if len(block_lines) == 1:
                        # Only this print in the block → leave it
                        new_lines.append(line)
                        continue

                    # Safe to comment
                    new_lines.append(line.replace("print(", "# [auto] print(", 1))
                    modified = True
                else:
                    new_lines.append(line)

            if modified:
                backup_path = file_path + ".bak"
                os.rename(file_path, backup_path)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print("📝 Commented prints in: {file_path}")


def main():
    project_dir = os.getcwd()
    print("📂 Using current directory: {project_dir}")
    comment_unnecessary_prints(project_dir)
    print("🎉 Done! All safe prints have been commented.")
