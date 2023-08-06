from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Collecting images for GTA sel-driving car project'
LONG_DESCRIPTION = 'A package that allows to setup automated script to easily collect dataset for training ' \
                   'neural networks on in game images'

# Setting up
setup(
    name="pygta-data-collector",
    version=VERSION,
    author="MrKubul (Jakub Dryka)",
    author_email="<szanowac@dziekana.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'keyboard', ' Pillow', 'numpy', 'mss'],
    keywords=['python', 'gta', 'ai', 'deep learning', 'dataset', 'dziekan'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)