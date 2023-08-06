from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'ArabicTextNormalization'
LONG_DESCRIPTION = 'ArabicTextNormalization package used to Normalize Arabic Text into standard format '

# Setting up
setup(
    name="ArabicTextNormalization",
    version=VERSION,
    author="Yousif Ahmed Alhaj",
    author_email="yalhag@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'Arabic text preprocessing', 'Arabic text classification', 'Arabic text Normalization', 'Arabic sentiment ana;ysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
