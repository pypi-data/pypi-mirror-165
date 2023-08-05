from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'A simple robot runner'
LONG_DESCRIPTION = 'A simple robot runner to control a robot on an open world. Run the command "robonav" to start exploring.'
LICENSE = "MIT"

# Setting up
setup(
    name="robonav",
    version=VERSION,
    author="LiveByTheCode (Archer EarthX)",
    author_email="<archerearthx@gmail.com>",
    license=LICENSE,
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