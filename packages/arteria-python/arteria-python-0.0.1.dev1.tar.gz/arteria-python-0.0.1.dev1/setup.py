from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'arteria/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='arteria-python',
    version=version.__version__,
    author='Arteria',
    author_email='dev@arteria.io',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/arteria-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(cuenca=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'cuenca>=0.14.1"',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
