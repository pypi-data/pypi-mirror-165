"""
Table-Descriptor-parsing and Statement-generating functions.
"""

try:
    # if running from a parent package (python -m app.py ...) i.e. relative import
    from .options import (
        CONSTRAINT_PRIMARY_KEY,
        STATEMENT_TYPE_CREATE_TABLE, 
        STATEMENT_TYPE_INSERT_INTO,
        STATEMENT_TYPE_MERGE,
        STATEMENT_TYPE_DELETE_FROM,
        STATEMENT_TYPE_RENAME_COLUMN,
        COL_MERGE_TYPE_ACCUMLATE,
        FILE_WRITE_MODE_APPEND,
        FILE_WRITE_MODE_OVERWITE,
        OPTIONS_STATEMENT_TYPE,
    )
    from .formats import (
        FORMAT_RENAME_COLUMN,
        proper_table_name,
        FORMAT_DELETE_FROM, FORMAT_DELETE_FROM_WHERE, FORMAT_INSERT_INTO_LINE_COL, FORMAT_INSERT_INTO_LINE_END, 
        FORMAT_INSERT_INTO_LINE_START, FORMAT_MERGE_LINE_COL, FORMAT_MERGE_LINE_END, FORMAT_MERGE_LINE_MATCH, 
        FORMAT_MERGE_LINE_MATCH_ACCUMUL, FORMAT_MERGE_LINE_MATCH_REPLACE, FORMAT_MERGE_LINE_NMATCH, 
        FORMAT_MERGE_LINE_NMATCH_FIELD, FORMAT_MERGE_LINE_NMATCH_VAL, FORMAT_MERGE_LINE_NMATCH_VALUES, 
        FORMAT_MERGE_LINE_ON, FORMAT_MERGE_LINE_ON_END, FORMAT_MERGE_LINE_ON_KEY, FORMAT_MERGE_LINE_START, 
        FORMAT_MERGE_LINE_USING, TAB_SPACE_COUNT, FORMAT_CREATE_TABLE_LINE_COL, FORMAT_CREATE_TABLE_LINE_END, 
        FORMAT_CREATE_TABLE_LINE_FK, FORMAT_CREATE_TABLE_LINE_FK_CONSTR, FORMAT_CREATE_TABLE_LINE_PKS, 
        FORMAT_CREATE_TABLE_LINE_START, FORMAT_CREATE_TABLE_LINE_TRUNC, FORMAT_DROP_TABLE_IF_EXISTS, 
    )
    from .tdparse import (
        parse_table_descriptor_all, 
        parse_table_descriptor_table_name, 
        parse_table_descriptor_table_name_fields
    )
    from .pyfunc import (
        gen_py_db_rename_column_function,
        gen_py_printable_statement,
        gen_py_db_create_table_function,
        gen_py_db_insert_update_function,
        gen_py_db_delete_function,
    )
except ImportError:
    # running from app folder (python app.py ...)
    from options import (
        CONSTRAINT_PRIMARY_KEY,
        STATEMENT_TYPE_CREATE_TABLE, 
        STATEMENT_TYPE_INSERT_INTO,
        STATEMENT_TYPE_MERGE,
        STATEMENT_TYPE_DELETE_FROM,
        STATEMENT_TYPE_RENAME_COLUMN,
        COL_MERGE_TYPE_ACCUMLATE,
        FILE_WRITE_MODE_APPEND,
        FILE_WRITE_MODE_OVERWITE,
        OPTIONS_STATEMENT_TYPE,
    )
    from formats import (
        FORMAT_RENAME_COLUMN,
        proper_table_name,
        FORMAT_DELETE_FROM, FORMAT_DELETE_FROM_WHERE, FORMAT_INSERT_INTO_LINE_COL, FORMAT_INSERT_INTO_LINE_END, 
        FORMAT_INSERT_INTO_LINE_START, FORMAT_MERGE_LINE_COL, FORMAT_MERGE_LINE_END, FORMAT_MERGE_LINE_MATCH, 
        FORMAT_MERGE_LINE_MATCH_ACCUMUL, FORMAT_MERGE_LINE_MATCH_REPLACE, FORMAT_MERGE_LINE_NMATCH, 
        FORMAT_MERGE_LINE_NMATCH_FIELD, FORMAT_MERGE_LINE_NMATCH_VAL, FORMAT_MERGE_LINE_NMATCH_VALUES, 
        FORMAT_MERGE_LINE_ON, FORMAT_MERGE_LINE_ON_END, FORMAT_MERGE_LINE_ON_KEY, FORMAT_MERGE_LINE_START, 
        FORMAT_MERGE_LINE_USING, TAB_SPACE_COUNT, FORMAT_CREATE_TABLE_LINE_COL, FORMAT_CREATE_TABLE_LINE_END, 
        FORMAT_CREATE_TABLE_LINE_FK, FORMAT_CREATE_TABLE_LINE_FK_CONSTR, FORMAT_CREATE_TABLE_LINE_PKS, 
        FORMAT_CREATE_TABLE_LINE_START, FORMAT_CREATE_TABLE_LINE_TRUNC, FORMAT_DROP_TABLE_IF_EXISTS, 
    )
    from tdparse import (
        parse_table_descriptor_all, 
        parse_table_descriptor_table_name, 
        parse_table_descriptor_table_name_fields
    )
    from pyfunc import (
        gen_py_db_rename_column_function,
        gen_py_printable_statement,
        gen_py_db_create_table_function,
        gen_py_db_insert_update_function,
        gen_py_db_delete_function,
    )
 

def gen_printable_statement(lines):
    return '\n'.join(lines)


def generate_statement_create_table(
        table_descriptor=None,
        column_name=None,
        where=None,
        printable=False,
        py_mode=False,
        py_prefix=None,
        py_func=None,
    ):

    statement = ''
    print_statement = ''

    # process table descriptor
    success, message, data = parse_table_descriptor_all(table_descriptor)

    if success:

        table_name, dependent_tables, field_names, field_types, field_constraints,\
            field_merge_types, relation_fields, relation_sources, relation_constraints,\
                count_fields, count_keys, max_len_field_name, max_len_field_type, count_fks,\
                    key_fields, non_key_fields, merge_on_fields, non_merge_on_fields,\
                        non_merge_on_fields_merge_types = data

        lines = []
        printable_lines = []

        def add_line(line, printable_line=None):
            lines.append(line)
            if printable: printable_lines.append(printable_line if printable_line else line)

        def gen_col_line(sep0, name, sep1, field_type, sep2, constraints, inx, count_fields):
            return FORMAT_CREATE_TABLE_LINE_COL % {
                "sep0": sep0,
                "colName": name,
                "sep1": sep1,
                "colType": field_type,
                "sep2": sep2 if constraints else '',
                "constraints": constraints,
                "comma": '' if inx==(count_fields-1) else ','
            }

        if dependent_tables:
            # dependent deletion lines
            for dep in dependent_tables:
                add_line(FORMAT_DROP_TABLE_IF_EXISTS % {'tableName': proper_table_name(dep)})
        # self deletion line
        add_line(FORMAT_DROP_TABLE_IF_EXISTS % {'tableName': proper_table_name(table_name)})
        # statement start line
        add_line(FORMAT_CREATE_TABLE_LINE_START % {'tableName': table_name})
        # field definitions
        comp_pks = []
        sep1_mult_param, sep2_mult_param = None, None
        if printable:
            sep1_mult_param = max_len_field_name + (TAB_SPACE_COUNT - max_len_field_name % TAB_SPACE_COUNT)
            sep2_mult_param = max_len_field_type + (TAB_SPACE_COUNT - max_len_field_type % TAB_SPACE_COUNT)
        for inx, name in enumerate(field_names):
            field_type = field_types[inx]
            constraints = field_constraints[inx]
            # check for composite primary key
            if count_keys > 1 and constraints and constraints[0] == CONSTRAINT_PRIMARY_KEY:
                comp_pks.append(name)
                constraints = constraints[1:]
            constraints = ' '.join(constraints) if constraints else ''
            line = gen_col_line('', name, ' ', field_type, ' ', constraints, inx, count_fields)
            if printable:
                sep0 = ' ' * TAB_SPACE_COUNT
                sep1 = ' ' * (sep1_mult_param - len(name))
                sep2 = ' ' * (sep2_mult_param - len(field_type))
                printable_line = gen_col_line(sep0, name, sep1, field_type, sep2, constraints, inx, count_fields)
                add_line(line, printable_line)
            else:
                add_line(line)

        # composite primary keys (if more than 1)
        if comp_pks:
            # add comma to previous line
            lines[-1] += ','
            # add PK line
            line = FORMAT_CREATE_TABLE_LINE_PKS % {'sep0': '', 'PKs': ', '.join(comp_pks)}
            if printable:
                printable_lines[-1] += ','
                sep0 = ' ' * TAB_SPACE_COUNT
                printable_line = FORMAT_CREATE_TABLE_LINE_PKS % {'sep0': sep0, 'PKs': ', '.join(comp_pks)}
                add_line(line, printable_line)
            else:
                add_line(line)
        # foreign key constraints (if any)
        if relation_fields:
            for inx, rel_name in enumerate(relation_fields):
                # add comma to previous line
                lines[-1] += ','            
                if printable:
                    printable_lines[-1] += ','
                src_name = relation_sources[inx]
                # add FK line
                line = FORMAT_CREATE_TABLE_LINE_FK % {'sep0': '', 'FK': rel_name, 'src': src_name}
                if printable:
                    sep0 = ' ' * TAB_SPACE_COUNT
                    printable_line = FORMAT_CREATE_TABLE_LINE_FK % {'sep0': sep0, 'FK': rel_name, 'src': src_name}
                    add_line(line, printable_line)
                else:
                    add_line(line)
                rel_constr = relation_constraints[inx]
                if rel_constr:
                    for constr in rel_constr:
                         # add FK line
                        line = FORMAT_CREATE_TABLE_LINE_FK_CONSTR % {'sep0': '', 'constraint': constr}
                        if printable:
                            sep0 = ' ' * (TAB_SPACE_COUNT * 2)
                            printable_line = FORMAT_CREATE_TABLE_LINE_FK_CONSTR % {'sep0': sep0, 'constraint': constr}
                            add_line(line, printable_line)
                        else:
                            add_line(line)               

        # ending lines
        add_line(FORMAT_CREATE_TABLE_LINE_END)
        add_line(FORMAT_CREATE_TABLE_LINE_TRUNC % {'tableName': table_name})

        # generate statement text
        statement = ' '.join(lines)

        if printable:
            if py_mode:
                # handle python mode
                print_statement = gen_py_printable_statement(STATEMENT_TYPE_CREATE_TABLE, table_name, printable_lines, py_prefix)
                if py_func:
                    print_statement += f"\n{gen_py_db_create_table_function(table_name, py_prefix)}"
            else:
                print_statement = gen_printable_statement(printable_lines)

    return statement, message, print_statement


def generate_statement_insert_into(
        table_descriptor=None,
        column_name=None,
        where=None,
        printable=False,
        py_mode=False,
        py_prefix=None,
        py_func=None,
    ):
    
    statement = ''
    print_statement = ''

    # process table descriptor
    success, message, data = parse_table_descriptor_table_name_fields(table_descriptor)

    if success:

        table_name, field_names, count_fields, max_len_field_name = data

        lines = []
        printable_lines = []

        def add_line(line, printable_line=None):
            lines.append(line)
            if printable: printable_lines.append(printable_line if printable_line else line)

        # statement start line
        add_line(FORMAT_INSERT_INTO_LINE_START % {'tableName': table_name})

        # field definitions
        for inx, name in enumerate(field_names):
            line = FORMAT_INSERT_INTO_LINE_COL('', name, '' if inx==(count_fields-1) else ',')
            if printable:
                printable_line = FORMAT_INSERT_INTO_LINE_COL(' ' * TAB_SPACE_COUNT, name, '' if inx==(count_fields-1) else ',')
                add_line(line, printable_line)
            else:
                add_line(line)

        # ending line
        add_line(FORMAT_INSERT_INTO_LINE_END)

        # generate statement text
        statement = ' '.join(lines)

        if printable:
            if py_mode:
                # handle python mode
                print_statement = gen_py_printable_statement(STATEMENT_TYPE_INSERT_INTO, table_name, printable_lines, py_prefix)
                if py_func:
                    print_statement += f"\n{gen_py_db_insert_update_function(table_name, field_names, count_fields, max_len_field_name, py_prefix)}"
            else:
                print_statement = gen_printable_statement(printable_lines)

    return statement, message, print_statement


def generate_statement_merge(
        table_descriptor=None,
        column_name=None,
        where=None,
        printable=False,
        py_mode=False,
        py_prefix=None,
        py_func=None,
    ):
    
    statement = ''
    print_statement = ''

    # process table descriptor
    success, message, data = parse_table_descriptor_all(table_descriptor)

    if success:

        table_name, dependent_tables, field_names, field_types, field_constraints,\
            field_merge_types, relation_fields, relation_sources, relation_constraints,\
                count_fields, count_keys, max_len_field_name, max_len_field_type, count_fks,\
                    key_fields, non_key_fields, merge_on_fields, non_merge_on_fields,\
                        non_merge_on_fields_merge_types = data

        lines = []
        printable_lines = []

        def add_line(line, printable_line=None):
            lines.append(line)
            if printable: printable_lines.append(printable_line if printable_line else line)

        # statement start lines
        add_line(FORMAT_MERGE_LINE_START % {'tableName': proper_table_name(table_name)})
        add_line(FORMAT_MERGE_LINE_USING)

        # all fields
        for inx, name in enumerate(field_names):
            line = FORMAT_MERGE_LINE_COL('', name, '' if inx==(count_fields-1) else ',')
            if printable:
                printable_line = FORMAT_MERGE_LINE_COL(' ' * TAB_SPACE_COUNT, name, '' if inx==(count_fields-1) else ',')
                add_line(line, printable_line)
            else:
                add_line(line)

        # on keys
        add_line(FORMAT_MERGE_LINE_ON)
        count_merge_on_fields = len(merge_on_fields)
        for inx, name in enumerate(merge_on_fields):
            line = FORMAT_MERGE_LINE_ON_KEY % {
                "sep0": '',
                "colName": name,
                "_and": '' if inx==(count_merge_on_fields-1) else ' and'
            }
            if printable:
                printable_line = FORMAT_MERGE_LINE_ON_KEY % {
                    "sep0": ' ' * TAB_SPACE_COUNT,
                    "colName": name,
                    "_and": '' if inx==(count_merge_on_fields-1) else ' and'
                }
                add_line(line, printable_line)
            else:
                add_line(line)
        add_line(FORMAT_MERGE_LINE_ON_END)

        # matched
        count_non_merge_on_fields = len(non_merge_on_fields)
        if count_non_merge_on_fields > 0:
            add_line(FORMAT_MERGE_LINE_MATCH)
        for inx, name in enumerate(non_merge_on_fields):
            merge_type = non_merge_on_fields_merge_types[inx]
            line = (FORMAT_MERGE_LINE_MATCH_ACCUMUL if merge_type==COL_MERGE_TYPE_ACCUMLATE else FORMAT_MERGE_LINE_MATCH_REPLACE) % {
                "sep0": '',
                "colName": name,
                "comma": '' if inx==(count_non_merge_on_fields-1) else ','
            }
            if printable:
                printable_line = (FORMAT_MERGE_LINE_MATCH_ACCUMUL if merge_type==COL_MERGE_TYPE_ACCUMLATE else FORMAT_MERGE_LINE_MATCH_REPLACE) % {
                    "sep0": ' ' * TAB_SPACE_COUNT,
                    "colName": name,
                    "comma": '' if inx==(count_non_merge_on_fields-1) else ','
                }
                add_line(line, printable_line)
            else:
                add_line(line)
        
        # not matched
        add_line(FORMAT_MERGE_LINE_NMATCH)
        for inx, name in enumerate(field_names):
            line = FORMAT_MERGE_LINE_NMATCH_FIELD % {
                "sep0": '',
                "colName": name,
                "comma": '' if inx==(count_fields-1) else ','
            }
            if printable:
                printable_line = FORMAT_MERGE_LINE_NMATCH_FIELD % {
                    "sep0": ' ' * TAB_SPACE_COUNT,
                    "colName": name,
                    "comma": '' if inx==(count_fields-1) else ','
                }
                add_line(line, printable_line)
            else:
                add_line(line)
        add_line(FORMAT_MERGE_LINE_NMATCH_VALUES)
        for inx, name in enumerate(field_names):
            line = FORMAT_MERGE_LINE_NMATCH_VAL('', name, '' if inx==(count_fields-1) else ',')
            if printable:
                printable_line = FORMAT_MERGE_LINE_NMATCH_VAL(' ' * TAB_SPACE_COUNT, name, '' if inx==(count_fields-1) else ',')
                add_line(line, printable_line)
            else:
                add_line(line)


        # ending line
        add_line(FORMAT_MERGE_LINE_END)

        # generate statement text
        statement = ' '.join(lines)

        if printable:
            if py_mode:
                # handle python mode
                print_statement = gen_py_printable_statement(STATEMENT_TYPE_MERGE, table_name, printable_lines, py_prefix)
                if py_func:
                    print_statement += f"\n{gen_py_db_insert_update_function(table_name, field_names, count_fields, max_len_field_name, py_prefix)}"
            else:
                print_statement = gen_printable_statement(printable_lines)

    return statement, message, print_statement


def generate_statement_delete_from(
        table_descriptor=None,
        column_name=None,
        where=None,
        printable=False,
        py_mode=False,
        py_prefix=None,
        py_func=None,
    ):
    
    # where = WHERE statement
    
    success = False
    statement = ''
    print_statement = ''

    if where:

        # process table descriptor
        success, message, table_name = parse_table_descriptor_table_name(table_descriptor)
        
        if success:

            lines = []
            printable_lines = []

            def add_line(line, printable_line=None):
                lines.append(line)
                if printable: printable_lines.append(printable_line if printable_line else line)

            # delete from line
            add_line(FORMAT_DELETE_FROM % {'tableName': table_name})
            
            # where line
            line = FORMAT_DELETE_FROM_WHERE % {
                'sep0': '',
                'where': where
            }
            if printable:
                print_line = FORMAT_DELETE_FROM_WHERE % {
                    'sep0': ' ' * TAB_SPACE_COUNT,
                    'where': where
                } 
                add_line(line, print_line)
            else:
                add_line(line)

            # generate statement text
            statement = ' '.join(lines)

            if printable:
                if py_mode:
                    # handle python mode
                    print_statement = gen_py_printable_statement(STATEMENT_TYPE_DELETE_FROM, table_name, printable_lines, py_prefix)
                    if py_func:
                        print_statement += f"\n{gen_py_db_delete_function(table_name, column_name, py_prefix)}"
                else:
                    print_statement = gen_printable_statement(printable_lines)
    else:
        message = "`where` argument is required for DELETE_FROM statement"
    return statement, message, print_statement


def generate_statement_rename_column(
        table_descriptor=None,
        column_name=None,
        where=None,
        printable=False,
        py_mode=False,
        py_prefix=None,
        py_func=None,
    ):
    
    statement = ''
    print_statement = ''

    # process table descriptor
    success, message, table_name = parse_table_descriptor_table_name(table_descriptor)

    if success:

        lines = []
        printable_lines = []

        def add_line(line, printable_line=None):
            lines.append(line)
            if printable: printable_lines.append(printable_line if printable_line else line)

        # rename line
        add_line(FORMAT_RENAME_COLUMN(table_name))

        # generate statement text
        statement = ' '.join(lines)

        if printable:
            if py_mode:
                # handle python mode
                print_statement = gen_py_printable_statement(STATEMENT_TYPE_RENAME_COLUMN, table_name, printable_lines, py_prefix)
                if py_func:
                    print_statement += f"\n{gen_py_db_rename_column_function(table_name, py_prefix)}"
            else:
                print_statement = gen_printable_statement(printable_lines)

    return statement, message, print_statement


STATEMENT_TYPE_TO_GENERATOR = {
    STATEMENT_TYPE_CREATE_TABLE:    generate_statement_create_table,
    STATEMENT_TYPE_INSERT_INTO:     generate_statement_insert_into,
    STATEMENT_TYPE_MERGE:           generate_statement_merge,
    STATEMENT_TYPE_DELETE_FROM:     generate_statement_delete_from,
    STATEMENT_TYPE_RENAME_COLUMN:   generate_statement_rename_column,
}


def ms_sql_statement(
        st_type,
        table_descriptor,
        column_name=None,
        where=None,
        out_file=None,
        out_overwrite=False,
        printable=False,
        py_mode=False,
        py_prefix=None,
        py_func=False,
    ):

    if st_type not in OPTIONS_STATEMENT_TYPE:
        statement = None
        print_statement = None
        message = f"invalid/unsupported statement type: \'{st_type}\' (options: {', '.join(OPTIONS_STATEMENT_TYPE)})"
    else:
        # call parser of relevant statement
        generator_function = STATEMENT_TYPE_TO_GENERATOR[st_type]
        statement, message, print_statement = generator_function(
            table_descriptor=table_descriptor,
            column_name=column_name,
            where=where,
            printable=printable,
            py_mode=py_mode,
            py_prefix=py_prefix,
            py_func=py_func
        )

    # write result to output file
    if out_file and statement:
        write_statement_to_output_file(
            out_file, 
            print_statement if printable else statement, 
            FILE_WRITE_MODE_OVERWITE if out_overwrite else FILE_WRITE_MODE_APPEND, 
            py_mode
        )
    
    return (statement, message, print_statement) if printable else (statement, message)


def get_table_descriptor_from_file(file):
    # check existence of table descriptor file
    import os
    if not os.path.exists(file):
        return False, f'file \'{file}\' does not exist', None
    td = None
    success = False
    message = ''
    with open(file, 'r') as fd: 
        text = fd.read()
        import json
        try:
            td = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            message = 'file \'{file}\' is not a valid json file'
        if td and type(td)==dict:
            success = True
        else:
            message = 'could not decode json from file \'{file}\''
    return success, message, td


def write_statement_to_output_file(out_file, statement, write_mode=FILE_WRITE_MODE_APPEND, py_mode=False):
    if write_mode == FILE_WRITE_MODE_APPEND:
        # check for content in file
        import os
        if os.path.exists(out_file) and os.path.getsize(out_file) != 0:
            statement = f"\n{'#' if py_mode else '--'} {'-'*90}\n{statement}"
    with open(out_file, write_mode) as out:
        out.write(statement)