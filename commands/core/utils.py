import os
import subprocess


def open_in_editor(file_path):
    """Open file in current editor (Cursor or VSCode)"""
    abs_path = os.path.abspath(file_path)

    # Try Cursor first
    try:
        subprocess.run(
            ["cursor", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(["cursor", "--goto", abs_path])
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback to VSCode
    try:
        subprocess.run(
            ["code", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(["code", "--reuse-window", "--goto", abs_path])
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Neither Cursor nor VSCode found in PATH")
