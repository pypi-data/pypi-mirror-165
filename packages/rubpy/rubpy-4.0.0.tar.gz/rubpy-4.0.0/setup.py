from setuptools import (setup, find_packages,)


requirements = ['pycryptodome', 'urllib3', 'websocket-client']


setup(
    name = 'rubpy',
    version = '4.0.0',
    author='Shayan Heidari',
    author_email = 'snipe4kill.tg@gmail.com',
    description = 'This is an unofficial library and fastest library for deploying robots on Rubika accounts.',
    keywords = ['rubika', 'rubpy', 'rubikaio', 'chat'],
    long_description = 'Loading...',
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/snipe4kill/rubika/',
    packages = find_packages(),
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)