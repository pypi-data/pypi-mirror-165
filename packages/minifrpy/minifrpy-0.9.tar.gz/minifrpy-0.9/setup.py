#!/usr/bin/env python


from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='minifrpy',
      version='0.9',
      description='langage minimal',
      long_description=readme(),
      url='https://github.com/imenemes/mypylang',
      author='imen Lhocine',
      author_email='imen.mes@gmail.com',
      license='MIT',
      packages = find_packages(),
      install_requires = ['sly', 'beautifulsoup4', 'colorama', 'requests'],
      entry_points={
        'console_scripts': [
            'mypyfr = mypy.interpreter:main',
        ],
        },
      zip_safe=False)



