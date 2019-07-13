from setuptools import setup, find_packages

setup(
    name="pew3wm",
    packages=find_packages(),
    install_requires=[
        "appdirs==1.4.3",
        "attrs==19.1.0",
        "black==19.3b0",
        "Click==7.0",
        "evdev==1.2.0",
        "future==0.17.1",
        "iso8601==0.1.12",
        "pyserial==3.4",
        "PyYAML==5.1.1",
        "toml==0.10.0",
    ],
    extras_require={"lint": ["pre-commit"], "test": ["pytest"]},
    entry_points={"console_scripts": ["pew3wm = pew3wm.pew3wm:cli"]},
)
