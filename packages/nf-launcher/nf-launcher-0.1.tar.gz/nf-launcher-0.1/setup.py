from setuptools import setup

__version__ = 0.1

setup(
    name='nf-launcher',
    version=__version__,
    author='Jordi Deu-Pons',
    description='Installs the Nextflow launcher',
    scripts=['launcher/nextflow'],
    long_description="""
## Description
 - Install Nextflow launcher using `pip install nf-launcher`. 
 - Now `nextflow` command is available on your path.
 - Run `nextflow info` to force it download all the dependencies (only the first time).
 - Now you are ready to run a pipeline `nextflow run hello`. 

## Requirements
The Nextflow launcher requires Java and curl or wget available on your
system to be able to download Nextflow java dependencies and launch Nextflow
""",
    long_description_content_type="text/markdown",
    license="MPL-2",
    keywords=["pipeline", "workflow", "nextflow"],
    install_requires=[],
    classifiers=[]
)
