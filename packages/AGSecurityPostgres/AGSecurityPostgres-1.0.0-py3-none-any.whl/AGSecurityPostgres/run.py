from security import AGSecurityListPostgres, AGCreateSecurityPostgres
import psycopg2

DB_HOST = 'localhost'
DB_PORT = 5432
DB_DATABASE = 'eazymessage'
DB_USER = 'michael'
DB_PASS = 'plokijuh'
DB_USER = 'michael'
DB_PASS = 'plokijuh'
DB_USER2 = 'string'
DB_PASS2 = 'string'
conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_DATABASE, user=DB_USER2, password=DB_PASS2)

security = AGSecurityListPostgres(usename=DB_USER, conn=conn)

print(security.get_view_rights_sp())

conn.close()