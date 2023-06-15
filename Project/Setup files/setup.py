from setuptools import setup, find_packages

setup(
    name='myproj',
    version='1.0',
    author='Moiz',
    description='Dip project',
    # packages=find_packages(),
    packages=[''],
    entry_points={
        'console_scripts': [
            'gui_script = gui:main',
            'project_script = project:main',
        ]
    },
)
