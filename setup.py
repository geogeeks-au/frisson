import setuptools
from frisson.version import Version


setuptools.setup(name='frisson',
        version=Version('0.0.1').number,
        description='Frisson Georeferencing Toolkit',
        long_description=open('README.md').read().strip(),
        author='Tom Lynch',
        author_email='',
        url='http://github.com/attentive/frisson',
        py_modules=['frisson'],
        install_requires=[
            'GDAL',
            ],
        license='MIT License',
        zip_safe=False,
        keywords='georeferencing spatial imagery package',
        classifiers=['Packages', 'Spatial'])
