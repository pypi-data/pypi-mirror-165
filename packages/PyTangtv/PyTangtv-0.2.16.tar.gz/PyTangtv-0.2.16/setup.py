

import sys
import setuptools
from distutils.core import setup
from glob import glob


install_requires = [
     'requests',
]
if sys.version_info < (3,):
    install_requires.append('tk')
    install_requires.append('pathlib2')
elif sys.version_info > (3,0) and sys.version_info < (3,5):
    install_requires.append('tk')
    install_requires.append('pathlib')
elif sys.version_info >= (3,5):
    install_requires.append('tk')

setup(
    name='PyTangtv',
    version='0.2.16',
    packages=['pytangtv','pytangtv.pymorph','pytangtv.pyalign','pytangtv.pymask','pytangtv.picker'],
    maintainer='Bill Meyer',
    maintainer_email='meyer8@llnl.gov',
    description="LLNL DIII-D diagnostic image tools",
    package_data={ "pytangtv":["bitmaps/*.xbm","bitmaps/*.png"],},
    scripts=['pytangtv/pyalign/pyalign','pytangtv/pymorph/pymorph','pytangtv/picker/picker','pytangtv/pymask/pymask'],
    license='LLNL',
    long_description=open('README.md').read(),
    classifiers = ['Programming Language :: Python',
                   'Programming Language :: Python :: 3'],
    install_requires = install_requires,
)

