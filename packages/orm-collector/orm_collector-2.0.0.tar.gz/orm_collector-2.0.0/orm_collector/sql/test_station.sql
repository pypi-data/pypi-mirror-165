select station.id as id,
       station.code as st_code,
       station.name as st_name,
       station.host as st_host,
       station.port as st_port,
       position_x as ECEF_X,
       position_y as ECEF_Y,
       position_z as ECEF_Z,
       protocol_host,
       protocol.name as prt_name,
       dbselect.typedb as db_type,
       dbselect.name as db_name,
       dbselect.code as
       db_code,
       dbselect.path as db_path,
       dbselect.host as db_host,
       dbselect.port as db_port,
       dbselect.user as db_user,
       dbselect.passw as db_passw,
       dbselect.info as db_info,
       dbselect.typedb,
       dbselect.data_list as db_list,
       network_select.name as network 
       FROM station
       INNER JOIN protocol ON station.protocol_id=protocol.id
       INNER JOIN (select dbdata.id, dbdata.code, 
             dbdata.path,
             dbdata.host,
             dbdata.port,
             dbdata.user,
             dbdata.passw,
             dbdata.info,
             dbdata.dbname,
             dbtype.typedb,
             dbtype.name,
             dbtype.data_list from dbdata inner join dbtype on
             dbdata.dbtype_id=dbtype.id)
        as dbselect on station.db_id=dbselect.id
	INNER JOIN (
	      select network_group.id, network_group.name
	      from network_group
	) as network_select on station.network_id=network_select.id
        where station.server_id=1 and station.active=false
