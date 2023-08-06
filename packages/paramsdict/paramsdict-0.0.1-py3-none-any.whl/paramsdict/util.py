'''
Utility functions.
'''
import numpy as np
from pandas import Series
import types

# Source: https://stackoverflow.com/a/54009756/17333120
fn_type = (types.BuiltinFunctionType, types.FunctionType, types.MethodType)

col_type = (np.ndarray, Series)

def _is_subtype(obj, types):
    '''
    Check if obj is a subtype of types. Can also input 'fn' to specify the tuple of (types.BuiltinFunctionType, types.FunctionType, types.MethodType), as these types are not pickleable so multiprocessing fails if they are input directly.

    Arguments:
        obj (object): object to check
        types (type or string, or list of types or strings): types to check

    Returns:
        (bool): if subtype, returns True
    '''
    obj_type = type(obj)
    for type_i in to_list(types):
        if isinstance(type_i, str):
            if type_i == 'fn':
                if _is_subtype(obj, fn_type):
                    return True
            else:
                raise ValueError(f"Only valid string input is 'fn', but input included string {type_i!r}.")
        else:
            if np.issubdtype(obj_type, type_i):
                return True
    return False

def _is_subdtype(col, types):
    '''
    Check if column dtype is a subtype of types. Source: https://stackoverflow.com/a/40312924/17333120.

    Arguments:
        col (NumPy Array or Pandas Series): column to compare
        types (str or list of str): types to check (options are 'float', 'int', 'any', and 'categorical')

    Returns:
        (bool): if subtype, returns True
    '''
    # Get dtype kind of current column
    col_dtype_kind = col.dtype.kind
    # Get typecodes for dtype kinds (typecodes are 'Character', 'Integer', 'UnsignedInteger', 'Float', 'Complex', 'AllInteger', 'AllFloat', 'Datetime', and 'All)
    typecodes = np.typecodes
    # Add Int64 to typecodes
    typecodes['Integer'] += 'Int64'
    typecodes['AllInteger'] += 'Int64'
    typecodes['All'] += 'Int64'
    # Dictionary linking input types to typecodes
    type_str_to_typecodes_dict = {
        'float': ['AllFloat', 'AllInteger'],
        'int': 'AllInteger',
        'any': 'All',
        'categorical': 'All'
    }
    for type_i in to_list(types):
        # Check whether column is valid type
        for sub_type_str_to_typecode in to_list(type_str_to_typecodes_dict[type_i]):
            if col_dtype_kind in typecodes[sub_type_str_to_typecode]:
                return True
    return False

def to_list(data):
    '''
    Convert data into a list if it isn't already. This function is taken from BipartitePandas.

    Arguments:
        data (obj): data to check if it's a list

    Returns:
        (list): data as a list
    '''
    if isinstance(data, (list, tuple, set, frozenset, range, type({}.keys()), type({}.values()), np.ndarray, Series)):
        return list(data)
    return [data]
