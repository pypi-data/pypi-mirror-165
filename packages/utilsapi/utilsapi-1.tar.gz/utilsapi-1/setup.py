"""from flask import Flask, request, render_template, url_for
from flask_cors import CORS

main = Flask(__name__)
CORS(main)

@main.route('/')
def home():
    return 'Miammmm'

@main.route('/test')
def test():
    return 'test'

if __name__=='__main__':
    
    main.debug = True
    main.run('0.0.0.0',9999)
"""

from setuptools import setup, find_packages

ver = '1'
desc = 'Test Pack'
descL = 'Test Packages'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="utilsapi", 
        version=ver,
        author="Capo Loup",
        author_email="<loupcapo4@gmail.com>",
        description=desc,
        long_description=descL,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)