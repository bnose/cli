from setuptools import setup

setup(
    name='Bottlenose CLI',
    version='1.0',
    py_modules=['bnose'],
    install_requires=[
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        bnose=bnose:cli
    '''
)

