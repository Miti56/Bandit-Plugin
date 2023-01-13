from setuptools import find_packages, setup

setup(
    name='Custom Bandit Checks',
    version='0.6.9',
    description='...',
    url='....',
    packages=['creditcard'],
    author='...',
    install_requires=[
        'bandit',
    ],
    entry_points={
        'bandit.plugins': [
            'stuff = creditcard.hardcoded_cc:hardcoded_creditcard_string',
        ],
    }
)

