from os.path import dirname, join
from setuptools import setup


with open(join(dirname(__file__), 'cococrawler/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()


setup(
    name='cococrawler',
    version=version,
    url='https://github.com/yjxkwp/cococrawler',
    description='A distributed network crawler framework',
    long_description=open('README.rst').read(),
    author='kwp',
    author_email='yjxkwp@foxmail.com',
    maintainer='kwp',
    maintainer_email='yjxkwp@foxmail.com',
    license="MIT",
    keywords=['distributed','crawler','spider'],
    packages= ['cococrawler','cococrawler.command','cococrawler.config','cococrawler.exceptions','cococrawler.templates'],
    install_requires=[
        "requests",
        'Jinja2',
        'pymongo',
        'redis'
    ],
    entry_points={
        'console_scripts': ['coco = cococrawler.command:execute']
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)