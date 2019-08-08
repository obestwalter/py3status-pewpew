from setuptools import setup, find_packages

setup(
    name="py3status-pewpew",
    version="0.1",
    packages=find_packages(where="src"),
    install_requires=["evdev", "pyserial", "distro"],
    package_dir={"": "src"},
    extras_require={"lint": ["pre-commit"], "test": ["pytest", "py3status"]},
    entry_points={"py3status": ["module = py3status_pewpew.pewpew"]},
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
