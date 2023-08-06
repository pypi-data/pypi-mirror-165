from os import name, listdir

from setuptools import setup

requirements = ["aiomultiprocess", "dill", "websocket-client"]

if name.lower() != "nt":
    requirements += ["uvloop"]

with open("version", "r") as f:
    version = f.read().rstrip("\n")

with open("README.md", "r") as f:
    readme = f.read()
    
setup(
    name="lightStart",
    version=version,
    long_description=readme,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Terminals",
    ],
    keywords=["discord", "self-bot", "dank-memer", "python", "python3"],
    description="A fast, free, and open-source Dank Memer self-bot.",
    url="https://github.com/splewdge/lightStart",
    author="splewdge",
    author_email="splewdge@proton.me",
    license="GNU AFFERO GENERAL PUBLIC LICENSE",
    zip_safe=False,
    entry_points={"console_scripts": ["lightStart=lightStart.__main__:start"]},
    packages=["lightStart"],
    package_dir={
        "database": "lightStart/database",
        "discord": "lightStart/discord",
        "utils": "lightStart/utils",
    },
    include_package_data=True,
)