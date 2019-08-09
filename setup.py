from pathlib import Path

from setuptools import setup, find_packages


def make_long_description():
    here = Path(__file__).parent
    readme = (here / "README.md").read_text()
    changelog = (here / "CHANGELOG.md").read_text()
    return f"{readme}\n\n{changelog}"


setup(
    name="py3status-pewpew",
    version="0.2",
    description="py3status module to control i3wm with the PewPew",
    long_description=make_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    install_requires=["py3status>=3.20", "evdev", "pyserial", "distro"],
    package_dir={"": "src"},
    extras_require={"lint": ["pre-commit"], "test": ["pytest", "py3status"]},
    entry_points={"py3status": ["module = py3status_pewpew.pewpew"]},
    url="https://github.com/obestwalter/py3status-pewpew",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

)
