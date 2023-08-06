select dbdata.id as id, dbdata.station_id as station_id, st.name,
	   st.code, ds.hostname, ds.host, ds.port, ds.dbname,
	   dbdata.database_id as database_id, 
from dbdata 
inner join dbtype on dbtype_id=dbtype.id
inner join dbserver as ds on database_id=ds.id
inner join station as st on station_id=station.id
