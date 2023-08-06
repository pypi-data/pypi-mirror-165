
# -*- coding:utf-8 -*-
###
#    Author:         Steven HELLEC
#    Creation Date:  Friday, August 26th 2022, 8:17:47 pm
###

from setuptools import setup, find_packages


setup(
    name='sh-crypt',
    version='1.0.0',
    description='Simple symmetric encryption and decryption (ECB) for text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/steven1909/sh-crypt.git',
    license='MIT license',
    author='Steven HELLEC',
    author_email='steven.hellc@live.fr',
    platforms=['any'],
    packages=["sh_crypt"],
    install_requires=['cryptography==37.0.4', 'cffi>=1.12', 'pycparser'],
    keywords='encryption,decryption,cipher,AES,ECB,crypto,cryptography',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: End Users/Desktop', 'Topic :: Security :: Cryptography',
        'Topic :: Security', 'Development Status :: 5 - Production/Stable',
        'Natural Language :: English', 'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX', 'Operating System :: Unix', 'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
)

