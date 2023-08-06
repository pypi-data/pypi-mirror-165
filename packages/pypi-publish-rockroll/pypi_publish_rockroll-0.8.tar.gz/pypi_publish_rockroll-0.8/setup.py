from setuptools import setup, find_packages


setup(
    name='pypi_publish_rockroll',
    version='0.8',
    license='MIT',
    author="Author Name",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/beverly0005/pypi_publish',
    keywords='example pypi project',
    install_requires=[
        'pandas', #'operator', 'itertools', 're', 
        'nltk', 'spacy==3.0.0', 'en_core_web_sm==3.0.0',
        'flair', 'stanza'
    ],

)
