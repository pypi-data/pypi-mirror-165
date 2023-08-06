from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Scrap data from Fundamentus.'

setup(
    name="fundamentus-py",
    version=VERSION,
    author="Nikolas Silva",
    author_email="<nikolas.rsilva@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="TODO: Add README",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'fundamentus'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)