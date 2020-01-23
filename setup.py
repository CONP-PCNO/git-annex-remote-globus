import setuptools

setuptools.setup(
    name='git-annex-remote-globus',
    version='1.0',
    author='Giulia Ippoliti',
    author_email='giuly.ippoliti@gmail.com',
    scripts=['git-annex-remote-globus'],
    keywords='git-annex remote globus',
    url='https://github.com/CONP-PCNO/git-annex-remote-globus',
    description='git annex special remote for Globus',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['annexremote==1.3.1', 'globus_sdk', 'pathlib'],
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Libraries',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)