"""
MS SQL Query Syntax
"""

try:
    # if running from a parent package (python -m app.py ...) i.e. relative import
    from .options import (
        STATEMENT_TYPE_ALT_NAMES, STATEMENT_TYPE_CREATE_TABLE, STATEMENT_TYPE_DELETE_FROM, 
        STATEMENT_TYPE_INSERT_INTO, STATEMENT_TYPE_MERGE, STATEMENT_TYPE_RENAME_COLUMN
    )
except ImportError:
    # running from app folder (python app.py ...)
    from options import (
        STATEMENT_TYPE_ALT_NAMES, STATEMENT_TYPE_CREATE_TABLE, STATEMENT_TYPE_DELETE_FROM, 
        STATEMENT_TYPE_INSERT_INTO, STATEMENT_TYPE_MERGE, STATEMENT_TYPE_RENAME_COLUMN
    )


MS_SQL_TABLE_PREFIX = "dbo."
TAB_SPACE_COUNT = 4


def proper_table_name(name):
    return f"{MS_SQL_TABLE_PREFIX}{name}"


# MS SQL FORMATS

FORMAT_DROP_TABLE_IF_EXISTS = "IF OBJECT_ID('%(tableName)s', 'U') IS NOT NULL DROP TABLE %(tableName)s;"

FORMAT_CREATE_TABLE_LINE_START = "CREATE TABLE %(tableName)s ("
FORMAT_CREATE_TABLE_LINE_COL = "%(sep0)s%(colName)s%(sep1)s%(colType)s%(sep2)s%(constraints)s%(comma)s"
FORMAT_CREATE_TABLE_LINE_PKS = "%(sep0)sPRIMARY KEY (%(PKs)s)"
FORMAT_CREATE_TABLE_LINE_FK = "%(sep0)sFOREIGN KEY (%(FK)s) REFERENCES %(src)s"
FORMAT_CREATE_TABLE_LINE_FK_CONSTR = "%(sep0)s%(constraint)s"
FORMAT_CREATE_TABLE_LINE_END = ");"
FORMAT_CREATE_TABLE_LINE_TRUNC = "TRUNCATE TABLE %(tableName)s;"

FORMAT_INSERT_INTO_LINE_START = "INSERT INTO %(tableName)s VALUES ("
def FORMAT_INSERT_INTO_LINE_COL(sep0, colName, comma): return f"{sep0}%({colName})s{comma}"
FORMAT_INSERT_INTO_LINE_END = ");"

FORMAT_MERGE_LINE_START = "MERGE %(tableName)s AS tgt"
FORMAT_MERGE_LINE_USING = "USING (SELECT"
def FORMAT_MERGE_LINE_COL(sep0, colName, comma): return f"{sep0}%({colName})s {colName}{comma}"
FORMAT_MERGE_LINE_ON = ") AS src ON ("
FORMAT_MERGE_LINE_ON_KEY = "%(sep0)ssrc.%(colName)s = tgt.%(colName)s%(_and)s"
FORMAT_MERGE_LINE_ON_END = ")"
FORMAT_MERGE_LINE_MATCH = "WHEN MATCHED THEN UPDATE SET"
FORMAT_MERGE_LINE_MATCH_REPLACE = "%(sep0)stgt.%(colName)s = src.%(colName)s%(comma)s"
FORMAT_MERGE_LINE_MATCH_ACCUMUL = "%(sep0)stgt.%(colName)s = tgt.%(colName)s+src.%(colName)s%(comma)s"
FORMAT_MERGE_LINE_NMATCH = "WHEN NOT MATCHED THEN INSERT ("
FORMAT_MERGE_LINE_NMATCH_FIELD = "%(sep0)s%(colName)s%(comma)s"
FORMAT_MERGE_LINE_NMATCH_VALUES = ") VALUES ("
def FORMAT_MERGE_LINE_NMATCH_VAL(sep0, colName, comma): return f"{sep0}%({colName})s{comma}"
FORMAT_MERGE_LINE_END = ");"

FORMAT_DELETE_FROM = "DELETE FROM %(tableName)s"
FORMAT_DELETE_FROM_WHERE = "%(sep0)sWHERE %(where)s;"

def FORMAT_RENAME_COLUMN(table): return f"EXEC sp_rename '{table}.%(column)s', %(newName)s;"


# PYTHON FUNCTION FORMATS

FORMAT_PY_FUNC_CREATE_TABLE = f"# {'-'*25}delete{'-'*25}\ncursor, conn = None, None\n" + f"# {'-'*(25*2+len('delete'))}\n" + \
    "def create_table_%(tableLower)s(commit=True):\n" + \
        f"{' '*TAB_SPACE_COUNT}cursor.execute(" + "%(prefix_)s" + \
            STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_CREATE_TABLE]+"_%(tableUpper)s)\n" + \
            f"{' '*TAB_SPACE_COUNT}if commit:\n{' '*(TAB_SPACE_COUNT*2)}conn.commit()"

FORMAT_PY_FUNC_INSERT_UPDATE = f"# {'-'*25}delete{'-'*25}\ncursor, conn = None, None\n" + "%(prefix_)s" + \
    STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_INSERT_INTO] +"_%(tableUpper)s = None\n%(prefix_)s" + \
        STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_MERGE] + "_%(tableUpper)s = None\n" + \
            f"# {'-'*(25*2+len('delete'))}\n" + \
                "def insert_into_%(tableLower)s(values, update_if_exists=False, commit=True):\n" + \
                    f"{' '*TAB_SPACE_COUNT}query = (\n{' '*(TAB_SPACE_COUNT*2)}" + \
                        "%(prefix_)s"+STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_MERGE] + \
                            "_%(tableUpper)s if update_if_exists else %(prefix_)s" + \
                                STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_INSERT_INTO]+"_%(tableUpper)s" + \
                                f"\n{' '*TAB_SPACE_COUNT}) +>?X$;~;^&$ " + "{\n" + "%(fieldLines)s" + f"{' '*TAB_SPACE_COUNT}" + "}\n" + \
                                    f"{' '*TAB_SPACE_COUNT}cursor.execute(query)\n" + \
                                        f"{' '*TAB_SPACE_COUNT}if commit:\n{' '*(TAB_SPACE_COUNT*2)}conn.commit()"
FORMAT_PY_FUNC_INSERT_UPDATE_FIELD = f"{' '*(TAB_SPACE_COUNT*2)}" + "\"%(colName)s\":%(sep0)svalues[%(inx)s]%(comma)s\n"

FORMAT_PY_FUNC_DELETE_FROM = f"# {'-'*25}delete{'-'*25}\ncursor, conn = None, None\n" + f"# {'-'*(25*2+len('delete'))}\n" + \
    "def delete_from_%(tableLower)s(id, commit=True):\n" + \
        f"{' '*TAB_SPACE_COUNT}query = "+"%(prefix_)s"+STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_DELETE_FROM] + \
            "_%(tableUpper)s +>?X$;~;^&$ "+"{\"%(column)s\": id}\n" + \
                f"{' '*TAB_SPACE_COUNT}cursor.execute(query)\n" + \
                    f"{' '*TAB_SPACE_COUNT}if commit:\n{' '*(TAB_SPACE_COUNT*2)}conn.commit()"

FORMAT_PY_FUNC_RENAME_COLUMN = f"# {'-'*25}delete{'-'*25}\ncursor, conn = None, None\n" + f"# {'-'*(25*2+len('delete'))}\n" + \
    "def rename_column_%(tableLower)s(column, new_name, commit=True):\n" + \
        f"{' '*TAB_SPACE_COUNT}query = "+"%(prefix_)s"+STATEMENT_TYPE_ALT_NAMES[STATEMENT_TYPE_RENAME_COLUMN] + \
            "_%(tableUpper)s +>?X$;~;^&$ "+"{\n" + \
                f"{' '*(TAB_SPACE_COUNT*2)}"+"\"column\": column,\n"+f"{' '*(TAB_SPACE_COUNT*2)}"+"\"newName\": new_name\n" + \
                f"{' '*TAB_SPACE_COUNT}" + "}\n" + f"{' '*TAB_SPACE_COUNT}cursor.execute(query)\n" + \
                    f"{' '*TAB_SPACE_COUNT}if commit:\n{' '*(TAB_SPACE_COUNT*2)}conn.commit()"
