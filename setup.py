from distutils.core import setup

setup(
    name='git-annex-remote-globus',
    version='0.1',
    author='Giulia Ippoliti',
    author_email='giuly.ippoliti@gmail.com',
    scripts=['git-annex-remote-globus'],
    keywords='git-annex remote globus',
    url='https://github.com/CONP-PCNO/git-annex-remote-globus',
    description='git annex special remote for Globus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['annexremote==1.3.1'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)