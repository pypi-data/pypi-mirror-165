from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'A simple robot runner'
LONG_DESCRIPTION = 'A package that allows to control a robot using custom language.'

# Setting up
setup(
    name="robonav",
    version=VERSION,
    author="LiveByTheCode (Archer EarthX)",
    author_email="<archerearthx@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['textx'],
    include_package_data=True,
    package_data={"": ["*.tx","*.rbt"]},
    entry_points={
          'console_scripts': [
              'robonav=robonav:navigator',
          ]
    },
    keywords=['python', 'textx', 'dsl', 'robot', 'state machine'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)