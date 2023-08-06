select dd.station_id, 
	   dd.database_id,
	   dd.priority, 
	   ds.hostname as hostname, 
	   ds.host as host,
	   ds.port as port, 
	   ds.dbname as dbname 
from dbserver as ds
inner join dbtype as dt on dt.id = ds.dbtype_id			  
inner join dbdata as dd on dd.database_id = ds.id
where dd.station_id=[STATION_ID]
