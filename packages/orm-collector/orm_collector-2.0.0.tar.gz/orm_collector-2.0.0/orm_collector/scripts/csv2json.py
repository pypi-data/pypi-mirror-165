import ujson as json
import csv
from django.utils.text import slugify
from pathlib import Path
import click

def add_list(elem_list):
    lista = []
    lista.append(elem_list)
    return lista


def file_csv2json(model, file_name, field, condition):
    path = Path(file_name)
    data_list = []
    if path.exists():
        with open(path, 'r') as read:
            reader = csv.DictReader(read, delimiter=';')
            for row in reader:
                field_slug = "slug_%s" % field
                dict_data = {}
                for key, value in row.items():
                    if not key == "id":
                        if condition.get(key):
                            value = condition.get(key)(value)
                        else:
                            value = value.strip()
                        dict_data.update({key: value})
                if field:
                    main_field = row.get(field)
                    dict_data.update({field_slug: slugify(main_field)})
                new_data = {
                    "model": model,
                    "pk": int(row.get('id').strip()),
                    "fields": dict_data}
                data_list.append(new_data)

        new_file_path = "./fixtures/%s.json" % file_name.split('.')[0]
        with open(new_file_path, 'w') as write_json:
            write_json.write("[\n")
            len_list = len(data_list)
            for i, elem in enumerate(data_list):
                json.dumps(elem, write_json, indent=2)
                if i < len_list-1:
                    write_json.write(',\n')
                else:
                    write_json.write('\n')
            write_json.write("]")
    else:
        print("No existe el archivo en %s" %path)

@click.command()
@click.option("--directorio",
              default="./fixtures",
              show_default=True, help="Ruta al directorio que contiene archivos")
def csv2json(directorio):
    files = [
        ('station.station', 'station.csv', 'name', {}),
        ('database.dbdata', 'dbdata_info.csv',
         'name', {"port": int, "dbtype": add_list}),
        ("network_register.network_register", "network.csv", "name", {}),
        ("server.server", "server.csv", "host_name", {}),
        ('database.dbtype', 'dbtype.csv', 'name', {})
    ]
    directorio =  directorio.strip().rstrip("/").strip()
    for files, file_name, field, condition in files:
        file_path = "%s/%s" % (directorio, file_name)
        file_csv2json(model, file_path, field, condition)
