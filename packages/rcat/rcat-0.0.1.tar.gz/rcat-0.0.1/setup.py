from src.VERSION import VERSION as version
from setuptools  import setup





# with open('VERSION.txt') as f:
#     version = f.read()

with open('requirements.txt') as f:
    requirements = f.read().split('\n')
    requirements = [i for i in requirements if i]






setup(
    name = 'rcat',
    version = version,
    description = 'cat but prints contents using rich.print',
    platforms = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    install_requires = requirements,
    package_dir = {'': 'src'},
    entry_points = {
        'console_scripts': [
            'rcat = rcat:init_main',
        ]
    },
    project_urls={
        'Bug Tracker': 'https://github.com/msr8/rcat/issues',
        'Source Code': 'https://github.com/msr8/rcat',
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS'
    ]
)








'''
name:        what you will pip install, not import
py_modules:  what they will import

!! NAME OF THE MAIN FILE IN THE src DIR SHOULD BE SAME AS PACKAGE NAME
'''


