
"""Package up the bloom filter code for consumption through pypi."""

from setuptools import setup
setup(
    name="drs-bloom-filter",
    version="2.4",
    py_modules=['bloom_filter_mod', ],
    # metadata for upload to PyPI
    author="Daniel Richard Stromberg",
    author_email="strombrg@gmail.com",
    description='Pure Python Bloom Filter module',
    long_description='''
A pure python bloom filter (low storage requirement, probabilistic
set datastructure) is provided.

Includes mmap, in-memory and disk-seek backends.

The user specifies the desired maximum number of elements and the
desired maximum false positive probability, and the module
calculates the rest.

Example use:
    >>> bf = bloom_filter_mod.Bloom_filter(ideal_num_elements_n=100, error_rate_p=0.01)
    >>> for i in range(0, 200, 2):
    ...     bf.add(i)
    ...
    >>> for i in range(0, 200, 3):
    ...     print(i in bf)
    ...
''',
    license="MIT",
    keywords="probabilistic set datastructure",
    url='http://stromberg.dnsalias.org/~strombrg/drs-bloom-filter/',
    platforms='Cross platform',
    classifiers=[
         "Development Status :: 5 - Production/Stable",
         "Intended Audience :: Developers",
         "Programming Language :: Python :: 3",
         ],
)
