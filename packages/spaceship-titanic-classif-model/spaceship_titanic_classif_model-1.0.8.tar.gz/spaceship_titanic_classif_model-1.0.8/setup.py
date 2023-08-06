from pathlib import Path
from setuptools import find_packages, setup

NAME = 'spaceship_titanic_classif_model'
DESCRIPTION = 'This is an toy project to learn the basics of MLOps and software design in the machine learning context'
URL = 'https://github.com/kojr1234/mlops_exercise.git'
EMAIL = 'fujii.kimio.k@gmail.com'
AUTHOR= 'FabioFujii'
REQUIRES_PYTHON = '==3.9.12'

long_description = DESCRIPTION

# load the package's version fila as a dictionary
about = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'classifier_model'
with open(PACKAGE_DIR / 'VERSION', 'r') as f:
    about['__version__'] = f.read().strip()

# What packages are required for this module to be executed
def list_reqs(fname='requirements.txt'):
    with open(REQUIREMENTS_DIR / fname) as f:
        return f.read().splitlines()

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude='tests'),
    package_data={'classifier_model':[
        'VERSION',
        'config.yml',
        'dataset/train.csv',
        'dataset/test.csv',
        f'models/*{about["__version__"]}.pkl'
    ]},
    install_requires=list_reqs(),
    extras_require={},
    include_packages_data=True,
    license='BSD-3',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)


