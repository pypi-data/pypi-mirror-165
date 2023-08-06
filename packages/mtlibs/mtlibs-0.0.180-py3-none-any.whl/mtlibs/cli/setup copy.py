from setuptools import setup
import setuptools
import os
import shutil
from pathlib import Path
import re

import os
import sysconfig


from setuptools import setup, find_packages

# https://stackoverflow.com/questions/21594925/error-each-element-of-ext-modules-option-must-be-an-extension-instance-or-2-t
# 注意，这个顺序必须在这里，要比setup低.
# from Cython.Build import cythonize

from setuptools.command.build_py import build_py as _build_py

package_name = "mtxcli"
# version = ""
# with open(f'__init__.py', 'r') as fd:
#     version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
#                         fd.read(), re.MULTILINE).group(1)
    

version_file = Path(__file__).parent.joinpath("version.txt")
print(f"version file : {version_file}")
f = open(version_file,"r")
version = f.read()
f.close()

def gen_data_files(*dirs):
    print("gen_data_files =========================================================", dirs)
    results = []
    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            results.append((root, map(lambda f: root + "/" + f, files)))
    print("gen_data_files result ===============", results)
    return results

# 上一个构建的残留会影响打包文件，所以这里先清除。
print("清理目录")
build_dir = os.path.join(os.getcwd(),"build")
if Path(build_dir).exists():        
    shutil.rmtree(build_dir)

packages = setuptools.find_packages(
    exclude=("test", "mtxcms*", "mtx_cloud.*", "mtxauth*", "gallery*"))
print("all packages", packages)

if os.path.exists("requirements.txt"):
    install_requires = open("requirements.txt").read().split("\n")
else:
    install_requires = []
    
setup(name='mtxcli',
    version=version,
    description='The funniest joke in the world',
    long_description='long_description',  # readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='funniest joke comedy flying circus',
    url='http://github.com/storborg/funniest',
    author='Flying Circus',
    author_email='flyingcircus@example.com',
    license='MIT',
    package_dir={
        'mtxcli': '.'
    },
    # package_dir={'mtxcli': '.'},
    # packages=setuptools.find_packages(exclude=("test",)),
    packages=['mtxcli', 
    ],
    install_requires = install_requires,       # 常用
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    include_package_data=True,
    package_data={
    #   'demo': ['data/*.txt'],
        # 'mtxcli': ['data/*.conf'],
    },
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'dockerdev=mtxcli.dockerdev:main',
            'gitup=mtxcli.gitup:main',
            'dc=mtxcli.dc:main',
            'mtgp=mtxcli.mtgp_init:main',
            'mtdp=mtxcli.mtdp:main',
            'mtpublish=mtxcli.mtpublish:main',
            'mtngrok=mtxcli.mtngrok:main'
        ]
    },
    # scripts=['mtxcli/dc.py'],
)