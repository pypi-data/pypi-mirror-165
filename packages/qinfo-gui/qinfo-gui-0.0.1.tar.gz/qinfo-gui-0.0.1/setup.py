import codecs
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

VERSION = "0.0.1"
DESCRIPTION = "A gui for qinfo"


setup(
    name="qinfo-gui",
    version=VERSION,
    author="Decator (Aidan Neal)",
    author_email="decator.c@proton.me",
    url="https://github.com/El-Wumbus/qinfo-gui",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=["qinfo-python==0.1.2"],
    license='LGPLv3',
    entry_points = {'console_scripts': ['qinfo-gui = main:main']},
    keywords=["python", "gui", "gtk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: Unix",

    ]
)
