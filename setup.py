from setuptools import setup
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}


name = 'colorfy'
version = '0.1'
author = 'S. Semper, EMS Group TU Ilmenau'
release = '0.1'

setup(
    author=author,
    version=release,
    name=name,
    packages=[name],
    author_email='sebastian.semper@tu-ilmenau.de',
    description='Smart Handling of Color Schemes of TeX, HTML and Python',
    url='https://colorfy.readthedocs.io/en/latest/',
    license='LGPLv3+',
    keywords='colors',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or\
        later (LGPLv3+)',
        'Operating System :: POSIX :: Linux',
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'doc/source'),
            'build_dir': ('setup.py', 'doc/build'),
        }
    },
)
