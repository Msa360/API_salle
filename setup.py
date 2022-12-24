from setuptools import setup
import os, re

with open("README.md", "r") as f:
    long_desc = f.read()

with open("requirements.txt", "r") as f:
    requirements = [line.rstrip() for line in f]

SRC = os.path.abspath(os.path.dirname(__file__))


def get_version():
    with open(os.path.join(SRC, 'cgs/__init__.py')) as f:
        for line in f:
            m = re.match("__version__ = \"(.*)\"", line)
            if m:
                return m.group(1)
    raise SystemExit("Could not find version string.")

setup(
    name='cgs',
    version=get_version(),
    packages=['cgs'],
    author='msa360',
    url="https://github.com/Msa360/cgs-csfoy-gym",
    license='MIT',
    description="Create & update reservations at Cégep Sainte-Foy gym with this simple api.",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    author_email='arnaud25@icloud.com',
    data_files=[("~/.config", ["configcgs.json"])], # todo change path
    entry_points={'console_scripts': ['cgs=cgs.cli:cli']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License'
    ]
)