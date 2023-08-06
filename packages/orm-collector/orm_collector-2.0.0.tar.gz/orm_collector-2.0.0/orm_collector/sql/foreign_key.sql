alter table station add network_id integer, add foreign key (network_id) references network_group(id)
