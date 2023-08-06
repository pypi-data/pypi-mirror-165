from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pypopup',
  version='0.0.1',
  description='A NONDOS Project',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='NONDOS',
  author_email='pypopup@gmx.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='tkinter', 
  packages=find_packages(),
  install_requires=[''] 
)