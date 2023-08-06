"""
App (CLI) to generate MS SQL statement

Statement types supported:
- CREATE TABLE
- INSERT INTO
- MERGE
- DELETE FROM
- RENAME COLUMN

Arguments description:
- type:                 MS SQL Statement type
- table_descriptor:     json file with info describing the table (see example_td.json)
- column_name:          (optional) column to operate on
- where:                (optional) WHERE condition text

Example commands:
- (sql mode)     python app.py -t CREATE_TABLE -i example_td.json -o out/test.sql
- (python mode)  python app.py -t CREATE_TABLE -i example_td.json -o out/test.py -py -pre SQL
- (show help)    python app.py -h

More example commands:
- python app.py -t CREATE_TABLE -i example_td.json -o out/test.py -py -pre SQL -func
- python app.py -t INSERT_INTO -i example_td.json -o out/test.py -py -pre SQL -func
- python app.py -t MERGE -i example_td.json -o out/test.py -py -pre SQL -func
- python app.py -t DELETE_FROM -i example_td.json -o out/test.py -py -pre SQL -func -where "id = %(id)s" -col id
- python app.py -t RENAME_COLUMN -i example_td.json -o out/test.py -py -pre SQL -func

Can run from either:
- some parent package using "python -m <pkg1>.<pkg2>.<...>.app ..."
- app folder using "python app.py ..."
"""

try:
    # if running from a parent package (python -m app.py ...) i.e. relative import
    from .log import (
        sqllogger, 
        print_to_terminal_OFF, print_to_terminal_ON, 
        write_to_log_OFF, write_to_log_ON
    )
    from .options import (
        OPTIONS_STATEMENT_TYPE,
        OPTIONS_STATEMENT_TYPE_LOWER,
    )
    from .gen import (
        get_table_descriptor_from_file,
        ms_sql_statement,
    )
except ImportError:
    # running from app folder (python app.py ...)
    from log import (
        sqllogger, 
        print_to_terminal_OFF, print_to_terminal_ON, 
        write_to_log_OFF, write_to_log_ON
    )
    from options import (
        OPTIONS_STATEMENT_TYPE,
        OPTIONS_STATEMENT_TYPE_LOWER,
    )
    from gen import (
        get_table_descriptor_from_file,
        ms_sql_statement,
    )


if __name__=='__main__':
    write_to_log_OFF()
    print_to_terminal_ON()
    
    # define cli arguments
    import argparse
    parser = argparse.ArgumentParser(description="MS SQL Statement text generator.")
    parser.add_argument('--type', '-type', '-t', required=True, help='MS SQL statement type',\
        choices=OPTIONS_STATEMENT_TYPE + OPTIONS_STATEMENT_TYPE_LOWER)
    parser.add_argument('--table', '-table', '-td', '-i', required=True, help='table descriptor file (json)')
    parser.add_argument('--output', '-output', '-o', default=None, help='output file name')
    parser.add_argument('--overwrite', '-overwrite', '-ow', action='store_true', default=False, help='output file write mode')
    parser.add_argument('--python', '-python', '-py', action='store_true', default=False, help='enable python mode for output file')
    parser.add_argument('--prefix', '-prefix', '-pre', default=None, help='variable name prefix for python mode')
    parser.add_argument('--pyfunc', '-pyfunc', '-func', action='store_true', default=False,\
        help='generate python function alongside printed statement for executing printed statement')
    parser.add_argument('--column', '--col', '-column', '-col', '-c', default=None,\
        help='column (name) to operate on')
    parser.add_argument('--where', '-where', '-w', default=None,\
        help='WHERE condition text to append to final statement (or oldColumnName in case of RENAME COLUMN statement)')
    
    # parse arguments
    args = parser.parse_args()
    arg_type = args.type.upper()        # required
    arg_td_file = args.table            # required
    arg_out_file = args.output          # optional
    arg_overwrite = args.overwrite      # optional
    arg_py = args.python                # optional
    arg_py_pre = args.prefix            # optional
    arg_py_func = args.pyfunc           # optional
    arg_column = args.column            # optional
    arg_where = args.where              # optional 

    # read table descriptor file (json)
    success, message, td = get_table_descriptor_from_file(arg_td_file)
    if not success:
        sqllogger(message)
        exit()

    # call statement generator
    statement, message, print_statement = ms_sql_statement(
        arg_type,
        table_descriptor=td,
        column_name=arg_column,
        where=arg_where,
        out_file=arg_out_file,
        out_overwrite=arg_overwrite,
        printable=True,
        py_mode=arg_py,
        py_prefix=arg_py_pre,
        py_func=arg_py_func,
    )

    if message:
        sqllogger(message)

    # print statement to terminal
    sqllogger(print_statement)
    print_to_terminal_OFF()
    write_to_log_ON()
