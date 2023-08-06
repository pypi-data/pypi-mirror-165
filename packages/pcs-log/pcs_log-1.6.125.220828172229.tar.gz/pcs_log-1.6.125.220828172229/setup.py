#!/usr/bin/env python3
# vim: expandtab:ts=4:sw=4:noai

""" Setup LogP """
import setuptools
from pcs_log.LogP import Version

with open("pcs_log/README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
Requirements = []
try:
    with open('pcs_log/requirements.txt','r',encoding='utf-8') as f:
        Requirements = [x for x in  [y.strip() for y in f.readlines()] if x]
except:                     # pylint: disable=bare-except
    pass

setuptools.setup(
    name="pcs_log",
#    version="0.6.7",
    version = Version,
    python_requires='>=3.6',
    author="Rainer Pietsch",
    author_email="r.pietsch@pcs-at.com",
    description="Generic logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pcs-log.readthedocs.io/en/latest/",
    download_url="https://github.com/rpietsch1953/Log",
    packages=setuptools.find_packages(),
    install_requires=Requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)
#----------------------------------------------------------------------
