import os
import inspect
from setuptools import setup, find_packages
import pysqsd

setup(
    name='pysqsd',
    version="0.0.1",
    description="SQS Daemon inspired by Elastic Beanstalk's sqsd",
    author='Florent Vilmart',
    author_email='flo@flovilmart.com',
    url='http://github.com/flovilmart/pysqsd/tree/master',
    packages=find_packages(),
    zip_safe=False,
    license='ISC', 
    install_requires=[
        'boto',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ], 
    entry_points = {
          'console_scripts': [
                'pysqsd = pysqsd:main', 
          ],
    },
)
