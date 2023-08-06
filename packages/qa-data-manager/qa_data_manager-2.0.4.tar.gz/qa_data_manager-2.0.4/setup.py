import setuptools

version = '2.0.4'

long_description = 'Библиотека для генерации данны в базе данных для автотестов'

setuptools.setup(
    name='qa_data_manager',
    version=version,
    author='e.kurdyumov',
    author_email='e.kurdyumov@ibolit.pro',
    description=(
        u'QA-DATA-MANAGER '
        u'Генерация тестовых данных'
    ),
    long_description=long_description,
    url='https://bitbucket.org/ibolitpro/qa-data-manager',
    packages=['qa_data_manager'],
    install_requires=['faker', 'peewee', 'pymysql', 'pyjwt']
)
