from setuptools import setup

'''A setuptools based setup module, per pypa/sampleproject
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='vial_detector',
      version='0.2',
      description='Background adjusted particle detection of fruitfly motion in glass vials',
      long_description=long_description,
      url='http://github.com/ctzhu/vial_detector',
      author='Chen-Tseh Zhu',
      author_email='lei.ctzhu@gmail.com',
      license='MIT',

      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
      # How mature is this project? Common values are
      # 3 - Alpha
      # 4 - Beta
      # 5 - Production/Stable
      'Development Status :: 3 - Alpha',
      # Indicate who your project is intended for
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      # Pick your license as you wish (should match "license" above)
      'License :: OSI Approved :: MIT License',
      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      #'Programming Language :: Python :: 3',
      #'Programming Language :: Python :: 3.2',
      #'Programming Language :: Python :: 3.3',
      #'Programming Language :: Python :: 3.4',
      ],

      keywords='image processing particle detection',

      packages=['vial_detector'],
      install_requires=['matplotlib', 'numpy', 'scipy', 'pandas', 'trackpy==0.2.4'],
      zip_safe=False)
