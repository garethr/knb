from setuptools import setup

setup(
    name='knb',
    author='Gareth Rushgrove',
    author_email='gareth@morethanseven.net',
    version='0.1.0',
    license='Apache License 2.0',
    packages=['knb',],
    install_requires=[
        'tabulate',
        'colorama',
	'click',
    ],
    tests_require=[

    ],
    entry_points={
        'console_scripts': [
            'knb = knb.command:cli',
       ]
    },
    keywords = 'kubernetes, knative',
    description = 'A utility to help work with Knative Build',
    url = "https://github.com/garethr/knb/",
)
