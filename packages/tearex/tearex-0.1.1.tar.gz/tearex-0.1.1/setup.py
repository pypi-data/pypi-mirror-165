from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='tearex',
    version='0.1.1',
    author='ppierzc',
    author_email='paul@teacode.io',
    description='A Python SDK for the TeaRex API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tearex-ai/tearex-py',
    packages=find_packages(),
    install_requires=[
        'gql'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)