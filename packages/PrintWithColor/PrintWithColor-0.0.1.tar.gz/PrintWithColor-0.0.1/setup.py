from setuptools import setup
# read the contents of your README file
with open("C:\\Users\\Harry\\Desktop\\abcdefgh\\TextEditor\\PrintWithColor" + "\\ReadMe.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()
    

setup(
    name='PrintWithColor',
    version = "0.0.1",
    description =" A tiny  wrapper for colorama library that enhances the print() syntax by enabling text coloring on the screen",
    long_description=long_description,
    long_description_content_type='text11/markdown',
    authors = "SweetSea-ButNotSweet",
    readme = "ReadMe.md",
    license = "LICENSE",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages = ['PrintWithColor'],
)