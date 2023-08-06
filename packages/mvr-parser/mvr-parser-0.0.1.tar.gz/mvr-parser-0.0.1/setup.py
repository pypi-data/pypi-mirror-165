from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'MVR Parser'

# Setting up
setup(
    name="mvr-parser",
    version=VERSION,
    author="Harry Bilney",
    author_email="<harry@harrybilney.co.uk>",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'mvr'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)