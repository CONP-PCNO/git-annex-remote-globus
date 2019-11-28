from distutils.core import setup

setup(
    name='git-annex-remote-globus',
    version='0.1',
    author='Giulia Ippoliti',
    author_email='giuly.ppoliti@gmail.com',
    scripts=['git-annex-remote-globus'],
    url='https://github.com/CONP-PCNO/git-annex-remote-globus',
    description='git annex special remote for Globus',
    long_description=open('README.md').read()
)