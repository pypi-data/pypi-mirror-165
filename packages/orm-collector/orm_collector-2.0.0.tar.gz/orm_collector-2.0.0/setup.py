from pathlib import Path
from setuptools import setup
import subprocess


path = Path(__file__).resolve().parent
readme = path/'README.md'
version = path / "VERSION"

if readme.exists():
    long_description = readme.read_text()

if version.exists():
    version = version.read_text().strip()

#install_gdal()

setup(name='orm_collector',
      version=version,
      description='ORM Collector Schemma',
      url='http://gitlab.csn.uchile.cl/dpineda/orm_collector',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      packages=['orm_collector'],
      keywords="collector gnss orm",
      install_requires=["networktools",
                        "basic_logtools",
                        "validators",
                        "shapely",
                        "psycopg2-binary",
                        "sqlalchemy>=1.3.17",
                        "geoalchemy2",
                        "ujson",
			"fastapi",
			"fastapi-cache2",
                        "django",
                        "click", 
			"aioredis",
			"rich", 
                        "aioredis==^2.0.1"],
      entry_points={
        'console_scripts': [
            "orm_create_db = orm_collector.scripts.create_db:run_crear_schema",
            "orm_load_data = orm_collector.scripts.load_data:load_data_orm",
            "orm_vars = orm_collector.scripts.create_db:show_envvars",
            "orm_show_data = orm_collector.scripts.show_data:show_data"
        ]
        },
      include_package_data=True,
      license='GPLv3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False
      )
