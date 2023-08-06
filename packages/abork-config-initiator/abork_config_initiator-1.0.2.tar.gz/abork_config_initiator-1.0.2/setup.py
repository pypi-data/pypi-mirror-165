from setuptools import setup

with open("README.md") as file:
    readme_description = file.read()

setup(
    name='abork_config_initiator',
    version='1.0.2', 
    packages=['py_config_initiator'], 
    author='Alex Bork',
    license=open('LICENSE', 'r').read(),
    description="Configuration File Initiator",
    long_description=readme_description,
    long_description_content_type="text/markdown",
)