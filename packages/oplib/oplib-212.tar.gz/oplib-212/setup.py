# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="oplib",
    version="212",
    url="https://github.com/bthate/oplib",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="object programming library",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=['op'],
    scripts=["bin/op"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
