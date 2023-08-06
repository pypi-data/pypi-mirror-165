'''
Class for a user-friendly parameter dictionary.
'''
import copy
from collections.abc import MutableMapping
from numpy import ndarray
from paramsdict.util import _is_subtype, _is_subdtype, to_list

class ParamsDict():
    '''
    Dictionary with fixed keys, and where values must follow given rules. Source: https://stackoverflow.com/a/14816620/17333120.

    Arguments:
        default_dict (dict): default dictionary. Each key should provide a tuple of (default_value, options_type, options, description, constraints), where `default_value` gives the default value associated with the key; `options_type` defines the valid types the value may take; `options` gives the valid values that can associated with the key (this can be a type or a set of particular values); `description` gives a description of the key-value pair; and `constraints` is either None if there are no constraints, or gives a description of the constraints on the value. The specifics on `options_type` follow. If `options_type` is:
            'type' - the key must be associated with a particular type
            'list_of_type' - the value must be a particular type or a list of values of a particular type
            'type_none' - the value can either be None or must be a particular type
            'list_of_type_none': the value can either be None or must be a particular type or a list of values of a particular type
            'type_constrained' - the value must be a particular type and fulfill given constraints
            'type_constrained_none' - the value can either be None or must be a particular type and fulfill given constraints
            'dict_of_type' - the value must be a dictionary where the values are of a particular type
            'dict_of_type_none' - the value can either be None or must be a dictionary where the values are of a particular type
            'array_of_type' - the value must be an array of values of a particular datatype
            'array_of_type_none' - the value can either be None or must be an array of values of a particular datatype
            'array_of_type_constrained' - the value must be an array of values of a particular datatype and fulfill given constraints
            'array_of_type_constrained_none' - the value can either be None or must be an array of values of a particular datatype and fulfill given constraints
            'set' - the value must be a member of a given set of values
            'list_of_set' - the value must be a member of a given set of values or a list of members of a given set of values
            'any' - the value can be anything
    '''

    def __init__(self, default_dict):
        self._paramsdict = ParamsDictBase(default_dict)

    def __call__(self, update_dict=None):
        '''
        Return a copy of self._paramsdict that is updated with update_dict.

        Arguments:
            update_dict (dict or None): dictionary to use when updating self._paramsdict; None is equivalent to {}

        Returns:
            (ParamsDict): a copy of self._paramsdict that is updated with update_dict
        '''
        if update_dict is None:
            return copy.deepcopy(self._paramsdict)
        ret = copy.deepcopy(self._paramsdict)
        ret.update(copy.deepcopy(update_dict))
        return ret

class ParamsDictBase(MutableMapping):
    '''
    Class to ensure that user-generated instances of ParamsDicts are copies of the default instance of the ParamsDict.

    Arguments:
        default_dict (dict): default dictionary. Each key should provide a tuple of (default_value, options_type, options, description, constraints), where `default_value` gives the default value associated with the key; `options_type` defines the valid types the value may take; `options` gives the valid values that can associated with the key (this can be a type or a set of particular values); `description` gives a description of the key-value pair; and `constraints` is either None if there are no constraints, or gives a description of the constraints on the value. The specifics on `options_type` follow. If `options_type` is:
            'type' - the key must be associated with a particular type
            'list_of_type' - the value must be a particular type or a list of values of a particular type
            'type_none' - the value can either be None or must be a particular type
            'list_of_type_none': the value can either be None or must be a particular type or a list of values of a particular type
            'type_constrained' - the value must be a particular type and fulfill given constraints
            'type_constrained_none' - the value can either be None or must be a particular type and fulfill given constraints
            'dict_of_type' - the value must be a dictionary where the values are of a particular type
            'dict_of_type_none' - the value can either be None or must be a dictionary where the values are of a particular type
            'array_of_type' - the value must be an array of values of a particular datatype
            'array_of_type_none' - the value can either be None or must be an array of values of a particular datatype
            'array_of_type_constrained' - the value must be an array of values of a particular datatype and fulfill given constraints
            'array_of_type_constrained_none' - the value can either be None or must be an array of values of a particular datatype and fulfill given constraints
            'set' - the value must be a member of a given set of values
            'list_of_set' - the value must be a member of a given set of values or a list of members of a given set of values
            'any' - the value can be anything
    '''
    def __init__(self, default_dict):
        self.__data = {k: v[0] for k, v in default_dict.items()}
        self.__options = {k: v[1:] for k, v in default_dict.items()}

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def __setitem__(self, k, v):
        if k not in self.__data:
            raise KeyError(f'Cannot add key {k!r}, as ParamsDict keys are fixed.')

        options_type, options, _, constraints = self.__options[k]
        if options_type == 'type':
            if _is_subtype(v, options):
                self.__data[k] = v
            else:
                raise ValueError(f'Value associated with key {k!r} must be of type {options!r}, but input is {v!r} which is of type {type(v)!r}.')
        elif options_type == 'list_of_type':
            for sub_v in to_list(v):
                if not _is_subtype(sub_v, options):
                    raise ValueError(f'Value associated with key {k!r} must be of type {options!r}, but input is {sub_v!r} which is of type {type(sub_v)!r}.')
            self.__data[k] = v
        elif options_type == 'type_none':
            if (v is None) or _is_subtype(v, options):
                self.__data[k] = v
            else:
                raise ValueError(f'Value associated with key {k!r} must be of type {options!r} or None, but input is {v!r} which is of type {type(v)!r}.',)
        elif options_type == 'list_of_type_none':
            if v is None:
                self.__data[k] = []
            for sub_v in to_list(v):
                if not _is_subtype(sub_v, options):
                    raise ValueError(f'Value associated with key {k!r} must be of type {options!r}, but input is {sub_v!r} which is of type {type(sub_v)!r}.')
            self.__data[k] = v
        elif options_type == 'type_constrained':
            if _is_subtype(v, options[0]):
                if options[1](v):
                    self.__data[k] = v
                else:
                    raise ValueError(f'Value associated with key {k!r} must fulfill the constraint(s) {constraints!r}, but input is {v!r} which does not.')
            elif options[1](v):
                raise ValueError(f'Value associated with key {k!r} must be of type {options[0]!r}, but input is {v!r} which is of type {type(v)!r}.')
            else:
                raise ValueError(f'Value associated with key {k!r} must be of type {options[0]!r}, but input is {v!r} which is of type {type(v)!r}. In addition, the input does not fulfill the constraint(s) {constraints!r}.')
        elif options_type == 'type_constrained_none':
            if v is None:
                self.__data[k] = v
            else:
                if _is_subtype(v, options[0]):
                    if options[1](v):
                        self.__data[k] = v
                    else:
                        raise ValueError(f'Value associated with key {k!r} must be None or fulfill the constraint(s) {constraints!r}, but input is {v!r} which does not.')
                elif options[1](v):
                    raise ValueError(f'Value associated with key {k!r} must be of type {options[0]!r} or None, but input is {v!r} which is of type {type(v)!r}.')
                else:
                    raise ValueError(f'Value associated with key {k!r} must be of type {options[0]!r} or None, but input is {v!r} which is of type {type(v)!r}. In addition, the input does not fulfill the constraint(s) {constraints!r}.')
        elif options_type == 'dict_of_type':
            if _is_subtype(v, dict):
                for sub_k, sub_v in v.items():
                    if not _is_subtype(sub_v, options):
                        raise ValueError(f'Value associated with key {k!r} must be a dictionary with values of type {options!r}, but key {sub_k!r} has associated value {sub_v!r}, which has type {type(sub_v)!r}.')
                self.__data[k] = v
            else:
                raise ValueError(f'Value associated with key {k!r} must be an array, but input is {v!r} which is of type {type(v)!r}.')
        elif options_type == 'dict_of_type_none':
            if v is None:
                self.__data[k] = v
            else:
                if _is_subtype(v, dict):
                    for sub_k, sub_v in v.items():
                        if not _is_subtype(sub_v, options):
                            raise ValueError(f'Value associated with key {k!r} must be a dictionary with values of type {options!r}, but key {sub_k!r} has associated value {sub_v!r}, which has type {type(sub_v)!r}.')
                    self.__data[k] = v
                else:
                    raise ValueError(f'Value associated with key {k!r} must be an array, but input is {v!r} which is of type {type(v)!r}.')
        elif options_type == 'array_of_type':
            if _is_subtype(v, ndarray):
                if _is_subdtype(v, options):
                    self.__data[k] = v
                else:
                    raise ValueError(f'Value associated with key {k!r} must be an array of datatype {options!r}, but input is {v!r} which has datatype {v.dtype!r}.')
            else:
                raise ValueError(f'Value associated with key {k!r} must be an array, but input is {v!r} which is of type {type(v)!r}.')
        elif options_type == 'array_of_type_none':
            if v is None:
                self.__data[k] = v
            else:
                if _is_subtype(v, ndarray):
                    if _is_subdtype(v, options):
                        self.__data[k] = v
                    else:
                        raise ValueError(f'Value associated with key {k!r} must be None or an array of datatype {options!r}, but input is {v!r} which has datatype {v.dtype!r}.')
                else:
                    raise ValueError(f'Value associated with key {k!r} must be None or an array, but input is {v!r} which is of type {type(v)!r}.')
        elif options_type == 'array_of_type_constrained':
            if _is_subtype(v, ndarray):
                if _is_subdtype(v, options[0]):
                    if options[1](v):
                        self.__data[k] = v
                    else:
                        raise ValueError(f'Value associated with key {k!r} must fulfill the constraint(s) {constraints!r}, but input is {v!r} which does not.')
                else:
                    raise ValueError(f'Value associated with key {k!r} must be an array of datatype {options!r}, but input is {v!r} which has datatype {v.dtype!r}.')
            elif options[1](v):
                raise ValueError(f'Value associated with key {k!r} must be an array, but input is {v!r} which is of type {type(v)!r}.')
            else:
                raise ValueError(f'Value associated with key {k!r} must be an array, but input is {v!r} which is of type {type(v)!r}. In addition, the input does not fulfill the constraint(s) {constraints!r}.')
        elif options_type == 'array_of_type_constrained_none':
            if v is None:
                self.__data[k] = v
            else:
                if _is_subtype(v, ndarray):
                    if _is_subdtype(v, options[0]):
                        if options[1](v):
                            self.__data[k] = v
                        else:
                            raise ValueError(f'Value associated with key {k!r} must be None or fulfill the constraint(s) {constraints!r}, but input is {v!r} which does not.')
                    else:
                        raise ValueError(f'Value associated with key {k!r} must be None or an array of datatype {options!r}, but input is {v!r} which has datatype {v.dtype!r}.')
                elif options[1](v):
                    raise ValueError(f'Value associated with key {k!r} must be None or an array, but input is {v!r} which is of type {type(v)!r}.')
                else:
                    raise ValueError(f'Value associated with key {k!r} must be None or an array, but input is {v!r} which is of type {type(v)!r}. In addition, the input does not fulfill the constraint(s) {constraints!r}.')
        elif options_type == 'set':
            if v in to_list(options):
                self.__data[k] = v
            else:
                raise ValueError(f'Value associated with key {k!r} must be a subset of {options!r}, but input is {v!r}.')
        elif options_type == 'list_of_set':
            for sub_v in to_list(v):
                if not sub_v in to_list(options):
                    raise ValueError(f'Value associated with key {k!r} must be subset of {options!r}, but input is {sub_v!r}.')
            self.__data[k] = v
        elif options_type == 'any':
            self.__data[k] = v
        else:
            raise NotImplementedError('Invalid options type')

    def __delitem__(self, k):
        raise NotImplementedError

    def __getitem__(self, k):
        return self.__data[k]

    def __contains__(self, k):
        return k in self.__data

    def __repr__(self):
        return dict(self).__repr__()

    def keys(self):
        return self.__data.keys()

    def values(self):
        return self.__data.values()

    def items(self):
        return self.__data.items()

    def copy(self):
        data_copy = self.__data.copy()
        options_copy = self.__options.copy()
        return ParamsDictBase({k: (v, *options_copy[k]) for k, v in data_copy.items()})

    def get_multiple(self, ks):
        '''
        Access the values associated with multiple keys.

        Arguments:
            ks (immutable or list of immutable): key(s) to access values

        Returns
            (tuple): value(s) associated with key(s)
        '''
        return (self[k] for k in to_list(ks))

    def describe(self, k):
        '''
        Describe what a particular key-value pair does.

        Arguments:
            k (immutable): key
        '''
        options_type, options, description, constraints = self.__options[k]
        print(f'KEY: {k!r}')
        print(f'CURRENT VALUE: {self[k]!r}')
        if options_type == 'type':
            print(f'VALID VALUES: one of type {options!r}')
        elif options_type == 'list_of_type':
            print(f'VALID VALUES: one of or list of type {options!r}')
        elif options_type == 'type_none':
            print(f'VALID VALUES: None or one of type {options!r}')
        elif options_type == 'list_of_type_none':
            print(f'VALID VALUES: None or one of or list of type {options!r}')
        elif options_type == 'type_constrained':
            print(f'VALID VALUES: one of type {options[0]!r}')
            print(f'CONSTRAINTS: {constraints!r}')
        elif options_type == 'type_constrained_none':
            print(f'VALID VALUES: None or one of type {options[0]!r}')
            print(f'CONSTRAINTS: {constraints!r}')
        elif options_type == 'dict_of_type':
            print(f'VALID VALUES: dictionary of type {options!r}')
        elif options_type == 'dict_of_type_none':
            print(f'VALID VALUES: None or dictionary of type {options!r}')
        elif options_type == 'array_of_type':
            print(f'VALID VALUES: array of datatype {options!r}')
        elif options_type == 'array_of_type_none':
            print(f'VALID VALUES: None or array of datatype {options!r}')
        elif options_type == 'array_of_type_constrained':
            print(f'VALID VALUES: array of datatype {options!r}')
            print(f'CONSTRAINTS: {constraints!r}')
        elif options_type == 'array_of_type_constrained_none':
            print(f'VALID VALUES: None or array of datatype {options!r}')
            print(f'CONSTRAINTS: {constraints!r}')
        elif options_type == 'set':
            print(f'VALID VALUES: one of {options!r}')
        elif options_type == 'list_of_set':
            print(f'VALID VALUES: one of or list of members of {options!r}')
        elif options_type == 'any':
            print('VALID VALUES: anything')
        print(f'DESCRIPTION: {description}')

    def describe_all(self):
        '''
        Describe all key-value pairs.
        '''
        for k in self.keys():
            self.describe(k)