import shutil
import subprocess
from pathlib import Path


def main():
    # Define directories
    current_dir = Path(__file__).parent.resolve()
    root_dir = current_dir.parent.resolve()
    build_dir = root_dir / "build"
    dist_dir = root_dir / "dist"
    # resources_dir = root_dir / "resources"

    for exe_name in ["main.exe", "Doro.exe"]:
        exe_path = dist_dir / exe_name
        if exe_path.exists():
            exe_path.unlink()

    # Run the build script
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",
        "-w",
        f"--distpath={dist_dir}",
        # f"--icon={resources_dir / 'icons/favicon.ico'}",
        str(root_dir / "main.py"),
        "--clean",
    ]
    subprocess.run(pyinstaller_cmd, check=True)

    # Rename the exe
    exe_name = "main.exe"
    new_exe_name = "Doro.exe"
    src_exe = dist_dir / exe_name
    dst_exe = dist_dir / new_exe_name
    if src_exe.exists():
        src_exe.rename(dst_exe)

    # Clear the build directory
    pycache_dir = build_dir / "__pycache__"
    main_dir = build_dir / "main"
    for d in [pycache_dir, main_dir]:
        if d.exists() and d.is_dir():
            shutil.rmtree(d, ignore_errors=True)
    for spec_file in [build_dir / "main.spec", root_dir / "main.spec"]:
        if spec_file.exists():
            spec_file.unlink()


if __name__ == "__main__":
    main()
