from sqlalchemy import update
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import text
from basic_logtools.filelog import LogFile
from pathlib import Path
from orm_collector.models import (Station,
                                  Protocol,
                                  DBData,
                                  DBServer,
                                  DBType,
                                  DataDestiny,
                                  ServerInstance,
                                  NetworkGroup)

from orm_collector.db_session import CollectorSession, data

import datetime

from geoalchemy2 import functions as geo_func

from sqlalchemy.sql import select
from sqlalchemy.sql import table
from sqlalchemy.sql import column
from sqlalchemy import inspect
from rich import print
import time
from networktools.geo import (radius, deg2rad, ecef2llh, llh2ecef)


def get_llh(data):
    ecef_keys = ["x","y","z"]
    data['ecef_x'] = float(data['ecef_x'])
    data['ecef_y'] = float(data['ecef_y'])
    data['ecef_z'] = float(data['ecef_z'])
    x = data['ecef_x']
    y = data['ecef_y']
    z = data['ecef_z']
    (lon, lat, h) = ecef2llh(x, y, z)
    data["position"] = {
        "ecef"  : {
            "x": data['ecef_x'],
            "y": data['ecef_y'],
            "z": data['ecef_z']
        },

        'llh': {'lat': lat, 'lon': lon, 'z': h}
    }
    for k in ecef_keys:
        key = f"ecef_{k}"
        if key in data:
            del data[key]

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class SessionHandle(CollectorSession):
    """
    A session middleware class to manage the basic elements in the database,
    has generic methods to verify the elements existence, update_ and obtain
    lists from tables
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = self.connection
        self.metadata = MetaData()
        code = kwargs.get('code', 'ORM')
        log_path = kwargs.get('log_path', './')
        print("ORM log path", log_path)
        log_level = kwargs.get('log_level', 'INFO')
        hostname = kwargs.get('hostname', 'localhost')
        self.logger = LogFile(self.class_name,
                              code,
                              hostname,
                              path=log_path,
                              base_level=log_level)
        self.path = Path(__file__).parent

    @property
    def class_name(self):
        return self.__class__.__name__

    def close(self):
        self.logger.close()
        self.session.close()

    def exists_table(self, table_name, **kwargs):
        """
        Check if table_name exists on schema
        :param table_name: a table_name string
        :return: boolean {True,False}
        """
        if bool(kwargs):
            this_schema = kwargs['schema']
        else:
            this_schema = 'collector'

        return self.engine.dialect.has_table(self.engine.connect(), table_name)

    def exists_field(self, table_name, field_name, **kwargs):
        """
        Check if field exist in table
        :param table_name: table name string
        :param field_name: field name string
        :return:  bolean {True, False}
        """
        if bool(kwargs):
            this_schema = kwargs['schema']
        else:
            this_schema = 'collector'

        assert self.exists_table(table_name), 'No existe esta tabla'
        fields = Table(
            table_name,
            self.metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=this_schema)
        r = [c.name for c in fields.columns]
        try:
            r.remove('id')
        except ValueError as e:
            self.logger.exception("Error al checkear campo, %s" % e)
        assert field_name in r, 'No existe este campo en tabla'
        return True

    def value_type(self, table_name, field_name, value, **kwargs):
        """
        Check if value is the same value type in field
        :param table_name: table name string
        :param field_name: field name string
        :param value:  some value
        :return: boolean {True, False, None}; None if value type doesn't exist
        on that list, because there are only the most common types.
        """
        if bool(kwargs):
            this_schema = kwargs['schema']
        else:
            this_schema = 'collector'

        # get type value
        assert self.exists_table(table_name), 'No existe esta tabla'
        fields = Table(
            table_name,
            self.metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=this_schema)
        r = [c.name for c in fields.columns]
        assert self.exists_field(table_name, field_name), \
            'Campo no existe en tabla'
        this_index = r.index(field_name)
        t = [str(c.type) for c in fields.columns]
        this_type = t[this_index]
        b = False
        if this_type == 'INTEGER' or this_type == 'BigInteger':
            assert isinstance(value, int)
            b = True
        elif this_type[0:7] == 'VARCHAR' or this_type == 'TEXT' or this_type == 'STRING':
            assert isinstance(value, str)
            b = True
        elif this_type == 'BOOLEAN':
            assert isinstance(value, bool)
            b = True
        elif this_type == 'DATE':
            assert isinstance(value, datetime.date)
            b = True
        elif this_type == 'DATETIME':
            assert isinstance(value, datetime.datetime)
            b = True
        elif this_type == 'FLOAT' or this_type == 'NUMERIC':
            assert isinstance(value, float)
            b = True
        else:
            b = None

        return b
        # check

        def generic_query(self, st):
            q = text(st)
            u = self.session.execute(q)
            return(u)

    def update_table(self, table_name, instance, field_name, value, **kwargs):
        """
        Change some value in table
        :param table_name: table name class
        :param instance: instance to modify in database
        :param field: field name string
        :param value: value
        :return: void()
        """
        this_schema = kwargs.get('schema', 'collector')
        # update to database
        table = Table(
            table_name,
            self.metadata,
            autoload=True,
            autoload_with=self.engine,
            schema=this_schema
        )
        up = update(table).where(
            table.c.id == instance.id).values({field_name: value})
        self.session.execute(up)
        result = self.session.commit()

    # LIST ELEMENTS

    def get_list(self, model):
        """
        Get the complete list of elements in some Model Class (Table in db)

        :param model:Model Class
        :return: a query list
        """
        return self.session.query(model).all()


# Class Alias
SH = SessionHandle


class SessionCollector(SH):
    """
    An specific SessionHandler who extends database model in Collector case,
    has a Station, a Protocol and a FBData tables
    """

    # STATION TABLE

    def station(self,
                refresh=True,
                **kwargs):
        code = kwargs.get('code')
        name = kwargs.get('name')
        position_x = kwargs.get('ECEF_X')
        position_y = kwargs.get('ECEF_Y')
        position_z = kwargs.get('ECEF_Z')
        protocol_host = kwargs.get('protocol_host')
        host = kwargs.get('host')
        port = int(kwargs.get('port',0))
        interface_port = int(kwargs.get('interface_port',80))
        db = kwargs.get('db')
        protocol = kwargs.get('protocol')
        server = kwargs.get('server_id', "atlas")
        active = kwargs.get('active', False)
        network = kwargs.get("network_id","3g")
        instance = self.session.query(Station).filter_by(code=code).first()

        if instance:
            self.logger.info("Estación %s ya existe" % instance)
            if refresh:
                return self.update_station(instance, kwargs)
            return instance
        else:
            try:
                point = dict(X=position_x, Y=position_y, Z=position_z)
                # check if db and protocol exists
                prot_e = object
                network_id = object
                if isinstance(protocol, int):
                    prot_e = self.get_protocol_by_id(protocol.upper())
                    prot_id = prot_e.id
                else:

                    prot_e = self.get_protocol_id(protocol)
                    prot_id = prot_e.id
                if isinstance(server, str) and not server.isdigit():
                    server_e = self.get_server_id(server.upper())
                    server_id = server_e.id
                elif server.isdigit():
                    server_e = self.get_server_by_id(server)
                    server_id = server_e.id
                if isinstance(network, int):
                    network_e = self.get_network_by_id(network.upper())
                    network_id = network_e.id
                else:
                    network_e = self.get_network_id(network)
                    network_id = network_e.id
                if prot_e:
                    station = Station(code=code,
                                      name=name,
                                      position_x=point['X'],
                                      position_y=point['Y'],
                                      position_z=point['Z'],
                                      interface_port=interface_port,
                                      protocol_host=protocol_host,
                                      port=port,
                                      host=host,
                                      protocol_id=prot_id,
                                      active=active,
                                      server_id=server_id,
                                      network_id=network_id)
                    self.create_station(station)
                    self.logger.info("Creada nueva estación %s" % instance)
                    return station
                else:
                    return None
            except Exception as ex:
                print("Alguna falla al crear nueva station -> %s" % ex)
                raise ex

    def create_station(self, station):
        self.session.add(station)
        self.session.commit()

    def update_station(self, instance, kwargs):
        differences = {}
        t_name = 'station'
        code = kwargs.get('code')
        name = kwargs.get('name')
        position_x = kwargs.get('ECEF_X')
        position_y = kwargs.get('ECEF_Y')
        position_z = kwargs.get('ECEF_Z')
        protocol_host = kwargs.get('protocol_host')
        host = kwargs.get('host')
        port = int(kwargs.get('port'))
        interface_port = int(kwargs.get('interface_port'))
        protocol = kwargs.get('protocol')
        server = kwargs.get('server_id', "atlas")
        active = kwargs.get('active', False)
        network = kwargs.get("network_id","3g")
        position_x = kwargs.get('ECEF_X')
        position_y = kwargs.get('ECEF_Y')
        position_z = kwargs.get('ECEF_Z')

        point = dict(X=position_x, Y=position_y, Z=position_z)
        # check if db and protocol exists
        prot_id = None
        network_id = None

        if isinstance(protocol, int):
            prot_e = self.get_protocol_by_id(protocol.upper())
            prot_id = prot_e.id
        else:

            prot_e = self.get_protocol_id(protocol)
            prot_id = prot_e.id
        kwargs["protocol_id"] = prot_id

        if isinstance(server, str) and not server.isdigit():
            server_e = self.get_server_id(server.upper())
            server_id = server_e.id
        elif server.isdigit():
            server_e = self.get_server_by_id(server)
            server_id = server_e.id
        kwargs["server_id"] = server_id

        if isinstance(network, int):
            network_e = self.get_network_by_id(network.upper())
            network_id = network_e.id
        else:
            network_e = self.get_network_id(network)
            network_id = network_e.id
        kwargs["network_id"] = server_id

        if prot_e:
            station = Station(code=code,
                              name=name,
                              position_x=point['X'],
                              position_y=point['Y'],
                              position_z=point['Z'],
                              interface_port=interface_port,
                              protocol_host=protocol_host,
                              port=port,
                              host=host,
                              protocol_id=prot_id,
                              active=active,
                              server_id=server_id,
                              network_id=network_id)

            for k, v in station.json.items():
                val = instance.json.get(k)
                if val:
                    if v != val and k!='id':
                        if k.startswith('ECEF'):
                            key = k.replace("ECEF", "position").lower()
                            differences[key] = v
                        else:
                            differences[k] = v
            for k, v in differences.items():
                if k in station.json.keys():
                    self.update_table(t_name, instance, k, v)
        return instance

    def delete_station(self, station):
        self.session.delete(station)
        self.session.flush()

    def get_stations(self, server='atlas', only_active=True):
        # for sta in stations:
        new_stations = []
        if only_active:
            server = self.get_server_id(server)
            new_stations = self.session.query(
                Station).filter_by(active=True, server_id=server.id)
        else:
            new_stations = self.get_list(Station)
        return new_stations

    def get_station_id(self, code):
        # code is a unique value
        u = self.session.query(Station).filter_by(code=code).first()
        if u:
            return u.id
        else:
            return None

    def get_station_by_id(self, pk):
        u = self.session.query(Station).filter_by(id=pk).first()
        if u:
            return u
        else:
            return None

    def get_stations_near(self, center_point, km):
        lat = center_point[0]
        lon = center_point[1]
        point = "POINT(" + str(lon) + " " + str(lat) + ")"
        Q = "ST_GeogFromText(\'%s\')" % point
        print(point)
        # u = self.session.query(Station).filter(
        #    functions.ST_DWithin(
        #        Station.position,
        #        Q, km * 1000,true))
        strq = "select * from station where ST_DWithin(ST_GeogFromText(\'" + \
            point + "\'),position," + str(km * 1000) + ",true)"
        stmt = text(strq)
        result = self.session.execute(stmt)
        return result

    def get_station_data(self, server='atlas', active="true"):
        server = self.get_server_id(server)
        file_q = Path(self.path / "sql/station_query.sql")
        if file_q.exists():
            sql_query_tpl = file_q.read_text()
            sql_query = sql_query_tpl.replace("[SERVER_ID]",
                                              str(server.id)).replace("[ACTIVE]", active)
            stmt = text(sql_query)
            result = self.session.execute(stmt)
            items = []
            for st in result:
                item = dict(**st)
                code = item["code"]
                protocol = item["protocol"]
                item["table_name"] = f"{code}_{protocol}"
                get_llh(item)
                items.append(item)
            return items

    # Network Group

    def network(self, **kwargs):
        if kwargs:
            name = kwargs.get('name', "3g").upper()
            description = kwargs.get("description", "Red de celular")
        network = self.session.query(
            NetworkGroup).filter_by(name=name).first()
        if network:
            self.logger.info("network ya exitse, %s" % network)
            return network
        else:
            network = NetworkGroup(
                name=name,
                description=description)
            self.create_network(network)
            self.logger.info("Nuevo network creado, %s" % network)
            return network

    def create_network(self, network):
        self.session.add(network)
        self.session.commit()

    def update_network(self, instance, fields, values):
        t_name = 'network_instance'
        assert len(fields) == len(values)
        for i, f in enumerate(fields):
            v = values[i]
            self.update_table(t_name, instance, f, v)

    def delete_network(self, network):
        self.session.delete(network)
        self.session.flush()

    def get_network(self):
        return self.get_list(NetworkGroup)

    def get_network_id(self, name):
        # code is a unique value
        u = self.session.query(NetworkGroup).filter_by(name=name.upper()).all()
        if u:
            return u[0]
        else:
            return None

    def get_network_by_id(self, pk):
        u = self.session.query(NetworkGroup).filter_by(id=pk).all()
        if u:
            return u[0]
        else:
            return None

  

    # Server Instance

    def server(self, **kwargs):
        if kwargs:
            host_name = kwargs.get('host_name', "atlas")
            host_ip = kwargs.get("host_ip", "10.54.217.15")
            gnsocket_port = kwargs.get("gnsocket")
            activated = kwargs.get("activated", False)
        server = self.session.query(
            ServerInstance).filter_by(host_name=host_name).first()
        if server:
            self.logger.info("server ya exite, %s" % server)
            return server
        else:
            server = ServerInstance(host_name=host_name,
                                    host_ip=host_ip,
                                    gnsocket_port=gnsocket_port,
                                    activated=activated)
            self.create_server(server)
            self.logger.info("Nuevo server creado, %s" % server)
            return server

    def create_server(self, server):
        self.session.add(server)
        self.session.commit()

    def update_server(self, instance, fields, values):
        t_name = 'server_instance'
        assert len(fields) == len(values)
        for i, f in enumerate(fields):
            v = values[i]
            self.update_table(t_name, instance, f, v)

    def active_server(self, instance):
        self.update_server(instance, ["activated"], [True])

    def deactive_server(self, instance):
        self.update_server(instance, ["activated"], [False])

    def delete_server(self, server):
        self.session.delete(server)
        self.session.flush()

    def get_server(self):
        return self.get_list(ServerInstance)

    def get_server_id(self, name):
        # code is a unique value
        u = self.session.query(ServerInstance).filter(ServerInstance.host_name.ilike(name)).all()
        if u:
            return u[0]
        else:
            return None

    def get_server_by_id(self, pk):
        u = self.session.query(ServerInstance).filter_by(id=pk).all()
        if u:
            return u[0]
        else:
            return None

    # PROTOCOL TABLE

    def protocol(self, **kwargs):
        if bool(kwargs):
            name = kwargs['name']
            ref = kwargs['ref']
            class_name = kwargs['class_name']
            git = kwargs['git']
        protocol = self.session.query(Protocol).filter_by(name=name).first()
        if protocol:
            self.logger.info("Protocolo ya exite, %s" % protocol)
            return protocol
        else:
            protocol = Protocol(name=name,
                                ref_url=ref,
                                class_name=class_name,
                                git_url=git)
            self.create_protocol(protocol)
            self.logger.info("Nuevo protocolo creado, %s" % protocol)
            return protocol

    def create_protocol(self, protocol):
        self.session.add(protocol)
        self.session.commit()

    def update_protocol(self, instance, fields, values):
        t_name = 'protocol'
        assert len(fields) == len(values)
        for f in fields:
            v = values[fields.index(f)]
            self.update_table(t_name, instance, f, v)

    def delete_protocol(self, protocol):
        self.session.delete(protocol)
        self.session.flush()

    def get_protocol(self):
        return self.get_list(Protocol)

    def get_protocol_id(self, name):
        # code is a unique value
        u = self.session.query(Protocol).filter_by(name=name).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_protocol_by_id(self, pk):
        u = self.session.query(Protocol).filter_by(id=pk).all()
        if len(u) > 0:
            return u[0]
        else:
            return None
    # DBDATA TABLE

    def dbserver(self, **kwargs):
        try:
            path = kwargs.get('path')
            host = kwargs.get('host')
            port = int(kwargs.get('port'))
            user = kwargs.get('user')
            passw = kwargs.get('passw')
            info = kwargs.get('info')
            dbtype = kwargs.get('dbtype')
            dbname = kwargs.get('dbname')
            hostname = kwargs.get('hostname')
            if 'type_name' in kwargs:
                dbtype = kwargs.get('type_name')
            instance = self.session.query(DBServer).filter_by(hostname=hostname).first()
            if instance:
                self.logger.info("DBSserver existe, %s" % instance)
                return instance
            else:
                db_e = self.get_dbtype_id(dbtype)
                if db_e:
                    instance = DBServer(
                                      path=path,
                                      host=host,
                                      port=port,
                                      user=user,
                                      passw=passw,
                                      info=info,
                                      dbtype_id=db_e.id,
                                      dbname=dbname, 
                                      hostname=hostname)
                    self.create_dbserver(instance)
                    self.logger.info("Dbserver creada, %s" % instance)
                    return instance
                else:
                    return None
        except Exception as ex:
            self.logger.exception("Error al crear new dbserver, %s" % ex)
            raise ex

    def create_dbserver(self, dbserver, commit=True):
        self.session.add(dbserver)
        if commit:
            self.session.commit()
        else:
            print("DBServer Data must be commited to be saved")

    def update_dbserver(self, instance, new_dict):
        t_name = 'dbserver'
        dbserver = object_as_dict(instance)
        for k in new_dict.keys():
            if k in dbserver.keys():
                v = new_dict[k]
                db_e = self.get_dbtype_by_id(dbserver)
                new_dict['dbtype_id'] = db_e.id
                if type(v) == type(dbserver[k]) and v != dbserver[k]:
                    self.update_table(t_name, instance, k, v)

    def delete_dbserver(self, dbserver):
        self.session.delete(dbserver)
        self.session.flush()

    def get_dbservers(self):
        return self.get_list(DBServer)

    def get_dbserver_id(self, hostname):
        # code is a unique value
        u = self.session.query(DBServer).filter_by(hostname=hostname).all()
        if u:
            return u[0].id
        else:
            return None

    def get_dbserver_list_by_type(self, dtype):
        # code is a unique value
        u = self.session.query(DBServer).filter_by(dbtype=dtype).all()
        return u

    def get_dbserver_by_id(self, pk):
        u = self.session.query(DBServer).filter_by(id=pk).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbserver_data(self, station_id):
        key = "[STATION_ID]"
        file_q = Path(self.path / "sql/dbserver_query.sql")
        if file_q.exists():
            sql_query = file_q.read_text().replace(key,
                                                   str(station_id))
            stmt = text(sql_query)
            result = self.session.execute(stmt)
            return result

    def dbdata(self, **kwargs):
        try:
            station = kwargs.get('station')
            database = kwargs.get('dbserver')
            prioridad = kwargs.get("priority")
            
            # buscar station, database
            station_id = self.get_station_id(station)
            database_id = self.get_dbserver_id(database)
            db_e = self.get_dbdata_by_id(station_id, database_id,
                                         prioridad)
            if (station_id and database_id) and not db_e:
                instance = DBData(
                    station_id=station_id,
                    database_id=database_id, 
                    priority=prioridad)
                self.create_dbdata(instance)
                self.logger.info("Dbdata creada, %s" % instance)

                return instance
            else:
                return db_e
        except Exception as ex:
            self.logger.exception("Error al crear new dbdata, %s" % ex)
            raise ex

    def create_dbdata(self, dbdata, commit=True):
        self.session.add(dbdata)
        if commit:
            self.session.commit()
        else:
            print("DBData must be commited to be saved")

    def get_dbdata_data(self):
        file_q = Path(self.path / "sql/dbdata_query.sql")
        if file_q.exists():
            sql_query = file_q.read_text()
            stmt = text(sql_query)
            result = self.session.execute(stmt)
            return result

    def get_dbdata_by_id(self, station_id, database_id, prioridad):
        u = self.session.query(DBData).\
            filter_by(
                database_id=database_id, 
                station_id=station_id, 
                priority=prioridad).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    # DBTYPE TABLE

    def dbtype(self, **kwargs):
        if kwargs:
            typedb = kwargs['typedb']
            name = kwargs['name']
            url = kwargs['url']
            data_list = kwargs['data_list']
        instance = self.session.query(DBType).filter_by(name=name).first()
        if instance:
            self.logger.info("DBType existe, %s" % instance)
            return instance
        else:
            instance = DBType(
                typedb=typedb,
                name=name,
                url=url,
                data_list=data_list)
            self.create_dbtype(instance)
            self.logger.info("DBType creada, %s" % instance)
            return instance

    def create_dbtype(self, dbtype):
        self.session.add(dbtype)
        self.session.commit()

    def update_dbtype(self, instance, fields, values):
        t_name = 'dbtype'
        assert len(fields) == len(values)
        for f in fields:
            v = values[fields.index(f)]
            self.update_table(t_name, instance, f, v)

    def delete_dbtype(self, dbtype):
        self.session.delete(dbtype)
        self.session.flush()

    def get_dbtype(self):
        return self.get_list(DBType)

    def get_dbtype_id(self, name):
        # code is a unique value
        u = self.session.query(DBType).filter_by(name=name).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbtype_by_id(self, db_id):
        # code is a unique value
        u = self.session.query(DBType).filter_by(id=db_id).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbtype_list_by_type(self, dtype):
        # code is a unique value
        u = self.session.query(DBData).filter_by(typedb=dtype).all()
        return u

    # DataDestiniy section


class SessionDataWork(SessionCollector):

    def datadestiniy(self, **kwargs):
        if bool(kwargs):
            station = kwargs['station']
            destiny = kwargs['destiny']
            uri = kwargs['uri']
            port = kwargs['port']
            description = kwargs['description']
        instance = self.session.query(DataDestiny).filter_by(
            station_id=station_id,
            destiny=destiny,
            uri=uri).first()
        if instance:
            return instance
        else:
            sta_id = self.get_station_id(station)
            if sta_id:
                instance = DataDestiny(
                    station_id=sta_id,
                    destiny=destiny,
                    uri=uri,
                    port=port,
                    description=description
                )
                self.create_datadestiny(instance)
                return instance
            else:
                return None

    def create_datadestiny(self, datadestiny):
        self.session.add(datadestiny)
        self.session.commit()

    def update_datadestiny(self, instance, fields, values):
        t_name = 'datadestiny'
        assert len(fields) == len(values)
        for f in fields:
            v = values[fields.index(f)]
            self.update_table(t_name, instance, f, v, **{'schema': 'datawork'})

    def delete_datadestiny(self, datadestiny):
        self.session.delete(datadestiny)
        self.session.flush()

    def get_datadestiny(self):
        return self.get_list(DataDestiny)

    def get_datadestiny_id(self, name):
        # code is a unique value
        u = self.session.query(DataDestiny).filter_by(
            station_id=station_id,
            destiny=destiny,
            uri=uri).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_datadestiny_by_id(self, db_id):
        # code is a unique value
        u = self.session.query(DataDestiny).filter_by(id=db_id).all()
        if len(u) > 0:
            return u[0]
        else:
            return None

    def get_dbtype_list_by_type(self, destiny_type):
        # code is a unique value
        u = self.session.query(DataDestiny).filter_by(
            destiny=destiny_type).all()
        return u

    def get_destiny_by_station(self, station):
        sta_id = self.get_station_id(station)
        u = self.session.query(DataDestiny).filter_by(station_id=sta_id).all()
        return u
