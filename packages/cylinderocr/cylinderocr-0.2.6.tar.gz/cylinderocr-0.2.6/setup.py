import setuptools
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "cylinderocr"
AUTHOR_USER_NAME = "Codebugged-Research"
SRC_REPO = "src"


setuptools.setup(
    name="cylinderocr",
    version="0.2.6",
    author=AUTHOR_USER_NAME,
    description="cylinder  ocr package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="thecodebugged@gmail.com",
    package_dir={'': "src"},
    python_requires=">=3.6",
    packages=setuptools.find_packages(where="src"),
    license="MIT",
    install_requires=['paddleocr',
                  'paddlepaddle',
                   'getmac',],
        classifiers=[
        'Intended Audience :: Developers', 'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6', 'Topic :: Utilities',
        'Programming Language :: Python :: 3.7', 'Topic :: Utilities',
        'Programming Language :: Python :: 3.8', 'Topic :: Utilities'
    ], )
