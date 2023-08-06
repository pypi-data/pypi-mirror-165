from setuptools import setup, find_packages

setup(
    name = 'ACETH',
    version = '0.0.1',
    author = 'Karim Galal, Walid Chatt',
    author_email = 'karim.galal@analytics-club.org, walid.chatt@analytics-club.org',
    license = 'MIT',
    description = 'Analytics Club ETHZ helper package',
    packages = ['ACETH'],
    url = 'https://github.com/kimo26/ACE',
    keywords = ['ETHZ','ethz','eth','AI','artificial intelligence',
                'machine learning', 'data processing','chatbot',
                'education','ML'],
    install_requires = [
        'numpy','pandas','torch',
        'tensorflow','transformers','sklearn',
        'emoji',
        ],
    classifiers=[
        'Programming Language :: Python :: 3'
        ]
    )
