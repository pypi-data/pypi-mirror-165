from setuptools import setup


setup(
    name='rubiks_snake',
    version='0.1.3',
    license='MIT',
    author='Denis Khamitov',
    author_email='hamitov.97@mail.ru',
    py_modules=['rubiks_snake'],
    url='https://github.com/denis240997/rubiks-snake',
    keywords=['rubiks snake', 'puzzle'],
    install_requires=[
        'numpy>=1.18',
        'plotly>=5.0',
    ],
)
