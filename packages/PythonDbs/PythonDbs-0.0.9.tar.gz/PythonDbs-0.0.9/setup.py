
from setuptools import setup, find_packages

VERSION = '0.0.9' 
DESCRIPTION = 'sqlite3 extension'
LONG_DESCRIPTION = 'allows sqlite3 to be used in a diffrent way'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="PythonDbs", 
        version=VERSION,
        author="Jordan",
        author_email="<jordybhunter10@outlook.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'irst package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Other Audience",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)