import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="oglio",
    version="0.5",
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='External Pyut Persistence',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/xmlio",
    packages=[
        'oglio',
    ],
    package_data={
        'oglio':          ['py.typed'],
        'oglio.toXmlV10': ['py.typed']
    },
    install_requires=[
        'pyutmodel==1.1.0',
        'ogl==0.60.1',
        'untanglepyut==0.4.5',
    ],
)
