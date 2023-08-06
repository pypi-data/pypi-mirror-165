from setuptools import setup, find_packages

setup(
    name = 'ACETH',
    version = '0.0.6',
    author = 'Karim Galal, Walid Chatt',
    author_email = 'karim.galal@analytics-club.org, walid.chatt@analytics-club.org',
    license = 'MIT',
    description = 'Analytics Club ETHZ helper package',
    packages=find_packages(),
    package_data={'ACETH': ['data/emoji_model.h5','data/encoder_emoji.pkl','data/token_emoji.pkl']},
    include_package_data=True,
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
