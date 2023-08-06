from setuptools import setup, find_packages

MAJOR = 1
MINOR = 0
PATCH = 0
VERSION = "{}.{}.{}".format(MAJOR, MINOR, PATCH)

with open("mrccleaner/version.py", "w") as f:
    f.write("__version__ = '{}'\n".format(VERSION))


setup(
    name='mrccleaner',
    version=VERSION,
    url='https://github.com/tubiana/MRCcleaner',
    license='MIT',
    author='Thibault Tubiana',
    author_email='tubiana.thibault@gmail.com',
    description='MRCcleaner: a simple script for MRC transformation when they are not centered.',
    platforms=["Linux", "Solaris", "Mac OS-X", "darwin", "Unix", "win32"],
    install_requires=['numpy',
                      'mrcfile',
                      'argparse',
                      ],

    entry_points={'console_scripts':['mrccleaner=mrccleaner.mrccleaner:main']},


    packages=find_packages(),
)