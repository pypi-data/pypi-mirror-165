from setuptools import dist, find_packages, setup, Extension

# To compile and install locally run "python setup.py build_ext --inplace"
# To install library to Python site-packages run "python setup.py build_ext install"

install_requires = [
    'setuptools>=18.0',
    'cython>=0.27.3',
    'matplotlib>=2.1.0',
    'numpy>=1.17.5'
]

dist.Distribution().fetch_build_eggs(install_requires)

import numpy as np
ext_modules = [
    Extension(
        'pycocotools._mask',
        sources=['./common/maskApi.c', 'pycocotools/_mask.pyx'],
        include_dirs=[np.get_include(), './common'],
        extra_compile_args=['-Wno-cpp', '-Wno-unused-function', '-std=c99'],
    )
]

setup(
    name='wf-pycocotools',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    description="Forked version of the cocodataset's pycocotools modified to install from pypi without manual intervention",
    version='2.0.1.4',
    url='https://github.com/WildflowerSchools/cocoapi',
    author='Piotr Dollar, Tsung-Yi Lin, Benjamin Jaffe-Talberg',
    author_email='ben.talberg@wildflowerschools.org',
    ext_modules=ext_modules
)
