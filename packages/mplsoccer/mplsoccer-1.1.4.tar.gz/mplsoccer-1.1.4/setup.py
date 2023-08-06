from setuptools import setup

exec(open('mplsoccer/_version.py').read())

with open('README.md') as readme_file:
    README = readme_file.read()

INSTALL_REQUIRES = ['matplotlib',
                    'seaborn',
                    'scipy',
                    'pandas',
                    'pillow',
                    'numpy',
                    'beautifulsoup4',
                    ]

# Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
			   'Framework :: Matplotlib',
               'Programming Language :: Python :: 3 :: Only',
               'Topic :: Scientific/Engineering :: Visualization']

setup(name='mplsoccer',
      version=__version__,
      description='A Python package for data visualization for football/ soccer analytics.',
      long_description_content_type="text/markdown",
      long_description=README,
      classifiers=CLASSIFIERS,
      url='https://github.com/andrewRowlinson/mplsoccer',
      author='Anmol Durgapal, Andrew Rowlinson',
      author_email='slothfulwave10@gmail.com, rowlinsonandy@gmail.com',
      author_twitter='@slothfulwave612, @numberstorm',
      license='MIT',
      packages=['mplsoccer'],
      python_requires='>=3.6',
      install_requires=INSTALL_REQUIRES,
      zip_safe=False)
