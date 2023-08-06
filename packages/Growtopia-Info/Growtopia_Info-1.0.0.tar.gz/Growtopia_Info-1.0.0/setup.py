from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Growtopia_Info',
  version='1.0.0',
  description='This code can search any info in Growtopia, including server status, sprite, description, and more!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/Gabrielbjb/growtopia-item-finder',  
  author='Gabrielbjb',
  author_email='',
  license='MIT',
  classifiers=classifiers,
  keywords='Growtopia', 
  packages=find_packages(),
  install_requires=[''] 
)