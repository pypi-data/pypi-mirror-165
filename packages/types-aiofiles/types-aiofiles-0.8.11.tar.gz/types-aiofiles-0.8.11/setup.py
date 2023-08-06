from setuptools import setup

name = "types-aiofiles"
description = "Typing stubs for aiofiles"
long_description = '''
## Typing stubs for aiofiles

This is a PEP 561 type stub package for the `aiofiles` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `aiofiles`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/aiofiles. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `2c7ac0990f3747ea4b88f157b752eebd656559f5`.
'''.lstrip()

setup(name=name,
      version="0.8.11",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/aiofiles.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['aiofiles-stubs'],
      package_data={'aiofiles-stubs': ['__init__.pyi', 'base.pyi', 'os.pyi', 'ospath.pyi', 'tempfile/__init__.pyi', 'tempfile/temptypes.pyi', 'threadpool/__init__.pyi', 'threadpool/binary.pyi', 'threadpool/text.pyi', 'threadpool/utils.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
