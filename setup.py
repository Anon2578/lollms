from pathlib import Path
from typing import Union

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(path: Union[str, Path]):
    with open(path, "r") as file:
        return file.read().splitlines()


requirements = read_requirements("requirements.txt")
requirements_dev = read_requirements("requirements_dev.txt")

def get_all_files(path):
    path = Path(path)
    file_list = []
    for file_path in path.rglob('*'):
        if file_path.is_file():
            if file_path.name != "__pycache__" and file_path.suffix !=".pyc" and  file_path.name!="local_config.yaml" and file_path.name!=".installed" and file_path.name!=".git" and file_path.name!=".gitignore":
                file_list.append("/".join(str(file_path).replace("\\","/").split("/")[1:]))
    return file_list

setuptools.setup(
    name="lollms",
    version="2.1.10",
    author="Saifeddine ALOUI",
    author_email="aloui.saifeddine@gmail.com",
    description="A python library for AI personality definition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ParisNeo/lollms",
    packages=setuptools.find_packages(),  
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'lollms-server = lollms.server:main',
            'lollms-console = lollms.console:main',
            'lollms-settings = lollms.settings:main',
        ],
    },
    extras_require={"dev": requirements_dev},
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
