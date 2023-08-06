from setuptools import setup, find_packages
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('eesr')


requirements = ['domonic',
     'html5lib',
     'plotly',
     'pandas',
     'numpy',
     'entsoe-py'
     ]

setup(
    name='opendc-eesr',
    version='0.0.1',    
    description='An instrument for reporting data center energy efficiency and sustanability.',
    url='https://github.com/philippsommer27/opendc-eesr',
    author='Philipp Sommerhalter',
    author_email='philippsommerhalter@gmail.com',
    license='Apache Software License 2.0',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['eesr', 'eesr.reporting', 'eesr.analysis'],
    package_data={ '' : extra_files}
)