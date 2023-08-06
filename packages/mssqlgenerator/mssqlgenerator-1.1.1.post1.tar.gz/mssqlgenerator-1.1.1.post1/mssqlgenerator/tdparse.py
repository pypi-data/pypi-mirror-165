"""
Table Descriptor parser functions
"""

from functools import cmp_to_key

try:
    # if running from a parent package (python -m app.py ...) i.e. relative import
    from .options import (
        CONSTRAINT_PRIMARY_KEY,
        DEFAULT_COL_MERGE_TYPE,
        OPTIONS_COL_MERGE_TYPE,
        OPTIONS_COL_RELATION_UPDEL,
        COL_MERGE_TYPE_SKIP
    )
except ImportError:
    # running from app folder (python app.py ...)
    from options import (
        CONSTRAINT_PRIMARY_KEY,
        DEFAULT_COL_MERGE_TYPE,
        OPTIONS_COL_MERGE_TYPE,
        OPTIONS_COL_RELATION_UPDEL,
        COL_MERGE_TYPE_SKIP
    )


def custom_compare_keys(a, b):
    # assuming a, b is either Type int or str
    a = a[0]
    b = b[0]
    try:
        a = int(a)
    except ValueError:
        a_is_int = False
    else:
        a_is_int = True
    try:
        b = int(b)
    except ValueError:
        if a_is_int:
            # a is a number but b is not
            return -1
        # a is a number but b is not
        return man_cmp(a.lower(), b.lower())
    else:
        if a_is_int:
            # a and b both are numbers
            return man_cmp(a, b)
        # a is not a number but b is
        return 1


def man_cmp(a, b):
    return (a > b) - (a < b) 


def parse_table_descriptor_all(td):
    """Returns [success(bool), message(str), parsed_fields(array)]"""
    
    # observations
    count_fields = 0
    count_keys = 0
    max_len_field_name = 0
    max_len_field_type = 0
    count_fks = 0
    # fields to parse
    table_name = None
    dependent_tables = []
    # ordered by key
    field_names = []
    field_types = []
    field_constraints = []
    field_merge_types = []
    # fk entries
    relation_fields = []
    relation_sources = []
    relation_constraints = []
    # merge related
    merge_on_fields = []
    non_merge_on_fields = []
    non_merge_on_fields_merge_types = []
    # key and non-key fields
    key_fields = []
    non_key_fields = []
    # obtain table name (required)
    table_name = td.get('name', None)
    if (not table_name) or (type(table_name) != str):
        return False, f"table name invalid or not provided", []
    table_name = table_name.strip()
    # obtain dependent table names (optional)
    dependent_tables = td.get('dependents', [])
    if dependent_tables:
        for inx, name in enumerate(dependent_tables):
            try:
                dependent_tables[inx] = str(name)
            except (ValueError, TypeError):
                return False, f"bad argument in field 'dependents'", []
    # obtain merge_on fields (required for merge)
    merge_on = td.get('merge_on', [])
    if merge_on:
        for inx, merge_name in enumerate(merge_on):
            try:
                merge_on[inx] = str(merge_name)
            except (ValueError, TypeError):
                return False, f"bad argument in field 'merge_on'", []
    # obtain field names & params (required at least one)
    fields = td.get('fields', [])
    if not fields:
        return False, f"table 'fields' not provided", []
    # sort the fields by key
    fields = sorted(fields.items(), key=cmp_to_key(custom_compare_keys))
    for inx, field in fields:
        # obtain field name (required)
        field_name = field.get('name', None)
        if (not field_name) or (type(field_name) != str):
            return False, f"column name not provided for field with key '{inx}'", []
        field_name = field_name.strip()
        field_names.append(field_name)
        # observe count_fields
        count_fields += 1
        # observe max_len_field_name
        len_field_name = len(field_name)
        if len_field_name > max_len_field_name:
            max_len_field_name = len_field_name
        # obtain field type (required)
        field_type = field.get('type', None)
        if (not field_type) or (type(field_type) != str):
            return False, f"column type not provided for field with key '{inx}' ({field_name})", []
        field_type = field_type.strip().upper()
        # obtain field type args (required)
        type_args = field.get('type_args', None)
        if type_args:
            for inx, arg in enumerate(type_args):
                try:
                    arg = str(arg)
                    type_args[inx] = arg.strip().upper()
                except (ValueError, TypeError):
                    return False, f"bad field type arguments for field with key '{inx}' ({field_name})", []
            field_type += f"({','.join(type_args)})"
        field_type = field_type.strip().upper()
        field_types.append(field_type)
        # observe max_len_field_type
        len_field_type = len(field_type)
        if len_field_type > max_len_field_type:
            max_len_field_type = len_field_type       
        # check for constraints
        constraints = []
        is_key = field.get('key', None)
        if is_key:
            # CONSTRAINT_PRIMARY_KEY (if is_key) will always be the first constraint
            constraints.append(CONSTRAINT_PRIMARY_KEY)
            key_fields.append(field_name)
            # observe count_keys
            count_keys += 1
        else:
            non_key_fields.append(field_name)
        # obtain additional constraints
        constraint_list = field.get('constraints', None)
        if constraint_list:
            for inx, arg in enumerate(constraint_list):
                try:
                    arg = str(arg)
                    constraint_list[inx] = arg.strip().upper()
                except (ValueError, TypeError):
                    return False, f"bad constraint value for field with key '{inx}' ({field_name})", []
            constraints += constraint_list
        field_constraints.append(constraints)
        # obtain field merge_type (optional)
        merge_type = field.get('merge_type', None)
        if not merge_type:
            merge_type = DEFAULT_COL_MERGE_TYPE
        elif type(merge_type) == str:
            merge_type = merge_type.strip().upper()
            if merge_type not in OPTIONS_COL_MERGE_TYPE:
                return False, f"bad merge_type argument for field with key '{inx}' ({field_name})", []
        else:
            return False, f"bad merge_type argument for field with key '{inx}' ({field_name})", []
        field_merge_types.append(merge_type)
        # check if field is in merge_on
        if field_name in merge_on:
            merge_on_fields.append(field_name)
        elif merge_type != COL_MERGE_TYPE_SKIP:
            non_merge_on_fields.append(field_name)
            non_merge_on_fields_merge_types.append(merge_type)
        # obtain relation fields
        relation = field.get('relation', None)
        if relation:
            rel_enforce = relation.get('enforce', True)
            if rel_enforce:
                # observe count_fks
                count_fks += 1
                #  obtain relation table and column
                rel_table = relation.get('table', None)
                if (not rel_table) or (type(rel_table) != str):
                    return False, f"relation table name invalid or not provided\
                        for field with key '{inx}' ({field_name})", []
                rel_table = rel_table.strip()
                rel_col = relation.get('column', None)
                if (not rel_col) or (type(rel_col) != str):
                    return False, f"relation column name invalid or not provided\
                        for field with key '{inx}' ({field_name})", []
                rel_col = rel_col.strip()
                relation_source = f"{rel_table}({rel_col})"
                relation_sources.append(relation_source)
                relation_fields.append(field_name)
                # obtain relation constraints
                rel_constraints = []
                rel_on_delete = relation.get('on_delete', None)
                if rel_on_delete:
                    if type(rel_on_delete) == str:
                        rel_on_delete = rel_on_delete.strip().upper()
                        if rel_on_delete not in OPTIONS_COL_RELATION_UPDEL:
                            return False, f"invalide value of relation on_delete constraint \
                                for field with key '{inx}' ({field_name})", []
                        else:
                            rel_constraints.append(f"ON DELETE {rel_on_delete}")
                    else:
                        return False, f"invalid value of relation on_delete constraint \
                            for field with key '{inx}' ({field_name})", []
                rel_on_update = relation.get('on_update', None)
                if rel_on_update:
                    if type(rel_on_update) == str:
                        rel_on_update = rel_on_update.strip().upper()
                        if rel_on_update not in OPTIONS_COL_RELATION_UPDEL:
                            return False, f"invalide value of relation on_update constraint \
                                for field with key '{inx}' ({field_name})", []
                        else:
                            rel_constraints.append(f"ON UPDATE {rel_on_update}")
                    else:
                        return False, f"invalid value of relation on_update constraint \
                            for field with key '{inx}' ({field_name})", []
                relation_constraints.append(rel_constraints)

    return True, 'parsed successfully', [
        table_name, dependent_tables, field_names, field_types, field_constraints, 
        field_merge_types, relation_fields, relation_sources, relation_constraints,
        count_fields, count_keys, max_len_field_name, max_len_field_type, count_fks,
        key_fields, non_key_fields, merge_on_fields, non_merge_on_fields,
        non_merge_on_fields_merge_types
    ]


def parse_table_descriptor_table_name(td):
    """Returns [success(bool), message(str), table_name(str)]"""
    
    table_name = td.get('name', None)
    if (not table_name) or (type(table_name) != str):
        return False, f"table name invalid or not provided", []
    table_name = table_name.strip()
    
    return True, 'parsed successfully', table_name


def parse_table_descriptor_table_name_fields(td):
    """Returns [success(bool), message(str), parsed_fields(array)]"""
    
    # observations
    count_fields = 0
    max_len_field_name = 0
    # fields to parse
    table_name = None
    # ordered by key
    field_names = []
    # obtain table name (required)
    table_name = td.get('name', None)
    if (not table_name) or (type(table_name) != str):
        return False, f"table name invalid or not provided", []
    table_name = table_name.strip()
    # obtain field names & params (required at least one)
    fields = td.get('fields', None)
    if not fields:
        return False, f"table 'fields' not provided", []
    # sort the fields by key
    fields = sorted(fields.items(), key=cmp_to_key(custom_compare_keys))
    for inx, field in fields:
        # obtain field name (required)
        field_name = field.get('name', None)
        if (not field_name) or (type(field_name) != str):
            return False, f"column name not provided for field with key '{inx}'", []
        field_name = field_name.strip()
        field_names.append(field_name)
        # observe count_fields
        count_fields += 1
        # observe max_len_field_name
        len_field_name = len(field_name)
        if len_field_name > max_len_field_name:
            max_len_field_name = len_field_name

    return True, 'parsed successfully', [
        table_name, field_names, count_fields, max_len_field_name,
    ]
