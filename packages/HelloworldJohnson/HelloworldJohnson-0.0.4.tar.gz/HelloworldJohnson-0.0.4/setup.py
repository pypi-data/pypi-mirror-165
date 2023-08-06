from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='HelloworldJohnson',
  version='0.0.4',
  description='A hello world with a few functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  py_modules=["hello","test"],  
  author='Najeb Johnson',
  author_email='Najebjohnson@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Helloworld', 
  packages=find_packages(),
  install_requires=[''] 
)