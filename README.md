# 🧹 print-cleaner

**print-cleaner** is a simple yet powerful developer utility that automatically **comments out** or **uncomments** all `print()` statements in your Python project.

This helps you keep your production code clean while easily restoring debug logs when needed.

---

## 🚀 Features

✅ Recursively scan your entire project for `print()` statements  
✅ Automatically comment them out safely with backups  
✅ Revert them anytime with one command  
✅ Never touches your docstrings or existing comments  
✅ CLI support (`comment-prints` and `uncomment-prints`)  
✅ Cross-platform and zero dependencies

---

## 🧰 Installation

```bash
pip install print-cleaner
```

---

## 🧩 Usage

### Comment all `print()` statements

```bash
comment-prints
```
You’ll be prompted for your project directory.  
Each modified file gets a `.bak` backup for safety.

---

### Uncomment previously commented prints

```bash
uncomment-prints
```
Restores all lines previously commented by `print-cleaner` (lines starting with `# [auto] print(...)`).

---

## 💡 Example

Before:
```python
print("Debug start")
for i in range(5):
    print(i)
# print("already commented")
```

After running `comment-prints`:
```python
# [auto] print("Debug start")
for i in range(5):
    # [auto] print(i)
# print("already commented")
```

After running `uncomment-prints`:
```python
print("Debug start")
for i in range(5):
    print(i)
# print("already commented")
```

---

## ⚙️ Command-Line Shortcuts

| Command | Description |
|----------|--------------|
| `comment-prints` | Comment all print statements |
| `uncomment-prints` | Restore all commented prints |

---

## 🧑‍💻 Author

**Syed Rakesh Uddin**  
Python Developer & Automation Enthusiast

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🌐 Links

- **Homepage:** [GitHub Repository](https://github.com/syedrakesh/print-cleaner)
- **PyPI:** https://pypi.org/project/print-cleaner

---

✨ Keep your codebase clean, your console quieter, and your debugging reversible!
