"""
OCR Toolkit
-----

The OCR Toolkit helps parse data and location information from
ABBYY XML output.

"""

from setuptools import find_packages, setup


setup(
        name='ocrtoolkit',
        version='0.1a',
        url='http://github.com/opensecrets/',
        license='MIT',
        author='Alex Byrnes',
        author_email='abyrnes@crp.org',
        description='Tools for parsing data from PDF OCR output.',
        long_description=__doc__,
        packages=find_packages(exclude=['tests*']),
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=['lxml>=2.3.2'],
        classifiers=[
                    'Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Programming Language :: Python',
                    'Topic :: Text Processing :: Markup :: XML',
                    'Topic :: Software Development :: Libraries :: Python Modules'
                ],
)

