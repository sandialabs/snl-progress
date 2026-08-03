import argparse
import shutil
import subprocess
import sys
import logging
from dataclasses import dataclass
from progress.paths import get_path

root_dir = get_path().parent
pcm_env_dir = root_dir / "progress" / "env_pcm"

class PCMInstallerError(RuntimeError):
    pass

@dataclass(frozen=True)
class PCMInstallCommand:
    program: str
    arguments: list[str]
    working_directory: object
    script_path: object

    def as_subprocess_args(self) -> list[str]:
        return [self.program, *self.arguments]

def get_pcm_env_dir():
    return pcm_env_dir

def get_pcm_python_executable():
    """
    Return the expected Python executable inside the PCM virtual environment.
    """
    if sys.platform.startswith("win"):
        return pcm_env_dir / "Scripts" / "python.exe"

    return pcm_env_dir / "bin" / "python"

def is_pcm_installed() -> bool:
    """
    PCM is considered installed only if the expected Python executable exists.

    Windows:
        root_dir/progress/pcm/Scripts/python.exe

    macOS/Linux:
        root_dir/progress/pcm/bin/python
    """
    python_exe = get_pcm_python_executable()
    return python_exe.exists() and python_exe.is_file()


def get_install_script_path():
    if sys.platform.startswith("win"):
        return root_dir / "install_pcm.bat"

    return root_dir / "install_pcm.sh"


def get_install_command() -> PCMInstallCommand:
    script_path = get_install_script_path()

    if sys.platform.startswith("win"):
        program = "cmd"
        arguments = ["/c", str(script_path)]
    else:
        program = "bash"
        arguments = [str(script_path)]

    return PCMInstallCommand(
        program=program,
        arguments=arguments,
        working_directory=root_dir,
        script_path=script_path,
    )

def install_pcm(*, force: bool = False, capture_output: bool = False) -> subprocess.CompletedProcess:
    """
    Install PCM by running pcm.bat on Windows or pcm.sh on macOS/Linux.
    PCM is considered installed if this directory exists:

        root_dir/progress/env_pcm
    """
    if is_pcm_installed() and not force:
        raise PCMInstallerError(
            f"PCM is already installed at:\n{pcm_env_dir}"
        )

    command = get_install_command()

    if not command.script_path.exists():
        raise PCMInstallerError(
            f"PCM install script not found:\n{command.script_path}"
        )

    result = subprocess.run(
        command.as_subprocess_args(),
        cwd=str(command.working_directory),
        text=True,
        capture_output=capture_output,
        check=False,
    )

    if result.returncode != 0:
        raise PCMInstallerError(
            f"PCM install failed with exit code {result.returncode}."
        )

    if not is_pcm_installed():
        raise PCMInstallerError(
            "PCM install script completed, but the PCM environment was not found at:\n"
            f"{pcm_env_dir}"
        )

    return result

def uninstall_pcm(*, missing_ok: bool = True) -> None:
    """
    Delete the PCM environment at:

        root_dir/progress/env_pcm

    Includes a safety check so an unexpected path is not deleted.
    """
    if not pcm_env_dir.exists():
        if missing_ok:
            return

        raise PCMInstallerError(
            f"PCM environment does not exist:\n{pcm_env_dir}"
        )

    env_dir_resolved = pcm_env_dir.resolve()
    expected_parent = (root_dir / "progress").resolve()

    if env_dir_resolved.name != "env_pcm" or env_dir_resolved.parent != expected_parent:
        raise PCMInstallerError(
            f"Refusing to delete unexpected path:\n{env_dir_resolved}"
        )
    shutil.rmtree(env_dir_resolved, onerror=remove_readonly)

def remove_readonly(func, path, exc_info):
        """
        Error handler for shutil.rmtree on Windows.
        Makes the file writable and retries the failed operation.
        """
        import os
        import stat
        os.chmod(path, stat.S_IWRITE)
        func(path)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install, uninstall, or check PCM.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install", help="Install PCM.")
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Run installer even if root_dir/progress/env_pcm already exists.",
    )

    subparsers.add_parser("uninstall", help="Uninstall PCM.")
    subparsers.add_parser("status", help="Show PCM installation status.")

    args = parser.parse_args(argv)

    try:
        if args.command == "install":
            if is_pcm_installed() and not args.force:
                print(f"PCM is already installed at: {pcm_env_dir}")
                return 0

            print(f"Installing PCM from root directory: {root_dir}")
            install_pcm(force=args.force, capture_output=False)
            print(f"PCM installed successfully at: {pcm_env_dir}")
            return 0

        if args.command == "uninstall":
            if not is_pcm_installed():
                print("PCM is not installed.")
                return 0

            uninstall_pcm()
            print("PCM uninstalled successfully.")
            return 0

        if args.command == "status":
            if is_pcm_installed():
                print(f"PCM is installed at: {pcm_env_dir}")
                return 0

            print("PCM is not installed.")
            return 1

    except PCMInstallerError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())