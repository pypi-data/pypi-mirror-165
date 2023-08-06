from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pyroborock_fork',
    version='1.1.10',
    packages=['pyroborock_fork'],
    install_requires=['pytuyapi-ipc==1.0.4', 'python-miio==0.5.12', 'pycryptodome==3.15.0'],
    description='Communicate with roborock over tuya protocol',
    long_description=read('README.md'),
    long_description_content_type='text/markdown'
)
