import setuptools
import vru

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="vr.utils",
    version=vru.__version__,
    author="Vladimir Rukavishnikov",
    author_email="RukavishnikovVV@mail.ru",
    description="Python utilities.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["vru", "vru.*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        "fastapi==0.78.0",
        "tortoise-orm==0.19.0",
        "loguru==0.6.0",
    ],

    python_requires='>=3.10',
)