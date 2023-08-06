#!/usr/bin/env python

import re
import setuptools
import os
import shutil
from pathlib import Path


# with open("README.md", "r") as fh:
#     long_description = fh.read()

# packages = setuptools.find_packages(exclude=("test","sm*","mtxcm*","mtxcli*")),
# print("all packages")
# print(packages)

package_name = "mtlibs"
# print("package_name", package_name)
# version = ""
# with open(f'__init__.py', 'r') as fd:
#     version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
#                         fd.read(), re.MULTILINE).group(1)
    
version_file = Path(__file__).parent.joinpath("version.txt")
print(f"version file : {version_file}")
f = open(version_file,"r")
version = f.read()
f.close()

# 上一个构建的残留会影响打包文件，所以这里先清除。
print("清理目录")

build_dir = os.path.join(os.getcwd(),"build")
print(f"build_dir: {build_dir}")
if Path(build_dir).exists():        
    shutil.rmtree(build_dir)
    
if os.path.exists("requirements.txt"):
    install_requires = open("requirements.txt").read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name=package_name,
    version=version,
    author="example",
    author_email="author@example.com",
    description="This is the SDK for example.",
    long_description="demo",
    long_description_content_type="text/markdown",
    url="http://example.com",
    # install_requires=[
    #     'requests',
    # ],
    install_requires = install_requires,       # 常用

    # build_dir=build_dir, #没按预期工作。
    # package_dir={
    #     package_name: package_name
    # },
    package_dir={'mtlibs': 'mtlibs'},
    # packages=setuptools.find_packages(exclude=("test",)),
    packages=['mtlibs', 
              'mtlibs.aws', 
              'mtlibs.cli', 
              'mtlibs.az',
              "mtlibs.service",
              "mtlibs.tests",
              "mtlibs.installers",
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
    
    exclude_package_data={'': ["mtlibs/test.py", "mtlibs/config.txt"]},

    zip_safe=True,
    entry_points = {
        'console_scripts': [
            # 'mtlibs = mtlibs.main:main',
            'dockerdev=mtlibs.cli.dockerdev:main',
            'gitup=mtlibs.cli.gitup:main',
            'dc=mtlibs.cli.dc:main',
            'dc3=mtlibs.cli.dc:main',
            'mtgp=mtlibs.cli.mtgp_init:main',
            'mtdp=mtlibs.cli.mtdp:main',
            'mtpub=mtlibs.cli.mtpublish:main',
            
        ]
    }
)