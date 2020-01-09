import argparse
from os import getenv
import psycopg2

parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", help="host location of postgres database", type=str)
parser.add_argument("-U", "--user", help="username to connect to the database", type=str)
parser.add_argument("-d", "--dbname", help="database name", type=str)
parser.add_argument("-p", "--port", help="port to connect to postgres", type=str)
args = parser.parse_args()
password = getenv('fwpgpass')

conn = psycopg2.connect(
    f"dbname={args.dbname} user={args.user} host={args.host} port={args.port} password={password}"
)
cur = conn.cursor()
print("connected to database")

cur.execute("SELECT MIN(id), MAX(id) FROM osm_ways;")
min_id, max_id = cur.fetchone()
print(f"there are {max_id - min_id + 1} edges to be processed")
cur.close()

interval = 50000
for x in range(min_id, max_id+1, interval):
    cur = conn.cursor()
    cur.execute(
    f"select pgr_createTopology('osm_ways', 0.000000001, 'geom', 'id', source:='source', target:='target', rows_where:='id>={x} and id<{x+interval}')"
)
    conn.commit()
    x_max = x + interval - 1
    if x_max > max_id:
        x_max = max_id
    print(f"edges {x} - {x_max} have been processed")

cur = conn.cursor()
# cur.execute("""ALTER TABLE ways_vertices_pgr
#   ADD COLUMN IF NOT EXISTS lat float8,
#   ADD COLUMN IF NOT EXISTS lon float8;""")

# cur.execute("""UPDATE ways_vertices_pgr
#   SET lat = ST_Y(the_geom),
#       lon = ST_X(the_geom);""")

conn.commit()