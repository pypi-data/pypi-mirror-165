from setuptools import setup
#from distutils.core import setup

def readme():  
  with open('README.md', 'r') as f:
    return  f.read()

setup(
  name = 'shadog',       
  packages = ['shadog'],  
  version = '1.0.23', 
  license='MIT', 
  description = 'Shadog',  
  long_description = readme(),  
  long_description_content_type = 'text/markdown',
  author = 'Tiago Alexandre Soares Aragão', 
  author_email = 'tiago.alexandre.aragao@gmail.com', 
  url = 'https://gitlab.com/tiago.alexandre.aragao',  
  download_url = 'https://gitlab.com/tiago.alexandre.aragao',
  keywords = ['crypto', 'sha512'],  
  #install_requires = [],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3', 
  ],
)