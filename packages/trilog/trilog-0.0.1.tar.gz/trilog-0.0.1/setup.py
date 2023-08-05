from setuptools import setup , find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name = 'trilog',
  version = '0.0.1',
  description = 'Trigonometric and Logarithmic calculators.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url = '',
  author = 'Mudit Bhatnagar',
  author_mail = 'mudit1bhatnagar@gmail.com',
  licenses = 'MIT',
  classifiers=classifiers,
  keywords='calculator',
  packages = find_packages(),
  install_requirements = ['math module']
)
