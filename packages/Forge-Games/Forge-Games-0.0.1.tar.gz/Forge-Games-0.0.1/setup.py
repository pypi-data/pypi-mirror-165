from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Forge-Games',
  version='0.0.1',
  description='A aid for developing text based games.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Blake Leslie',
  author_email='blakeleslie4607@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='engine', 
  packages=find_packages(),
  install_requires=['time', 'sys', 'os'] 
)