import re

from databricks import sql
from pyhive.sqlalchemy_hive import HiveDialect
from pyhive.sqlalchemy_hive import _type_map
from sqlalchemy import types
from sqlalchemy import util
from sqlalchemy import exc


class DatabricksDialect(HiveDialect):
    """
    Credit: https://github.com/crflynn/sqlalchemy-databricks
    License: MIT
    """

    name = "databricks"
    driver = "connector"  # databricks-sql-connector

    @classmethod
    def dbapi(cls):
        return sql

    def create_connect_args(self, url):
        # databricks-sql-connector expects just
        # server_hostname, access_token, and http_path
        kwargs = {
            "server_hostname": url.host,
            "access_token": url.password,
        }

        if url.query is not None and "http_path" in url.query:
            kwargs["http_path"] = url.query["http_path"]

        kwargs.update(url.query)
        return [], kwargs

    def get_table_names(self, connection, schema=None, **kw):
        # override to use row[1] in databricks instead of row[0] in hive
        query = "SHOW TABLES"
        if schema:
            query += " IN " + self.identifier_preparer.quote_identifier(schema)
        return [row[1] for row in connection.execute(query)]

    def _get_table_columns(self, connection, table_name, schema):
        full_table = table_name
        if schema:
            full_table = schema + "." + table_name
        # TODO using TGetColumnsReq hangs after sending TFetchResultsReq.
        # Using DESCRIBE works but is uglier.
        try:
            # This needs the table name to be unescaped (no backticks).
            rows = connection.execute("DESCRIBE {}".format(full_table)).fetchall()
        except exc.OperationalError as e:
            # Does the table exist?
            regex_fmt = r"TExecuteStatementResp.*SemanticException.*Table not found {}"
            regex = regex_fmt.format(re.escape(full_table))
            if re.search(regex, e.args[0]):
                raise exc.NoSuchTableError(full_table)
            elif hasattr(e, "orig") and e.orig:
                regex = r"Table or view not found"
                if re.search(regex, str(e.orig)):
                    raise exc.NoSuchTableError(full_table)
                raise

        else:
            # Hive is stupid: this is what I get from DESCRIBE some_schema.does_not_exist
            regex = r"Table .* does not exist"
            if len(rows) == 1 and re.match(regex, rows[0].col_name):
                raise exc.NoSuchTableError(full_table)
            return rows

    def get_columns(self, connection, table_name, schema=None, **kw):
        # override to get columns properly; the reason is because databricks
        # presents the partition information differently from oss hive
        rows = self._get_table_columns(connection, table_name, schema)
        # Strip whitespace
        rows = [[col.strip() if col else None for col in row] for row in rows]
        # Filter out empty rows and comment
        rows = [row for row in rows if row[0] and row[0] != "# col_name"]
        result = []
        for (col_name, col_type, _comment) in rows:
            # Handle both oss hive and Databricks' hive partition header, respectively
            if col_name in ("# Partition Information", "# Partitioning"):
                break
            # Take out the more detailed type information
            # e.g. 'map<int,int>' -> 'map'
            #      'decimal(10,1)' -> decimal
            col_type = re.search(r"^\w+", col_type).group(0)
            try:
                coltype = _type_map[col_type]
            except KeyError:
                util.warn(
                    "Did not recognize type '%s' of column '%s'" % (col_type, col_name)
                )
                coltype = types.NullType

            result.append(
                {
                    "name": col_name,
                    "type": coltype,
                    "nullable": True,
                    "default": None,
                }
            )
        return result


from sqlalchemy.dialects import registry

registry.register("databricks.connector", __name__, DatabricksDialect.__name__)
