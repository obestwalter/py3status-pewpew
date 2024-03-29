# coding: utf-8
import getpass
import grp
import logging
import os
import shutil

import distro
from pathlib import Path

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
HERE = Path(__file__).parent
MODULE_NAME = "code.py"
PY3STATUS_MODULE_PATH = HERE.parent / "src/py3status_pewpew/pewpew.py"
PY3STATUS_CONFIG_PATH = ""


def main():
    warn_if_user_not_in_expected_groups()
    deploy_pew_pew_control_module()
    deploy_py3status_module()


def warn_if_user_not_in_expected_groups():
    expected_groups_by_distro = {"arch": ["uucp"], "ubuntu": ["input", "dialout"]}
    expected_groups = expected_groups_by_distro[distro.id()]
    user = getpass.getuser()
    groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
    for exp_group in expected_groups:
        if exp_group not in groups:
            log.info(f"warning: user '{user}' is not in expected group: '{exp_group}'")


def deploy_pew_pew_control_module():
    containerPath = find_container_path()
    if containerPath is None:
        raise Exception("Could not find pewpew; check cable!")
    assert containerPath.exists(), containerPath
    srcPath = HERE / MODULE_NAME
    dstPath = containerPath / MODULE_NAME
    print(f"deploying control module from {srcPath}...")
    if dstPath.exists():
        backupPath = dstPath.with_suffix(".bak")
        print(f"move existing {dstPath} to {backupPath}")
        dstPath.rename(backupPath)
    shutil.copy(srcPath, dstPath)
    assert srcPath.read_bytes() == dstPath.read_bytes(), "target != source; deploy fail?"
    print(f"...deployed control module to {dstPath}")


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
        raise Exception(f"could not find a home for {MODULE_NAME}")


def first_existing(candidates):
    for candidate in candidates:
        print(f"checking {candidate}")
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


if __name__ == "__main__":
    main()
