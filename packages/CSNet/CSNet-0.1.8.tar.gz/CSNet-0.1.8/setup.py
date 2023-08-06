from setuptools import setup
from setuptools import find_packages

# python setup.py build
# python setup.py install
# python setup.py sdist
# python setup.py bdist_wheel
# pip install <path-to-package>
# python setup.py sdist upload

VERSION = '0.1.8'

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "Framework :: Jupyter",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux", "Programming Language :: Python",
    "Programming Language :: Python :: 3.9",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

python_requires = ">=3.9"

install_requires = [
    "scanpy>=1.8.2",
    "scikit-learn>=1.0.2",
    "scvi-tools>=0.15.2",
    "numpy>=1.20.3",
    "pandas>=1.3.4",
    "torch>=1.9.0",
    "pytorch-lightning>=1.5.7",
    "scipy>=1.7.1",
    "pyyaml>=0.2.5",
    "wandb>=0.12.9",
    "scikit-misc>=0.1.4",
    "tqdm>=4.62.3",
    "seaborn>=0.11.2",
]

project_urls = {
    "Documentation": "https://github.com/ouc16020021031",
    "Code": "https://github.com/ouc16020021031",
    "Issue tracker": "https://github.com/ouc16020021031",
}

package_data = {"": ["*.yaml"]}

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()


setup(
    author='shenzhuoqiao',
    author_email='ouc16020021031@gmail.com',
    name='CSNet',
    version=VERSION,
    python_requires=python_requires,
    install_requires=install_requires,
    classifiers=classifiers,
    project_urls=project_urls,
    description='short description',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data=package_data,
    zip_safe=False,
)
