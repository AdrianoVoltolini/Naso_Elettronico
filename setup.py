from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
#build_exe_options = {
#    "excludes": ["tkinter", "unittest"],
#    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
#}

setup(
    name="Auto Nos",
    version="0.2",
    description="Applicazione per concatenamento ed analisi di file NOS",
    #options={"build_exe": build_exe_options},
    executables=[Executable("main_window.py", base="gui")],
)

