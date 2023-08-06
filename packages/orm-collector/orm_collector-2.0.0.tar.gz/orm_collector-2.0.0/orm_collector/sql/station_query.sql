select station.id as id,
       station.code as code,
       station.name as name,
       station.host as host,
	   station.interface_port as interface_port,
       station.port as port,
       position_x as ecef_x,
       position_y as ecef_y,
       position_z as ecef_z,
       protocol_host,
       protocol.name as protocol,
       --
       network_select.name as network 
       FROM station
       INNER JOIN protocol ON station.protocol_id=protocol.id
       -- INNER JOIN (select 
	   -- 				 dbserver.id, 
	   -- 				 dbserver.path,
	   -- 				 dbserver.host,
	   -- 				 dbserver.port,
	   -- 				 dbserver.user,
	   -- 				 dbserver.passw,
	   -- 				 dbserver.info,
	   -- 				 dbserver.dbname,
	   -- 				 dbtype.name,
	   -- 				 dbtype.data_list from dbserver
	   -- 		inner join dbtype ON dbtype.database_id=dbserver.database_id
	   -- )
	INNER JOIN (
	      select network_group.id, network_group.name
	      from network_group
	) as network_select on station.network_id=network_select.id
        where station.server_id=[SERVER_ID] and station.active=[ACTIVE]
