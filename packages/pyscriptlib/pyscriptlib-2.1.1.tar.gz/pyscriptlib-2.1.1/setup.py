from setuptools import setup, find_packages
from pathlib import Path

setup(
	name= "pyscriptlib",
	version= "2.1.1",
	author= "Rick Arnold",
	author_email= "ntwrick@gmail.com",
	description= "Python Bash Script Helpers",
	long_description= Path('README.md').read_text(),
	long_description_content_type= "text/markdown",
	url= "https://gitlab.com/ntwrick/pyscriptlib",
	classifiers= [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
    keywords=[
        'scripting', 'shell', 'bash', 'helpers', 
		'subprocess', 'sys', 'os',
    ],
	python_requires= '>=3.6',
	packages= find_packages(),
)
