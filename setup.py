import setuptools
from distutils.core import setup
import pathlib

# This is necessary to get the version right, otherwise
# it will fail and give v0.0.0
import setuptools_scm

setup(name='cutlet', 
      use_scm_version=True,
      author="Paul O'Leary McCann",
      author_email="polm@dampfkraft.com",
      description="Romaji converter",
      long_description=pathlib.Path('README.md').read_text('utf8'),
      long_description_content_type="text/markdown",
      url="https://github.com/polm/cutlet",
      packages=setuptools.find_packages(),
      install_requires=['jaconv', 'fugashi', 'mojimoji'],
      setup_requries=['setuptools-scm'],
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Natural Language :: Japanese",
          ],
      python_requires='>=3.5',
      scripts=['bin/cutlet'],
      package_data={'cutlet':['exceptions.tsv']},
      )
