import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {"packages": ["os", "keyboard", "tkinter", "tkinter.ttk", "time", "threading", "win10toast", "pyperclip", "urllib.request", "json", "sys", "webbrowser", "psutil"]}
#include_files = ["my_first_file.png"]
# dans build_exe_options, { 'include_files': include_files }
setup(
    name = "Discord Spammer",
    description = "Discord Spammer by SiniKraft",
    version = "0.3",
    options = {"build_exe": build_exe_options},
    executables = [Executable("DiscordSpammer.py", base=base, copyright="© SiniKraft 2020-2021", icon="DiscordSpammer.ico", shortcut_name="Discord Spammer", shortcut_dir="DesktopFolder")],
)