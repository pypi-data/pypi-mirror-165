from setuptools import setup

setup(
    name='nlp-for-mlf',
    version='0.0.6',
    author='MLF Team',
    description='A brief synopsis of the project',
    long_description='A much longer explanation of the project and helpful resources',
    url='https://github.com/BenjaminFranline',
    keywords='nlp',
    python_requires='>=3.9, <4',
    # packages=['nlp-for-mlf'],
    install_requires=[
        'torch',
        'transformers',
        'numpy>=1.14.5',
        'matplotlib>=2.2.0',
    ]
    #,
    # package_data={
    #     'sample': ['sample_data.csv'],
    # },
    # entry_points={
    #     'runners': [
    #         'sample=sample:main',
    #     ]
    # }
)