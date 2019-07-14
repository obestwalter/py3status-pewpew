import getpass
import logging
import os
import shutil
import sys
from pathlib import Path


log = logging.getLogger(__name__)
HERE = Path(__file__).parent
MODULE_NAME = "code.py"
PY3STATUS_MODULE_PATH = HERE.parent / "src" / "pew3wm" / "pewpew.py"
PY3STATUS_CONFIG_PATH = ""


def main():
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        containerPath = Path(sys.argv[1])
    else:
        user = getpass.getuser()
        containerPath = Path(f"/run/media/{user}/CIRCUITPY")
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
        ".config/py3status/modules",
        ".config/i3status/py3status",
        ".config/i3/py3status",
        ".i3/py3status",
    ]
    for candidate in candidates:
        path = configHomePath / candidate
        if path.exists():
            log.info(f"deploy py3status module {PY3STATUS_MODULE_PATH} to {candidate}")
            shutil.copy(PY3STATUS_MODULE_PATH, path)


if __name__ == "__main__":
    main()
