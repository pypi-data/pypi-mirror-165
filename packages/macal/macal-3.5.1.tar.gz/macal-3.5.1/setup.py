from setuptools import setup, find_packages

import shutil
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

cachepath = "macal/external/__pycache__"

if os.path.exists(cachepath):
	shutil.rmtree(cachepath)

setup(
	name = 'macal',
	version = '3.5.1',
	author= 'Marco Caspers',
	author_email="marco.caspers@westcon.com",
	packages=find_packages(include=['macal','external','tests', 'libraries', 'sublime']),
	description = "Specialized scripting language",
	long_description = read("README.md"),
	long_description_content_type = "text/markdown",
	url = "https://github.com/Sama-Developer/macal",
	license='MIT',
	classifiers = [
    	"Programming Language :: Python :: 3",
    	"License :: OSI Approved :: MIT License",
    	"Operating System :: OS Independent"],
	requires = ["unidecode", "Depricated"],
	#package_data={'macal': ['sublime/*']}
	#'libraries/*.mcl', 'external/*.py', '../tests/*',
)