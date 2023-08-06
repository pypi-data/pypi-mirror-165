from setuptools import setup

setup(
    name="aresTools",
    version="0.1.5",
    packages=['aresTools'],
    description='A Python package that transforms a pandas DataFrame based on mathematical operations',
    url='https://github.com/aresmaterials/arestools',
    author='Erik Gutierrez-Valladares',
    author_email='erik@aresmaterials.com',
    license='Apache License 2.0',
    install_requires= [ "pandas",
                        "rdkit-pypi",
                        "mordred",
                        "scikit-learn",
                      ],
)
    #packages=['pyexample'],
    #scripts=["pandas_featurizer_json.py"],

