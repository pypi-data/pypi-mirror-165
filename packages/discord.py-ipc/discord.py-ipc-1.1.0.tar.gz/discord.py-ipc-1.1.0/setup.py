from setuptools import setup
import re

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("discord/ext/ipc/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("Version is not set.")

with open("README.md") as f:
    readme = f.read()

extras_require = {
    "docs": [
        "sphinx",
        "sphinxcontrib_trio",
        "sphinx-rtd-theme",
    ],
}

packages = [
    "discord.ext.ipc",
]

setup(
    name="discord.py-ipc",
    author="Sn1F3rt",
    url="https://github.com/Sn1F3rt/discord.py-ipc",
    project_urls={
        "Documentation": "https://discordpy-ipc.readthedocs.io/en/latest/",
        "Issue Tracker": "https://github.com/Sn1F3rt/discord.py-ipc/issues",
    },
    version=version,
    packages=packages,
    license="Apache Software License",
    description="A discord.py extension for inter-process communication.",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.8.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
