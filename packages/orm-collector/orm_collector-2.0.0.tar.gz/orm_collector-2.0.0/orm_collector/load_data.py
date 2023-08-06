from networktools.library import check_type
from orm_collector import SessionCollector
from pathlib import Path
import csv
from rich import print

def load_protocol(session, file_protocol):
     this_protocol = dict()
     with file_protocol.open() as rfile:
         reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
         for row in reader:
             print(row)
             for k in row.keys():
                 row[k] = row[k].rstrip().lstrip()
             p = row['name']
             print("Load protocl",p, row)
             if not session.get_protocol_id(p) and p != '':
                 this_protocol[int(row['id'])] = session.protocol(**row)
     print("Protocol ok")
                 

def load_dbtype(session, file_dbtype):
    this_dbtype = dict()
    with file_dbtype.open() as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            print(row)
            p = row['name']
            if not session.get_dbtype_id(p) and p != '':
                this_dbtype[int(row['id'])] = session.dbtype(**row)
    print("DBType ok")

def load_dbserver(session, file_dbserver):
    this_dbserver = dict()
    print("Path->", file_dbserver)
    with file_dbserver.open() as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            if not row['port'].isdigit():
                row['port'] = 0
            path = row['path']
            if path == '':
                row['path'] = None
            hostname = row["hostname"]
            print("Hostname", hostname)
            if not session.get_dbserver_id(hostname):
                print("Saving->", row)
                this_dbserver[int(row['id'])] = session.dbserver(**row)
                print("Saved dbdata", this_dbserver[int(row['id'])])


def load_server(session, file_server):
    this_server = dict()

    with file_server.open() as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            print(row)
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            hostname = row['host_name']
            row["gnsocket"] = check_type(row.get('gnsocket', 0), 'int')
            row["activated"] = check_type(row.get("activated"))
            if not session.get_protocol_id(hostname):
                this_server[int(row['id'])] = session.server(**row)

    print("This server->", this_server)
    [print(server.host_name) for server in this_server.values()]



def load_network(session, file_network):
    this_network = dict()
    with file_network.open() as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            print(row)
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            this_network[int(row['id'])] = session.network(**row)
    print("This network->", this_network)
    [print(network) for network in this_network.values()]

    
def load_station(session, file_station):
    this_station = dict()

    print("Server Instances ok")

    with file_station.open() as rfile:
        reader = csv.DictReader(rfile, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            port = row.get('port', 0)
            iport = row.get('interface_port', 0)
            p = row['code']
            station_data = dict(
                id=check_type(row.get('id'), 'int'),
                code=row['code'],
                name=row['name'],
                ECEF_X=float(row['ECEF_X']),
                ECEF_Y=float(row['ECEF_Y']),
                ECEF_Z=float(row['ECEF_Z']),
                host=row['host'],
                port=int(check_type(port, 'int')),
                interface_port=int(check_type(iport, 'int')),
                db=row['db'],
                protocol=row['protocol'],
                protocol_host=row["protocol_host"],
                active=check_type(row.get("active", 0)),
                server_id=row.get('server_id', "atlas"),
                network_id=row["network_id"]
            )
            this_station[int(row['id'])] = session.station(
                 **station_data, 
                 refresh=True)
            print(this_station[int(row['id'])])
    print("Station ok")

def load_dbdata(session, file_dbdata):
    this_dbdata = dict()
    with file_dbdata.open() as rfile:
        reader = csv.DictReader(rfile, delimiter=';',
                                quoting=csv.QUOTE_NONE)
        counter = 0
        for row in reader:
            print("ROW DBDATA", row)
            for k in row.keys():
                row[k] = row[k].rstrip().lstrip()
            dbdata = {
                 "station": row["station"],
                 "dbserver": row["dbserver"],
                 "priority": row["priority"]
            }
            this_dbdata[counter] = session.dbdata(
                 **dbdata, 
                 refresh=True)
            counter += 1 
    print(this_dbdata)
    
if __name__=='__main__':
    pwd = Path(__file__).parent
    file_protocol = pwd/"fixtures/protocol.csv"
    file_dbtype = pwd/"fixtures/dbtype.csv"
    file_server = pwd/"fixtures/server.csv"
    file_network = pwd/"fixtures/network.csv"
    file_station = pwd/"fixtures/station.csv"
    file_dbserver = pwd/"fixtures/dbserver.csv"
    file_dbdata = pwd/"fixtures/dbdata.csv"
    session = SessionCollector()
    if file_protocol.exists():
         load_protocol(session, file_protocol)
    if file_dbtype.exists():
         load_dbtype(session, file_dbtype)
    if file_server.exists():
         load_server(session, file_server)
    if file_network.exists():
         load_network(session, file_network)
    if file_station.exists():
         load_station(session, file_station)
    if file_dbserver.exists():
         load_dbserver(session, file_dbserver)
    if file_dbdata.exists():
         load_dbdata(session, file_dbdata)
