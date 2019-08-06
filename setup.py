from setuptools import setup, find_packages

setup(
    name="py3status-pewpew",
    packages=find_packages(where="src"),
    install_requires=["evdev", "pyserial", "distro"],
    package_dir={"": "src"},
    extras_require={"lint": ["pre-commit"], "test": ["pytest", "py3status"]},
    entry_points={"py3status": ["module = py3status-pewpew.pewpew"]},
)
