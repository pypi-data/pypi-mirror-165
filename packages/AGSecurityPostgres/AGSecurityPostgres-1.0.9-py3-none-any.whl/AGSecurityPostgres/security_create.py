import os
import psycopg2
import psycopg2.extras


class AGSecurityCreatePostgres:
    dirname = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, conn):
        self.conn = conn

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
        # query = open(os.path.join(self.dirname, "sql_queries/create_view_user_groups.sql"), "r").read()
        query = """CREATE OR REPLACE VIEW public.user_groups AS
                    SELECT r.rolname, r2.rolname as groname FROM pg_catalog.pg_roles r
                    INNER JOIN pg_catalog.pg_roles r2 ON r2.rolname = r.rolname OR r2.rolname IN (SELECT g.groname
                    FROM pg_catalog.pg_group g
                    INNER JOIN pg_catalog.pg_auth_members am ON am.roleid = g.grosysid
                    INNER JOIN pg_catalog.pg_roles u ON u.oid = am.member
                    WHERE u.rolname = r.rolname)
                    ORDER BY r.rolname, r2.rolname;"""
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_table_rights(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # query = open(os.path.join(self.dirname, "sql_queries/create_fn_table_rights.sql"), "r").read()
        query = """CREATE OR REPLACE FUNCTION public.fn_table_rights(
                        p_schema_name NAME,
                        p_table_name NAME
                    )
                    RETURNS TABLE (
                        schema NAME,
                        name NAME,
                        privileges VARCHAR[]
                    )
                    AS
                    $BODY$
                    BEGIN
                        RETURN QUERY
                        SELECT t.table_schema::NAME, t.table_name::NAME, array_agg(DISTINCT tp.privilege_type::VARCHAR)
                        FROM information_schema.tables t
                        INNER JOIN information_schema.table_privileges tp
                                ON tp.table_schema = t.table_schema AND tp.table_name = t.table_name AND
                                    t.table_type = 'BASE TABLE' -- tables type
                        WHERE tp.grantee IN (SELECT ug.groname FROM public.user_groups ug WHERE ug.rolname = CURRENT_USER)
                        AND (p_schema_name IS NULL OR t.table_schema = p_schema_name)
                        AND (p_table_name IS NULL OR t.table_name = p_table_name)
                        GROUP BY t.table_schema, t.table_name
                        ORDER BY t.table_schema, t.table_name;
                    END;
                    $BODY$
                    LANGUAGE 'plpgsql';"""
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_view_rights(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # query = open(os.path.join(self.dirname, "sql_queries/create_fn_view_rights.sql"), "r").read()
        query = """CREATE OR REPLACE FUNCTION public.fn_view_rights(
                        p_schema_name NAME,
                        p_view_name NAME
                    )
                    RETURNS TABLE (
                        schema NAME,
                        name NAME,
                        privileges VARCHAR[]
                    )
                    AS
                    $BODY$
                    BEGIN
                        RETURN QUERY
                        SELECT t.table_schema::NAME, t.table_name::NAME, array_agg(DISTINCT tp.privilege_type::VARCHAR)
                        FROM information_schema.tables t
                        INNER JOIN information_schema.table_privileges tp
                                ON tp.table_schema = t.table_schema AND tp.table_name = t.table_name AND
                                    t.table_type = 'VIEW' --views type
                        WHERE tp.grantee IN (SELECT ug.groname FROM public.user_groups ug WHERE ug.rolname = CURRENT_USER)
                        AND (p_schema_name IS NULL OR t.table_schema = p_schema_name)
                        AND (p_view_name IS NULL OR t.table_name = p_view_name)
                        GROUP BY t.table_schema, t.table_name
                        ORDER BY t.table_schema, t.table_name;
                    END;$BODY$
                    LANGUAGE 'plpgsql';"""
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_stored_procedure_rights(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # query = open(os.path.join(self.dirname, "sql_queries/create_fn_stored_procedure_rights.sql"), "r").read()
        query = """SELECT DISTINCT n.nspname as "schema",
                        p.proname as "name"
                    FROM pg_catalog.pg_proc p
                    INNER JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace
                    INNER JOIN (SELECT r.rolname, r2.rolname as groname FROM pg_catalog.pg_roles r
                        INNER JOIN pg_catalog.pg_roles r2 ON r2.rolname = r.rolname OR r2.rolname IN (SELECT g.groname
                        FROM pg_catalog.pg_group g
                        INNER JOIN pg_catalog.pg_auth_members am ON am.roleid = g.grosysid
                        INNER JOIN pg_catalog.pg_roles u ON u.oid = am.member
                        WHERE u.rolname = r.rolname)
                        ORDER BY r.rolname, r2.rolname) ug ON ug.rolname = CURRENT_USER
                    WHERE pg_catalog.has_function_privilege(ug.groname, p.oid, 'execute')
                        AND n.nspname NOT IN ('information_schema', 'pg_catalog', 'public') --exclude built in procedures
                    ORDER BY n.nspname, p.proname;"""
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_user_groups(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # query = open(os.path.join(self.dirname, "sql_queries/create_fn_user_groups.sql"), "r").read()
        query = """CREATE OR REPLACE FUNCTION public.fn_user_groups(
                    )
                    RETURNS SETOF pg_catalog.pg_roles
                    AS
                    $BODY$
                    BEGIN
                        RETURN QUERY
                        SELECT * from pg_catalog.pg_roles
                        WHERE rolname IN
                            (SELECT ug.groname FROM public.user_groups ug WHERE ug.rolname = CURRENT_USER)
                        ORDER BY rolname;
                    END;
                    $BODY$
                    LANGUAGE 'plpgsql';"""
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_table_exists(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # query = open(os.path.join(self.dirname, "sql_queries/create_fn_table_exists.sql"), "r").read()
        query = """CREATE OR REPLACE FUNCTION public.fn_table_exists(
                        p_schema_name NAME,
                        p_table_name NAME
                    )
                    RETURNS BOOL
                    AS
                    $BODY$
                    DECLARE
                        p_view_name NAME;
                        privileges VARCHAR[];
                    BEGIN
                        ASSERT p_schema_name IS NOT NULL, 'Must provide p_schema_name';
                        ASSERT p_table_name IS NOT NULL, 'Must provide p_table_name';
                        p_view_name := p_table_name || '_view';
                        SELECT INTO privileges (public.fn_view_rights(p_schema_name, p_view_name)).privileges;
                        IF privileges IS NULL THEN
                            RETURN FALSE;
                        END IF;
                        RETURN 'SELECT' = ANY(privileges);
                    END;$BODY$
                    LANGUAGE 'plpgsql';"""
        cur.execute(query)
        self.conn.commit()
        cur.close()

    def create_function_record_exists(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        # query = open(os.path.join(self.dirname, "sql_queries/create_fn_record_exists.sql"), "r").read()
        query = """CREATE OR REPLACE FUNCTION public.fn_record_exists(
                        p_schema_name NAME,
                        p_table_name NAME,
                        p_object_id UUID
                    )
                    RETURNS BOOL
                    AS
                    $BODY$
                    DECLARE
                        p_view_name NAME;
                        _sql TEXT;
                        i int;
                    BEGIN
                        ASSERT p_schema_name IS NOT NULL, 'Must provide p_schema_name';
                        ASSERT p_table_name IS NOT NULL, 'Must provide p_table_name';
                        ASSERT p_object_id IS NOT NULL, 'Must provide p_object_id';
                        p_view_name := p_table_name || '_view';
                        _sql := format('SELECT ID FROM %s.%s WHERE id = %L', p_schema_name, p_view_name, p_object_id);
                        EXECUTE _sql;
                        GET DIAGNOSTICS i = ROW_COUNT;
                        RETURN i = 1;
                    END;$BODY$
                    LANGUAGE 'plpgsql';"""
        cur.execute(query)
        self.conn.commit()
        cur.close()
