from setuptools import setup, find_packages

import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('ecldoc/Templates')
print(extra_files)
setup(
    name="HPCCSystemsECLDOc",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        'Jinja2==2.9.6',
        'lxml==4.9.0',
        'importlib-metadata==4.8.3',
        'markdown==3.3.7',
        'typing-extensions==4.1.1',
        'zipp==3.6.0',
        'webencodings==0.5.1',
        'zopfli==0.1.9',
        'CairoSVG==2.5.2',
        'Pillow==8.0.0',
        'Pyphen==0.11.0',
        'cffi==1.15.0',
        'cssselect2==0.4.1',
        'defusedxml==0.7.1',
        'html5lib==1.1',
        'pycparser==2.21',
        'setuptools==59.6.0',
        'six==1.16.0',
        'tinycss2==1.1.1',
        'weasyprint==52.5',
        'webencodings==0.5.1',
    ],
    package_data={'': extra_files},
    scripts=['bin/ecldoc'],
    url="https://github.com/lilyclemson/ECLDocGenerator",
)

