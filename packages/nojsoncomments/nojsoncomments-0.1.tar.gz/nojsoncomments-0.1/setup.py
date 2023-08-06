from setuptools import setup
from Cython.Build import cythonize


setup(
    name='nojsoncomments',
    version='0.1',
    description='Library to remove js-style comments from JSON strings',
    author='linjackson',
    author_email='linjackson78@gmail.com',
    maintainer='petri',
    maintainer_email='petri@koodaamo.fi',
    url='https://github.com/koodaamo/nojsoncomments',
    keywords=['json', 'comment', 'javascript', 'parse'],
    classifiers=['Development Status :: 3 - Alpha', 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.5'],
    license='MIT',
    test_suite="tests",
    ext_modules = cythonize("nojsoncomments.pyx", language_level=3)
)
