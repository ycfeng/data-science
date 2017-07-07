from setuptools import setup

setup(
    name='pysql'
    , version='1.0'
    , description='Python-SQL interface for data science.'
    , url='https://github.com/ycfeng/ds-tools'
    , author='Yuchen Feng'
    , author_email='ycfeng@alum.mit.edu'
    , license='None'
    , packages=['pysql']
    , install_requires=['pandas', 'psycopg2', 'sqlalchemy', 'sqlalchemy-redshift']
    , zip_safe=False
)
