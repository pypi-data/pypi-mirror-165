"""
Python function text generator.
"""

try:
    # if running from a parent package (python -m app.py ...) i.e. relative import
    from .formats import (
        FORMAT_PY_FUNC_CREATE_TABLE,
        FORMAT_PY_FUNC_DELETE_FROM,
        FORMAT_PY_FUNC_INSERT_UPDATE,
        FORMAT_PY_FUNC_INSERT_UPDATE_FIELD,
        FORMAT_PY_FUNC_RENAME_COLUMN,
        TAB_SPACE_COUNT,
    )
    from .options import STATEMENT_TYPE_ALT_NAMES
except ImportError:
    # running from app folder (python app.py ...)
    from formats import (
        FORMAT_PY_FUNC_CREATE_TABLE,
        FORMAT_PY_FUNC_DELETE_FROM,
        FORMAT_PY_FUNC_INSERT_UPDATE,
        FORMAT_PY_FUNC_INSERT_UPDATE_FIELD,
        FORMAT_PY_FUNC_RENAME_COLUMN,
        TAB_SPACE_COUNT,
    )
    from options import STATEMENT_TYPE_ALT_NAMES


def gen_py_printable_statement(statement_type, table, lines, prefix=None):
    return f"{(prefix+'_') if prefix else ''}{STATEMENT_TYPE_ALT_NAMES[statement_type]}_{table.upper()} = \"\\\n{' ' * TAB_SPACE_COUNT}" +\
        f"\\\n{' ' * TAB_SPACE_COUNT}".join(lines) + "\\\n\""


def gen_py_db_create_table_function(table, prefix=None):
    return FORMAT_PY_FUNC_CREATE_TABLE % {
        "tableLower": table.lower(),
        "prefix_": f"{(prefix+'_') if prefix else ''}",
        "tableUpper": table.upper(),
    }


def gen_py_db_insert_update_function(table, field_names, count_fields, max_len_field_name, prefix=None):
    field_lines = ''
    extra_char_count = 3
    max_len_field_name += extra_char_count
    for inx, name in enumerate(field_names):
        sep0 = ' ' * (max_len_field_name + (TAB_SPACE_COUNT - max_len_field_name % TAB_SPACE_COUNT) - len(name) - extra_char_count)
        field_lines += FORMAT_PY_FUNC_INSERT_UPDATE_FIELD % {
            "colName": name,
            "sep0": sep0,
            "inx": inx,
            "comma": '' if inx==(count_fields-1) else ','
        }
    return (FORMAT_PY_FUNC_INSERT_UPDATE % {
        "tableLower": table.lower(),
        "prefix_": f"{(prefix+'_') if prefix else ''}",
        "tableUpper": table.upper(),
        "fieldLines": field_lines,
    }).replace("+>?X$;~;^&$", "%")


def gen_py_db_delete_function(table, column, prefix=None):
    return (FORMAT_PY_FUNC_DELETE_FROM % {
        "tableLower": table.lower(),
        "prefix_": f"{(prefix+'_') if prefix else ''}",
        "tableUpper": table.upper(),
        "column": column if column else 'id'
    }).replace("+>?X$;~;^&$", "%")


def gen_py_db_rename_column_function(table, prefix=None):
    return (FORMAT_PY_FUNC_RENAME_COLUMN % {
        "tableLower": table.lower(),
        "prefix_": f"{(prefix+'_') if prefix else ''}",
        "tableUpper": table.upper(),
    }).replace("+>?X$;~;^&$", "%")
