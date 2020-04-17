import setuptools
from distutils.core import setup
import pathlib

setup(name='cutlet', 
      version='0.1.0',
      author="Paul O'Leary McCann",
      author_email="polm@dampfkraft.com",
      description="Romaji converter",
      long_description=pathlib.Path('README.md').read_text('utf8'),
      long_description_content_type="text/markdown",
      url="https://github.com/polm/cutlet",
      packages=setuptools.find_packages(),
      install_requires=['jaconv', 'fugashi'],
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Natural Language :: Japanese",
          ],
      python_requires='>=3.5',
      )
