from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mechpress',
  version='0.0.2',
  description='package for mechanical press design',
  long_description=open('LONGDESCRIPTION.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sanchit',
  author_email='sanchitsharma84@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='mechanical press', 
  packages=find_packages(),
  install_requires=[''] 
)