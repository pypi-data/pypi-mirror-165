from setuptools import setup

setup(
  name = 'mission_naming',
  packages = ['mission_naming'],
  version = '1.1.0',
  description = 'A library to generate random mission names',
  author = 'Raphael Stefanini',
  author_email = 'raphael@rphlo.com',
  url = 'https://github.com/rphlo/mission_naming',
  download_url = 'https://github.com/rphlo/mission_naming/tarball/1.1.0',
  keywords = ['random', 'naming', 'name', 'mission'],
  classifiers = [
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
  ],
  entry_points = {
    'console_scripts': ['mission_name=mission_naming.command_line:main'],
  }
)