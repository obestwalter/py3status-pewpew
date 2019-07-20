# Standard
import getpass
import grp
import logging
import os
import shutil

# Cheese shop
from pathlib import Path


log = logging.getLogger(__name__)
HERE = Path(__file__).parent
MODULE_NAME = "code.py"
PY3STATUS_MODULE_PATH = HERE.parent / "src" / "pew3wm" / "pewpew.py"
PY3STATUS_CONFIG_PATH = ""


def first_existing(candidates):
    for candidate in candidates:
        print("Checking {}".format(candidate))
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
        configHomePath / ".config" / "py3status" / "modules",
        configHomePath / ".config" / "i3status" / "py3status",
        configHomePath / ".config" / "i3" / "py3status",
        configHomePath / ".i3" / "py3status",
    ]
    path = first_existing(candidates)
    if path is not None:
        log.info(f"deploy py3status module {PY3STATUS_MODULE_PATH} to {path}")
        shutil.copy(PY3STATUS_MODULE_PATH, path)
    else:
        raise Exception("Could not find a home for {}".format(MODULE_NAME))


def warn_if_user_not_in_expected_groups():
    user = getpass.getuser()
    groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
    groups = []
    expected_groups = ['input', 'dialout']
    for exp_group in expected_groups:
        if exp_group not in groups:
            print("Warning: user '{}' is not in expected group: '{}'".format(user, exp_group))


def main():
    logging.basicConfig(level=logging.DEBUG)
    warn_if_user_not_in_expected_groups()
    containerPath = find_container_path()
    if containerPath is None:
        raise Exception("Could not find pewpew; check cable!")
    deploy_pew_pew_control_module(containerPath)
    deploy_py3status_module()


if __name__ == "__main__":
    main()
