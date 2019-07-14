import getpass
import logging
import os
import shutil
from pathlib import Path


log = logging.getLogger(__name__)
HERE = Path(__file__).parent
MODULE_NAME = "code.py"
PY3STATUS_MODULE_PATH = HERE.parent / "src" / "pew3wm" / "pewpew.py"
PY3STATUS_CONFIG_PATH = ""


def first_existing(candidates):
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def find_container_path():
    user = getpass.getuser()
    candidates = [
        Path(f"/run/media/{user}/CIRCUITPY"),
        Path(f"/media/{user}/CIRCUITPY"),
    ]
    return first_existing(candidates)


def main():
    logging.basicConfig(level=logging.DEBUG)
    containerPath = find_container_path()
    if containerPath is None:
        print("Could not find pewpew; check cable!")
        return
    deploy_pew_pew_control_module(containerPath)
    deploy_py3status_module()


def deploy_pew_pew_control_module(containerPath):
    assert containerPath.exists(), containerPath
    srcPath = HERE / MODULE_NAME
    dstPath = containerPath / MODULE_NAME
    print(f"deploy control module to {srcPath}")
    if dstPath.exists():
        backupPath = dstPath.with_suffix(".bak")
        print(f"move existing {dstPath} to {backupPath}")
        dstPath.rename(backupPath)
    shutil.copy(srcPath, dstPath)
    print(f"deployed control module to {dstPath}")


def deploy_py3status_module():
    configHomePath = Path(os.getenv("XDG_CONFIG_HOME", "~")).expanduser()
    candidates = [
        configHomePath / ".config/py3status/modules",
        configHomePath / ".config/i3status/py3status",
        configHomePath / ".config/i3/py3status",
        configHomePath / ".i3/py3status",
    ]
    path = first_existing(candidates)
    if path is not None:
        log.info(f"deploy py3status module {PY3STATUS_MODULE_PATH} to {path}")
        shutil.copy(PY3STATUS_MODULE_PATH, path)
    else:
        raise Exception("Could not find a home for pewpew")


if __name__ == "__main__":
    main()
