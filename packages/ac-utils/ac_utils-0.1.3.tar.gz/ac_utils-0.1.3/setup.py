from distutils.core import setup
setup(
  name = 'ac_utils',
  packages = ['ac_utils'],
  version = '0.1.3',
  license='GNU General Public License v3.0',
  description = 'Functions for working with robotics.',
  author = 'Alberto Cruz',
  author_email = 'alberto.cruz@upm.es',
  url = 'https://github.com/AlbertoCruzRuiz/ac_utils',
  download_url = 'https://github.com/AlbertoCruzRuiz/ac_utils/archive/refs/tags/v0.1.tar.gz',
  keywords = ['Robotics'],
  install_requires=[
          'numpy',
          'scipy',
          'cupy',
          'sensor-msgs',
          'std_msgs',
          'builtin_interfaces'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.10',
  ],
)
