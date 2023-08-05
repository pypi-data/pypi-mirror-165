from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='modelTissueFlow',
    version='1.2',    
    description='tissue-flow-analysis',
    author='Bandan Chakrabortty',
    author_email='bandan13@gmail.com',
    packages=['modelTissueFlow','modelTissueFlow/modules'],
    url='https://github.com/HiBandan/modelTissueFlow', 
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe = False,
    )


