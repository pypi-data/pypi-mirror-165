from setuptools import setup
from Cython.Build import cythonize
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nojsoncomments',
    version='0.2',
    description='Library to remove js-style comments from JSON strings',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
