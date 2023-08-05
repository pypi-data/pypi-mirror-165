from setuptools import setup
long_description = open("README.md").read()

setup(name="anylinux",
version="0.0.01",
description="Ultimate tool for installing any LINUX in termux.",
long_description=long_description,
long_description_content_type='text/markdown',
author="NISHANT2009",
url="https://github.com/Nishant2009/anylinux",
scripts=["anylinux"],
install_requires= ['colourfulprint'],
classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
], )
