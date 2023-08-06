from setuptools import setup,find_packages
import os 

setup(
    name='desktop-banner',
    version='0.0.1',
    description="Display the classification of the system on the desktop",
    packages=find_packages(),
    classifiers = [
    	"Programming Language :: Python :: 3",
    	"License :: OSI Approved :: MIT License",
    	"Operating System :: POSIX :: Linux",
    ],
   python_requires=">=3.0",
   scripts=["bin/banner"],
   license_files = ('LICENSE'),
   install_requires=[
       "tk",
       "tcl",
       "configparser",
       "screeninfo",
    ],
)

# Ensure the banner script is world readable and executable
script_path = '/usr/local/bin/banner'
if os.path.exists(script_path):
    os.chmod(script_path, int('755', 8))
