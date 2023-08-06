#!/usr/bin/env python


from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='minifrpy',
      version='0.8',
      description='langage minimal',
      long_description=readme(),
      url='https://github.com/imenemes/mypylang',
      author='imen Lhocine',
      author_email='imen.mes@gmail.com',
      license='MIT',
      packages = find_packages(),
      install_requires = ['sly==0.4', 'beautifulsoup4==4.9.3', 'colorama==0.4.4', 'requests==2.26.0'],
      zip_safe=False)



