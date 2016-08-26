from setuptools import setup


setup(
    name='pgrader',
    version='0.1.0',
    packages=['pgrader'],
    entry_points={
        'console_scripts': [
            'pgrader = pgrader.__main__:main'
        ]
    },
)
