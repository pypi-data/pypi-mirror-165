from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
]

setup(
    name='CMLPy',
    version='0.0.1',
    description='CMLPy is a Python package for speeding up pandas usage.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    url='',
    author='Sam Varley',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords='pandas',
    packages=find_packages(),
    install_requires=['pandas'],
)