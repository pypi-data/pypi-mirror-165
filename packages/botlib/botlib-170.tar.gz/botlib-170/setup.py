# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botlib",
    version="170",
    url="https://github.com/bthate/botlib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="The Python3 bot Namespace",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=["bot"],
    zip_safe=False,
    install_requires=["oplib"],
    include_package_data=True,
    scripts=["bin/bot"],
    data_files=[
                ("share/doc/botlib", ["README.rst",]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
