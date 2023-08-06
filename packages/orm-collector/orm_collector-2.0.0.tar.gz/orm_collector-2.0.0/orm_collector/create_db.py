from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy import event
from sqlalchemy.sql import exists, select

from networktools.environment import get_env_variable
from orm_collector import Base
import os

"""
Create Schema Collector
"""

def create_collector(engine):
    try:
        engine.execute(CreateSchema('collector'))
    except Exception as e:
        raise e

"""
Create Schema DataWork
"""
def create_datawork(engine):
    try:
        engine.execute(CreateSchema('datawork'))
    except:
        raise

if __name__=='__main__':
    user=os.environ.get('COLLECTOR_DBUSER')
    passw=os.environ.get('COLLECTOR_DBPASS')
    dbname=os.environ.get('COLLECTOR_DBNAME')
    hostname=os.environ.get('COLLECTOR_DBHOST')
    db_engine='postgresql://%s:%s@%s/%s' %(user,passw,hostname,dbname)
    #create engine
    engine = create_engine(db_engine, echo=True)
    print(db_engine)
    #load schema on engine
    try:
        create_collector(engine)
        Base.metadata.create_all(engine, checkfirst=True)
    except Exception as e:
        print("Falla al crear esquema de tablas")
        raise e
