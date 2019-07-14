import getpass
import shutil
import sys
from pathlib import Path


HERE = Path(__file__).parent
MODULE_NAME = "code.py"


def main():
    user = getpass.getuser()
    container_path = Path(f"/run/media/{user}/CIRCUITPY")
    assert container_path.exists(), f"Expected pewpew at {container_path}; check cable!"
    src_path = HERE / MODULE_NAME
    dst_path = container_path / MODULE_NAME
    print(f"deploy control module to {src_path}")
    if dst_path.exists():
        backup_path = dst_path.with_suffix(".bak")
        print(f"move existing {dst_path} to {backup_path}")
        dst_path.rename(backup_path)
    shutil.copy(src_path, dst_path)
    print(f"deployed control module to {dst_path}")


if __name__ == "__main__":
    main()
