# Author: Daisuke Komura <kdais-prm@m.u-tokyo.ac.jp>
# Copyright (c) 2022 Daisuke Komura
# License: This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC-BY-NC-SA 4.0)

from setuptools import setup
import deepsemhist

DESCRIPTION = "deep_semantic_histology: Deep Semantic Representations for Cancer Histology Images"
NAME = 'deepsemhist'
AUTHOR = 'Daisuke Komura'
AUTHOR_EMAIL = 'kdais-prm@m.u-tokyo.ac.jp'
URL = 'https://github.com/dakomura/deep_texture_histology'
LICENSE = 'CC-BY-NC-SA 4.0'
DOWNLOAD_URL = 'https://github.com/dakomura/deep_texture_histology'
VERSION = deepsemhist.__version__
PYTHON_REQUIRES = ">=3.6"
ENTRY = {"console_scripts":[
    "segpatch=deepsemhist.segpatch:main",
    "segslide=deepsemhist.segslide:main",
]}

INSTALL_REQUIRES = [
    'numpy',
    'joblib',
    'Pillow',
    'matplotlib',
    'seaborn',
    'pandas',
    'pyrsistent',
]

PACKAGES = [
    'deepsemhist'
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
]

with open('README.rst', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS,
      entry_points=ENTRY,
)
