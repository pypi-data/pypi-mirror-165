from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='winky',
    version='1.15.3',
    packages=['winky'],
    url='https://bitbucket.org/alborov/winky',
    license='MIT',
    author='Zaur Alborov',
    author_email='alborov.z@gmail.com',
    description='API Test Framework',
    install_requires=['requests==2.28.1', 'lxml==4.8.0', 'pytest==7.1.2',
                      'allure-pytest==2.9.45', 'psycopg2-binary==2.9.2',
                      'cx-Oracle==8.3.0', 'mysql-connector-python==8.0.28'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
