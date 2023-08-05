from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name             = 'pyPilot',
    packages         = ['pyPilot'],
    version          = '0.2.0',
    description      = 'Python package for navigation, guidance, path planning, and control',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    author           = 'Power_Broker',
    author_email     = 'gitstuff2@gmail.com',
    url              = 'https://github.com/PowerBroker2/pyPilot',
    download_url     = 'https://github.com/PowerBroker2/pyPilot/archive/0.2.0.tar.gz',
    keywords         = ['pyPilot'],
    classifiers      = [],
    install_requires = ['numpy', 'scipy']
)
