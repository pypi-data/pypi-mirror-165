import os
import setuptools

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name="Open3dLite",
    version="0.0.2",
    author="Muhammad Haroon",
    author_email="muhammad.haroon44@gmail.com",
    description="An easy syntax of Python Package Open3d",
    long_description="An easy syntax of Python Package Open3d",
    long_description_content_type="text/markdown",
    url="https://github.com/haroon4412/open3d_lite.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
