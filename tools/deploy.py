import getpass
import shutil
import sys
from pathlib import Path


HERE = Path(__file__).parent
MODULE_NAME = "code.py"


def main():
    if len(sys.argv) > 1:
        containerPath = Path(sys.argv[1])
    else:
        user = getpass.getuser()
        containerPath = Path(f"/run/media/{user}/CIRCUITPY")
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


if __name__ == "__main__":
    main()
