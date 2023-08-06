import os
import psycopg2
import psycopg2.extras
from AGCoder import Coder
from AGQueryPostgres import AGQueryPostgres

#
# Variable with all security settings for a PostgreSQL user
# Should be kept as session variable just like the conn object
# Check if standard user have rights to these information by default
# If not create tmp_permission_user and grant the right for the information
#
class AGSecurityListPostgres:
    usename: str = None
    dirname = os.getcwd()

    def __init__(self, usename, conn):
        self.conn = conn
        self.usename = usename

    #
    # If a user is member of one or more groups, and just one of the groups have a permission,
    # the user will have this permission i.e. false + false + true = true, false + false = false
    # all these calls should be packed into stored procedures or views
    #
    def get_user_rights(self):
        #
        # Database
        #
        db_grant = AGQueryPostgres(conn=self.conn)
        db_grant.json_obj.schema_name = "pg_catalog"
        db_grant.json_obj.table_name = "pg_roles"
        db_grant.json_obj.select = [
            "rolname", "rolsuper", "rolinherit", "rolcreaterole", "rolcreatedb", "rolcanlogin",
            "rolconnlimit", "rolvaliduntil", "rolreplication", "rolbypassrls"
        ]
        db_grant.json_obj.where = [
            {
                "rolname": self.usename
            }
        ]
        db_grant.json_obj.order_by = ["rolname"]
        db_grant_rows = db_grant.execute()

        return db_grant_rows["results"][0]

    def get_user_groups(self):
        db_grant = AGQueryPostgres(conn=self.conn)
        db_grant.json_obj.select = ["r.rolname", "r2.rolname"]
        db_grant.json_obj.schema_name = "pg_catalog"
        db_grant.json_obj.table_name = "pg_roles"
        db_grant.json_obj.alias_name = 'r'
        db_grant.json_obj.inner_join = [{
            "schema_name": 'pg_catalog',
            "table_name": 'pg_roles',
            "alias_name": 'r2',
            "on": 'r2.rolname = r.rolname OR r2.rolname IN (' + ', '.join(self.get_user_groups_subquery()) + ')'
        }]
        db_grant.json_obj.order_by = ["r.rolname", "r2.rolname"]
        db_grant.json_obj.where_string = 'r.rolname = CURRENT_USER'
        db_grant_rows = db_grant.execute()
        return list(map(lambda x: "'" + x["r2_rolname"] + "'", db_grant_rows["results"]))

    def get_user_groups_subquery(self):
        db_grant = AGQueryPostgres(conn=self.conn)
        db_grant.json_obj.select = ["groname"]
        db_grant.json_obj.schema_name = "pg_catalog"
        db_grant.json_obj.table_name = "pg_group"
        db_grant.json_obj.alias_name = 'g'
        db_grant.json_obj.inner_join = [{
            "schema_name": 'pg_catalog',
            "table_name": 'pg_auth_members',
            "alias_name": 'am',
            "on": 'am.roleid = g.grosysid'
        }, {
            "schema_name": 'pg_catalog',
            "table_name": 'pg_roles',
            "alias_name": 'u',
            "on": 'u.oid = am.member'
        }]
        db_grant.json_obj.where_string = 'rolname = CURRENT_USER'

        db_grant_rows = db_grant.execute()
        return list(map(lambda x: "'" + x["groname"] + "'", db_grant_rows["results"]))

    def get_database_rights(self):
        # Return JSON with database
        pass

    # If you do not pass schema name, list them all, table name=list everything in the schema
    def get_table_rights(self, schema_name=None, table_name=None):
        db_grant = AGQueryPostgres(conn=self.conn)
        db_grant.json_obj.select = ["t.table_schema", "t.table_name"]
        db_grant.json_obj.schema_name = "information_schema"
        db_grant.json_obj.table_name = "tables"
        db_grant.json_obj.alias_name = 't'
        db_grant.json_obj.inner_join = [{
            "schema_name": 'information_schema',
            "table_name": 'table_privileges',
            "alias_name": 't2',
            "on": "t2.table_schema = t.table_schema AND t2.table_name = t.table_name AND t.table_type = 'BASE TABLE'"
        }]
        db_grant.json_obj.order_by = ["r.rolname", "r2.rolname"]
        db_grant.json_obj.where_string = 't2.grantee IN (' + ','.join(self.get_user_groups()) + ')'
        if schema_name:
            db_grant.json_obj.where_string += f" AND t.table_schema = '{schema_name}'"
        if table_name:
            db_grant.json_obj.where_string += f" AND t.table_name = '{table_name}'"

        db_grant.json_obj.total = [{
            "action": "array_agg",
            "column": "t2.privilege_type",
        }]

        db_grant.json_obj.order_by = ["t.table_schema", "t.table_name"]

        db_grant_rows = db_grant.execute()
        return db_grant_rows["results"]

    # If you do not pass schema name, list them all, view name=list everything in the schema
    def get_view_rights(self, schema_name=None, view_name=None):
        db_grant = AGQueryPostgres(conn=self.conn)
        db_grant.json_obj.select = ["t.table_schema", "t.table_name"]
        db_grant.json_obj.schema_name = "information_schema"
        db_grant.json_obj.table_name = "tables"
        db_grant.json_obj.alias_name = 't'
        db_grant.json_obj.inner_join = [{
            "schema_name": 'information_schema',
            "table_name": 'table_privileges',
            "alias_name": 't2',
            "on": "t2.table_schema = t.table_schema AND t2.table_name = t.table_name AND t.table_type = 'VIEW'"
        }]
        db_grant.json_obj.order_by = ["r.rolname", "r2.rolname"]
        db_grant.json_obj.where_string = 't2.grantee IN (' + ','.join(self.get_user_groups()) + ')'
        if schema_name:
            db_grant.json_obj.where_string += f" AND t.table_schema = '{schema_name}'"
        if view_name:
            db_grant.json_obj.where_string += f" AND t.table_name = '{view_name}'"

        db_grant.json_obj.total = [{
            "action": "array_agg",
            "column": "t2.privilege_type",
        }]

        db_grant.json_obj.order_by = ["t.table_schema", "t.table_name"]

        db_grant_rows = db_grant.execute()
        return db_grant_rows["results"]

    def get_stored_procedure_rights(self, schema_name=None, stored_procedure_name=None):
        pass

    def get_user_groups_sql(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open("./sql_queries/get_user_groups.sql", "r").read()
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()
        return lst

    # If you do not pass schema name, list them all, table name=list everything in the schema
    def get_table_rights_sql(self, schema_name=None, table_name=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open("./sql_queries/get_table_rights.sql", "r").read()
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()
        return lst

    # If you do not pass schema name, list them all, view name=list everything in the schema
    def get_view_rights_sql(self, schema_name=None, view_name=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open("./sql_queries/get_view_rights.sql", "r").read()
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()
        return lst

    def get_stored_procedure_rights_sql(self, schema_name=None, stored_procedure_name=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open("./sql_queries/get_stored_procedure_rights.sql", "r").read()
        cur.execute(query)
        lst = cur.fetchall()
        cur.close()
        return lst

    def get_user_groups_sp(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        funcname = 'public.fn_user_groups'
        params = ()
        cur.callproc(funcname, params)
        lst = cur.fetchall()
        cur.close()
        return lst

    # If you do not pass schema name, list them all, table name=list everything in the schema
    def get_table_rights_sp(self, schema_name=None, table_name=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        funcname = 'public.fn_table_rights'
        params = (schema_name, table_name)
        cur.callproc(funcname, params)
        lst = cur.fetchall()
        cur.close()
        return lst

    # If you do not pass schema name, list them all, view name=list everything in the schema
    def get_view_rights_sp(self, schema_name=None, view_name=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        funcname = 'public.fn_view_rights'
        params = (schema_name, view_name)
        cur.callproc(funcname, params)
        lst = cur.fetchall()
        cur.close()
        return lst

    def get_stored_procedure_rights_sp(self, schema_name=None, stored_procedure_name=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        funcname = 'public.fn_stored_procedure_rights'
        params = (schema_name, stored_procedure_name)
        cur.callproc(funcname, params)
        lst = cur.fetchall()
        cur.close()
        return lst


#
class AGCreateSecurityPostgres:
    usename: str = None
    dirname = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, usename, conn):
        self.conn = conn
        self.usename = usename

    def execute(self):
        self.create_view_user_groups()
        self.create_function_user_groups()
        self.create_function_table_rights()
        self.create_function_view_rights()
        self.create_function_stored_procedure_rights()
        self.create_function_table_exists()
        self.create_function_record_exists()

    def create_view_user_groups(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_view_user_groups.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_table_rights(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_fn_table_rights.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_view_rights(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_fn_view_rights.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_stored_procedure_rights(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_fn_stored_procedure_rights.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_user_groups(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_fn_user_groups.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_table_exists(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_fn_table_exists.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_record_exists(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        query = open(os.path.join(self.dirname, "/sql_queries/create_fn_record_exists.sql"), "r").read()
        cur.execute(query)
        self.conn.commit()
        cur.close()


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

# s = AGSecurityListPostgres("test")
# s.get_user_groups.sql()
