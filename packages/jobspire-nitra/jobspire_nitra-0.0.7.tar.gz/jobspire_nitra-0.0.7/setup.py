from setuptools import setup, find_packages

VERSION = '0.0.7' 
DESCRIPTION = 'Nitra'


with open("README.rst", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="jobspire_nitra", 
    version=VERSION,
    author="JobSpire team",
    author_email="<info@jobspire.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    url='https://github.com/HBS-Economics/nitra.git',
    install_requires=['requests'], # add any additional packages that 
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'nitra package'],
    python_requires='>=3.8',
)