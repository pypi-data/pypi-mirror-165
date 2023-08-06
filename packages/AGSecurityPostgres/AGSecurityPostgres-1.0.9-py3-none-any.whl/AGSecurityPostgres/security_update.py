import psycopg2
import psycopg2.extras
from AGCoder import Coder
from AGQueryPostgres import AGQueryPostgres


#
# Shared library to call stored procedures with changes in security settings
#
class AGSecurityUpdatePostgres:
    usename: str = None
    command: list = []

    # Variables
    conn = None
    conn_string: str = None

    def __init__(self, usename):
        # self.conn_string = DB_CONNECTION_SECURITY_OFFICER
        self.conn = psycopg2.connect(self.conn_string)

        self.usename = usename
        self._define_sql()
        self._define_list_sql(usename)

    #
    # SQL Library
    #
    def _define_sql(self):
        c = Coder("sql")

        # Create role
        self.command.append(
            {"create_role": "CREATE ROLE %1"}
        )

    def _define_list_sql(self, usename):
        #
        # Database
        #
        db_grant = AGQueryPostgres("pg_catalog", "pg_roles", conn=self.conn)
        db_grant.select = [
            "rolname", "rolsuper", "rolinherit", "rolcreaterole", "rolcreatedb", "rolcanlogin",
            "rolconnlimit", "rolvaliduntil", "rolreplication", "rolbypassrls"
        ]
        db_grant.where = [
            {
                "rolname": usename
            }
        ]
        db_grant.order_by = ["rolname"]
        db_grant_rows = db_grant.execute()

        #
        # Group
        #
        db_role = AGQueryPostgres("pg_catalog", "pg_auth_members", conn=self.conn)
        db_role.select = ["role.rolname"]
        db_role.id_name = "roleid"
        db_role.inner_join = [
            {
                "schema_name": "pg_catalog",
                "table_name": "pg_roles",
                "alias": "role",
                "relation": "oid",
            }
        ]
        db_role.where = [
            {
                "role.rolname": usename
            }
        ]
        db_role_rows = db_grant.execute()

        print(db_grant_rows)

