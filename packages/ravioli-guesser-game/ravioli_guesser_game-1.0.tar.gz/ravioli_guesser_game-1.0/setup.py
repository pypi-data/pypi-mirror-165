from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ravioli_guesser_game',
  version='1.00',
  description='A cool game to play with!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ravioli',
  author_email='aaravrajup@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='game', 
  packages=find_packages(),
  install_requires=[''] 
)