import os
import re

def comment_unnecessary_prints(root_dir):
    """
    Comments out all print() statements in Python files within the given directory.
    Creates a .bak backup for each modified file.
    """
    print_pattern = re.compile(r'^(\s*)print\s*\(.*\)')

    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.endswith('.py'):
                continue

            file_path = os.path.join(subdir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            new_lines = []
            inside_multiline = False

            for line in lines:
                stripped = line.strip()

                # Toggle multiline string context
                if stripped.startswith(("'''", '"""')):
                    inside_multiline = not inside_multiline
                    new_lines.append(line)
                    continue

                if inside_multiline or stripped.startswith("#"):
                    new_lines.append(line)
                    continue

                match = print_pattern.match(line)
                if match:
                    indent = match.group(1)
                    commented = f"{indent}# [auto] {line[len(indent):]}"
                    new_lines.append(commented)
                    modified = True
                else:
                    new_lines.append(line)

            if modified:
                backup_path = file_path + '.bak'
                os.rename(file_path, backup_path)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"📝 Commented prints in: {file_path}")
            else:
                print(f"✅ No prints found in: {file_path}")


def main():
    project_dir = os.getcwd()
    print(f"📂 Using current directory: {project_dir}")
    comment_unnecessary_prints(project_dir)
    print("\n🎉 Done! All unnecessary prints have been commented.")
