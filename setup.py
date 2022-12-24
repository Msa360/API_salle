from setuptools import setup

setup(
    name='cgs',
    author='msa360',
    author_email='arnaud25@icloud.com',
    data_files=[("", ["configtemplate.json"])],
    entry_points={'console_scripts': ['cgs=cgs.cli:cli']}
)