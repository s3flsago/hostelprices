import sys 
import os

<<<<<<< HEAD
pwd = os.getcwd()

module_path = os.path.join(pwd, 'src')
print(module_path)
sys.path.insert(0, module_path)
=======
# pwd = os.getcwd()

# module_path = os.path.join(pwd, 'src')
# print(module_path)
# sys.path.insert(0, module_path)
>>>>>>> 7a6a857929766f56301196042efbc499144b85ff

import os
import setuptools 

HERE = os.path.abspath(os.path.dirname(__file__))

<<<<<<< HEAD
# with open(os.path.join(HERE, 'README.md')) as f:
#     long_description = f.read()
=======
with open(os.path.join(HERE, 'README.md')) as f:
    long_description = f.read()
>>>>>>> 7a6a857929766f56301196042efbc499144b85ff

requirements = list()
with open(os.path.join(HERE, 'requirements.txt')) as f:
    for line in f:
        line = line.strip()
        if not line.startswith('#'):
            requirements.append(line)


setuptools.setup(
    name='hostelprices',
    version=0.1,
    author="Florian Sagolla",
<<<<<<< HEAD
    author_email="florian.sagolla@gmx.de.de",
    #description=long_description,
    #long_description=long_description,
    package_dir={'': 'src'},
    packages=['hostelprices'],
    python_requires='>=3.6',
    install_requires=requirements,
=======
    author_email="florian.sagolla@gmx.de",
    description=long_description,
    long_description=long_description,
    package_dir={'': 'src'},
    packages=['hostelprices'],
    python_requires='>=3.6',
    #install_requires=requirements,
>>>>>>> 7a6a857929766f56301196042efbc499144b85ff
    #tests_require=requirements
)