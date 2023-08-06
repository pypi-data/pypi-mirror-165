import os
import shutil
from pathlib import Path

DOCS_PATH = "temp/"
NOT_ALLOWED_FILES = ["temp/config.md", "temp/utils/managed_env.md", "temp/utils/index.md"]
CURRENT_DIR = os.getcwd()
OUTPUT_DIR = "docs/"


def is_files_not_allowed(file):
    return file in NOT_ALLOWED_FILES


def get_all_files():
    files = []
    for r, d, f in os.walk(DOCS_PATH):
        for file in f:
            if file.endswith(".md"):
                files.append((os.path.join(r, file)))
    return files


def handle_line(line: str):
    new_line = line
    if new_line.startswith("    "):
        new_line = new_line.split("    ")[1]
    if new_line.startswith("#"):
        new_line = "#" + new_line
    if new_line.startswith("======================="):
        new_line = new_line.replace("=", "-")
    if new_line.endswith("`\n"):
        new_line = new_line + " \n"
    if new_line.startswith(": ###"):
        new_line = new_line.split(": ###")[1]
    if new_line.startswith(":"):
        new_line = "\n"
    return new_line


def copy_static_files():
    os.rename(f"{CURRENT_DIR}/{DOCS_PATH}index.md", f"{CURRENT_DIR}/{DOCS_PATH}superwise.md")
    shutil.copyfile(f"{CURRENT_DIR}/index.md", f"{CURRENT_DIR}/{OUTPUT_DIR}index.md")
    shutil.copyfile(f"{CURRENT_DIR}/CHANGELOG.md", f"{CURRENT_DIR}/{OUTPUT_DIR}CHANGELOG.md")
    shutil.copytree(f"{CURRENT_DIR}/assets", f"{CURRENT_DIR}/{OUTPUT_DIR}assets")


def write_file(new_file, new_file_url):
    print(f"writing to file {new_file_url}")
    output_file = Path(new_file_url)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(new_file)


def main():
    copy_static_files()
    files = get_all_files()
    for file in files:
        if is_files_not_allowed(file):
            continue
        new_file = ""
        data = open(file, "r").readlines()
        for line in data:
            new_line = handle_line(line)
            new_file += new_line
        file_name = ("/").join(file.split("/")[1:])
        new_file_url = f"{CURRENT_DIR}/{OUTPUT_DIR}{file_name}"
        write_file(new_file, new_file_url)


if __name__ == "__main__":
    main()
