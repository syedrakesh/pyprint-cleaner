import os

def uncomment_prints(root_dir):
    """
    Reverts previously commented print statements safely.
    Only restores lines that start with '# [auto] print('.
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

            for line in lines:
                if "# [auto] print(" in line:
                    # Restore the original print
                    new_lines.append(line.replace("# [auto] print(", "print(", 1))
                    modified = True
                else:
                    new_lines.append(line)

            if modified:
                backup_path = file_path + ".uncomment.bak"
                os.rename(file_path, backup_path)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print("🔄 Uncommented prints in: {file_path}")


def main():
    project_dir = os.getcwd()
    print("📂 Using current directory: {project_dir}")
    uncomment_prints(project_dir)
    print("🎉 Done! All prints have been uncommented.")
