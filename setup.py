from setuptools import setup, find_packages

setup(
    name="pew3wm",
    packages=find_packages(where="src"),
    install_requires=["evdev", "pyserial"],
    package_dir={"": "src"},
    extras_require={"lint": ["pre-commit"], "test": ["pytest"]},
    entry_points={"console_scripts": ["pew3wm = pew3wm.pew3wm:cli"]},
)
