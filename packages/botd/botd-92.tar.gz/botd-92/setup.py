# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="botd",
    version="92",
    url="https://github.com/bthate/botd",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="24/7 channel daemon",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    zip_safe=False,
    install_requires=["botlib"],
    include_package_data=True,
    data_files=[
                ("share/botd", ["files/botd.service",]),
                ("share/doc/botd", ["README.rst",]),
    ],
    scripts=["bin/botcmd", "bin/botctl", "bin/botd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
)
