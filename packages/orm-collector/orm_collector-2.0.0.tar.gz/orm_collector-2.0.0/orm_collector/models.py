import json
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint, Index
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy import Boolean
from sqlalchemy.types import NUMERIC

# GEO
from geoalchemy2 import Geography
from geoalchemy2 import functions as geo_func

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from geoalchemy2.shape import to_shape

#from osgeo import ogr

from networktools.ip import validURL
from base64 import b64decode

Base = declarative_base()


class Protocol(Base):
    """
    Define protocols for data communication
    """

    __tablename__ = 'protocol'
    __table_args__ = {'schema': 'collector'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(15), unique=True)
    ref_url = Column(String(300), unique=True, nullable=True)
    class_name = Column(String(20), unique=False, nullable=True)
    git_url = Column(String(300), unique=False, nullable=True)

    stations_prot = relationship('Station', backref='protocol')

    @validates('ref_url', 'git_url')
    def validate_url(self, key, value):
        return value if validURL(value) else "localhost"

    def __repr__(self):
        return f"Procotol({self.id} {self.name})"

    def __str__(self):
        return f"Procotol({self.id} {self.name})"

class DBType(Base):
    """
    Define database information for store data
    """

    __tablename__ = 'dbtype'
    __table_args__ = {'schema': 'collector'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    typedb = Column(String(12), unique=False)
    # name software
    name = Column(String(12), unique=True, nullable=True)
    url = Column(String(300), unique=True, nullable=True)
    data_list = Column(String(300), unique=False, nullable=True)

    dbservers = relationship('DBServer', back_populates='dbtype')

    @validates('typedb')
    def validate_typedb(self, key, value):
        if value.upper() in ['TEXT', 'SQL', 'NO-SQL', 'ReQL']:
            return value.upper()
        else:
            return 'TEXT'


class DBServer(Base):
    """
    Define server parameters of databases
    """
    __tablename__ = 'dbserver'
    __table_args__ = {'schema': 'collector'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(200), unique=True, nullable=True)
    host = Column(String(25), unique=False, nullable=True)
    port = Column(Integer, unique=False, nullable=True)
    user = Column(String(25), unique=False, nullable=True)
    passw = Column(String(200), unique=False, nullable=True)
    info = Column(String(255), unique=False, nullable=True)
    dbname = Column(String(255), unique=False, nullable=True)
    hostname = Column(String(255), unique=True, nullable=False)
    dbtype_id = Column(Integer, ForeignKey('collector.dbtype.id'))

    dbtype = relationship('DBType', back_populates='dbservers')
    dbdata_set = relationship('DBData', back_populates='dbservers')


    @validates('host')
    def validate_host(self, key, value):
        return value if validURL(value) else "localhost"

    def __str__(self):
        return f"DBServer({self.hostname}:{self.dbname}:{self.host}:{self.port})"

    def __repr__(self):
        return f"DBServer({self.hostname}:{self.dbname}:{self.host}:{self.port})"


class Station(Base):
    """
    Define basic station information
    """

    __tablename__ = 'station'
    __table_args__ = {'schema': 'collector'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8), unique=True)
    name = Column(String(40), unique=False, nullable=True)
    position_x = Column(NUMERIC(precision=15, scale=3),
                        unique=False, default=0)
    position_y = Column(NUMERIC(precision=15, scale=3),
                        unique=False, default=0)
    position_z = Column(NUMERIC(precision=15, scale=3),
                        unique=False, default=0)
    protocol_host = Column(String(80), unique=False)  # validate ip
    port = Column(Integer, unique=False, default=0)
    interface_port = Column(Integer, unique=False, default=0)
    host = Column(String(80), unique=False)  # validate ip
    active = Column(Boolean, default=True, unique=False)

    # db_id = Column(Integer, ForeignKey('collector.dbdata.id'))
    protocol_id = Column(Integer, ForeignKey('collector.protocol.id'))
    server_id = Column(Integer, ForeignKey('collector.server_instance.id'))
    network_id = Column(Integer, ForeignKey('collector.network_group.id'))

    dbdata_set = relationship('DBData', back_populates='stations')
    
    def __repr__(self):
        return f"{self.code} ->  {self.name}"

    @validates('port')
    def validate_port(self, key, port):
        assert port >= 0 and port < 65500, "No es un valor correcto"
        return port

    @validates('interface_port')
    def validate_port(self, key, interface_port):
        print("El puerto de interface se valida")
        print(interface_port)
        if interface_port == None:
            interface_port = 0
        assert interface_port >= 0 and interface_port < 65500, "No es un valor correcto"
        return interface_port

    @validates('host')
    def validate_host(self, key, value):
        return value if validURL(value) else "localhost"

    @validates('protocol_host')
    def validate_protocol_host(self, key, value):
        return value if validURL(value) else "localhost"

    @property
    def interface_url(self):
        if self.interface_port > 0:
            return "http://" + str(self.host) + ":" + str(self.interface_port)
        else:
            return "http://" + str(self.host)

    def get_position(self):
        point = dict(X=self.position_x, Y=self.position_y, Z=self.position_z)
        return point  # list(point.coords)

    @property
    def json(self):
        return {
            "id": self.id, 
            "code": self.code,
            "name": self.name,
            "ECEF_X": float(self.position_x),
            "ECEF_Y": float(self.position_y),
            "ECEF_Z": float(self.position_z),
            "interface_port": self.interface_port,
            "host": self.host,
            "protocol_host": self.protocol_host,
            "port": self.port,
            "active": self.active,
            "protocol_id": self.protocol_id,
            "server_id": self.server_id,
            "network_id": self.network_id
        }


class DBData(Base):
    """
    Define what databases are allowd to some station
    """

    __tablename__ = 'dbdata'
    __table_args__ = (
        UniqueConstraint('station_id','database_id', 'priority', name="unique_origin_destiny"),
        {'schema': 'collector'})

    id = Column(Integer, primary_key=True, autoincrement=True)
    # ascii, sql, no-sql
    # name software
    # code for this database en particular
    station_id = Column(Integer, ForeignKey('collector.station.id'), 
                        nullable=False) 
    database_id = Column(Integer, ForeignKey('collector.dbserver.id'),
                         nullable=False)
    priority = Column(Integer, unique=False, default=0)

    stations = relationship('Station', back_populates='dbdata_set')
    dbservers = relationship('DBServer', back_populates='dbdata_set')

    def __str__(self):
        return f"DBData({self.stations}:{self.dbservers}->{self.priority})"

    def __repr__(self):
        return f"DBData({self.stations}:{self.dbservers}->{self.priority})"


class NetworkGroup(Base):
    __tablename__ = 'network_group'
    __table_args__ = {"schema": "collector"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), unique=False)

    def __str__(self):
        return "%d : %s : %s" % (self.id, self.name, self.description)


class ServerInstance(Base):
    __tablename__ = 'server_instance'
    __table_args__ = {"schema": "collector"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_name = Column(String(100), unique=True, nullable=False)
    host_ip = Column(String(20), unique=False)
    gnsocket_port = Column(Integer, unique=False, default=0)
    activated = Column(Boolean, default=True, unique=False)

    @validates('host_ip')
    def validate_host_ip(self, key, value):
        return value if validURL(value) else "localhost"

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def __str__(self):
        return "%s : %s : %d" % (self.host_name, self.host_ip, self.gnsocket_port)


class DataDestiny(Base):
    """
    Define final destiny for data station 
    """

    __tablename__ = 'datadestiny'
    __table_args__ = {'schema': 'collector'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('collector.station.id'))
    destiny = Column(String(40), unique=False, nullable=True)
    uri = Column(String(40), unique=False, nullable=True)
    port = Column(Integer, unique=False, default=0)
    description = Column(String(300), unique=False, nullable=True)

    @validates('port')
    def validate_port(self, key, port):
        assert port >= 0 and port < 65500, "No es un valor correcto"
        return port

    def get_destiny(self):
        return (self.station_id, "-> %s = %s:%s" % (self.destiny, self.uri, self.port))
