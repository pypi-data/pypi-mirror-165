from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='slowtype',
      version='0.1',
      description='SlowType - Small python library for type-effect',
      packages=['slowtype'],
      author_email='isgamekillerept@gmail.com',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')