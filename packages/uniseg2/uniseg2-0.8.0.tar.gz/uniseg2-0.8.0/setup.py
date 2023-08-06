from setuptools import setup

with open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

setup(
    name = 'uniseg2',
    version = '0.8.0',
    author = 'Max Bachmann',
    author_email = 'pypi@maxbachmann.de',
    url = 'https://github.com/maxbachmann/uniseg',
    description = 'Determine Unicode text segmentations',
    long_description = readme,
    long_description_content_type="text/markdown",
    license = 'MIT',
    packages = ['uniseg2'],
    package_data = {
        'uniseg': ['docs/*.html', 'samples/*.py']
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Text Processing',
    ],
    zip_safe = False,
    python_requires= ">=3.6",
)
