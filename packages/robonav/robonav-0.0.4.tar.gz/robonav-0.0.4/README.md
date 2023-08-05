**Usage**

Run the command `robonav` to spin up a robot navigating on an open world. The available directions are up, down, left and right. The initial option allows you to recenter the robot on the specified coordinates.

**Deployment and Publishing**

To install the application locally, run `python setup.py install`.

To create the builds, `python setup.py sdist bdist_wheel`.

To publish to TestPyPi, `twine upload --repository-url https://test.pypi.org/legacy/ dist/*` or `twine upload --repository testpypi --config-file pypirc dist/*` or `twine upload --repository pypi --config-file pypirc dist/*`.