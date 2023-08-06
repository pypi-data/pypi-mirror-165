import click
from orm_collector.scripts.create_db import get_session, get_json2dbdata
from rich import print
import csv

@click.command()
@click.option("--name", 
              default="collector", 
              show_default=True, 
              help="Nombre del esquema a conectarse {collector, datawork}")
@click.option("--env/--no-env", default=True, show_default=True,
              type=bool, 
              required=True,
              help="Si obtener los datos de ambiente o cargarlos de un json o data entregada")
@click.option("--table", "-t", 
              default="station", 
              help="table name to show", )
@click.option("--csvfile", default="station.csv", help="Crear csv o no")
def show_data(name, env, table, csvfile):

    tables = (
        "station",
        "dbdata",
        "dbtype",
        "network_group",
        "protocol",
        "server_intance")

    fields = [
        "id",
        "code",
        "name",
        "host",
        "interface_port",
        "protocol_host",
        "port",
        "ECEF_X",
        "ECEF_Y",
        "ECEF_Z",
        "db",
        "protocol",
        "active",
        "server_id",
        "network_id"]

    schema = 'COLLECTOR'
    dbparams = dict(dbuser=f'{schema}_DBUSER',
                    dbpass=f'{schema}_DBPASS',
                    dbname=f'{schema}_DBNAME',
                    dbhost=f'{schema}_DBHOST',
                    dbport=f'{schema}_DBPORT')       
    session = get_session(name, env, {}, dbparams)
    dataset = []
    if table == 'station':
        stations = sorted(
            session.get_stations(),
            key=lambda e: e.id)
        for station in stations:
            db = session.get_dbdata_by_id(station.db_id)
            protocol = session.get_protocol_by_id(station.protocol_id)
            server = session.get_server_by_id(station.server_id)
            network = session.get_network_by_id(station.network_id)
            item = {
                "db": db.code,
                "protocol": protocol.name,
                "server_id": server.host_name,
                "network_id": network.name
            }
            for field, value in station.json.items():
                if not field.endswith("_id"):
                    item[field] = value
            dataset.append(item)
    with open(csvfile,"w") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')
        writer.writeheader()
        for item in dataset:
            writer.writerow(item)
    session.close()
