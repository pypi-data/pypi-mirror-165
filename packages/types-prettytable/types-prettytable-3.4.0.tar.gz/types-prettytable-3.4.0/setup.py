from setuptools import setup

name = "types-prettytable"
description = "Typing stubs for prettytable"
long_description = '''
## Typing stubs for prettytable

This is a PEP 561 type stub package for the `prettytable` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `prettytable`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/prettytable. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `9e696275018ef3798bb596821ad0d8b4b8e80ab6`.
'''.lstrip()

setup(name=name,
      version="3.4.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/prettytable.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['prettytable-stubs'],
      package_data={'prettytable-stubs': ['__init__.pyi', 'colortable.pyi', 'prettytable.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
