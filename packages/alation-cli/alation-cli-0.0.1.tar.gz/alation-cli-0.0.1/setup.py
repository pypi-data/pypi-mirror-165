from setuptools import setup, find_namespace_packages

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

# reading long description from file
with open('..\README.rst', 'r', encoding='utf-8') as f:
    README = f.read()


# some more details
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
]

# calling the setup function
setup(name='alation-cli',
      version='0.0.1',
      description='Alation Command-Line Tools',
      long_description=README,
      url='https://github.com/jojitech/alation-cli',
      author='Shawn McGough',
      author_email='smcgough@jojitech.com',
      packages=find_namespace_packages(),
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='alation api cli',
      entry_points={
          'console_scripts': ['al=alation.cli.main:main']
      },
      project_urls={
          'Documentation': 'https://github.com/jojitech/alation-cli',
          'Funding': 'https://github.com/sponsors/ShawnMcGough',
          'Source': 'https://github.com/jojitech/alation-cli',
          'Tracker': 'https://github.com/jojitech/alation-cli/issues',
      }
      )
