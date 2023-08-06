from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

setup(
    name='pargv',
    version='0.1.0',
    description='Parse command line arguments into a list of args and a dict of kwargs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        'dev':[
            'pytest',
        ]
    },
)
