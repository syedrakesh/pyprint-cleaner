import os
import re

def uncomment_prints(root_dir):
    """
    Uncomments lines that were commented by print_cleaner (i.e., lines starting with '# [auto] print').
    """
    comment_pattern = re.compile(r'^(\s*)#\s*\[auto\]\s*print\s*\(.*\)')

    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.endswith('.py'):
                continue

            file_path = os.path.join(subdir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            new_lines = []

            for line in lines:
                match = comment_pattern.match(line)
                if match:
                    indent = match.group(1)
                    uncommented = re.sub(r'^(\s*)#\s*\[auto\]\s*', r'\1', line)
                    new_lines.append(uncommented)
                    modified = True
                else:
                    new_lines.append(line)

            if modified:
                backup_path = file_path + '.uncomment.bak'
                os.rename(file_path, backup_path)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"🔄 Uncommented prints in: {file_path}")
            else:
                print(f"✅ No commented prints found in: {file_path}")


def main():
    project_dir = os.getcwd()
    print(f"📂 Using current directory: {project_dir}")
    uncomment_prints(project_dir)
    print("\n🎉 Done! All commented prints have been uncommented.")
