from setuptools import find_packages, setup

setup(
    name='groupme-bot',
    version='0.0.2',
    description='GroupMe bot',
    author='Quinn Weber',
    maintainer='Quinn Weber',
    maintainer_email='quinnsweber@gmail.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=(
        'flask',
    ),
)
