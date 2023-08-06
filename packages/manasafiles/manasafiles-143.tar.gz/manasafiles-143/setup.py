import setuptools
import sys


vr = sys.argv[1]
del sys.argv[1]



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='manasafiles',
    version= vr,
    author='manasa',
    author_email='manasabalagoni1@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/manasabalagoni/python-second',
    project_urls = {
        "Bug Tracker": "https://github.com/manasabalagoni/python-second/issues"
    },
    license='MIT',
    packages=['manasafiles'],
    install_requires=['requests'],
    
    
)
