import os
import inspect
from setuptools import setup, find_packages
import pysqsd

setup(
    name='pysqsd',
    version="0.0.3",
    description="SQS Daemon inspired by Elastic Beanstalk's sqsd",
    author='Florent Vilmart',
    author_email='florentvilmart@me.com',
    url='http://github.com/flovilmart/pysqsd/tree/master',
    packages=find_packages(),
    zip_safe=False,
    license='MIT', 
    install_requires=[
        'boto',
    ],
    keywords='aws sqs queue',
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
