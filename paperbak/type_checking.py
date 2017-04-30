"""In this module is everythng connected with strict type checking."""


def auto_attr_check(cls):
    """Class decorator attribute checker.

    Ensure that specific fields have certain type or None.

    Usage:

    Add attribute params which will be dictionary. Key in dictionary is the name of attribute.
    The value can be several types:
        1) is a tuple with len 2 where first element is a type and second is default value
        2) is a tuple with len 3 where first element is a type and second is default value and
           third is boolen if False attribute can't be None
        3) is False this means attribute is read only
        4) is a tuple with len 2 where first element is False this means attribute is read only and
           second is it's default
        5) is a type this leads to being default value of attribute None

    Defaults from params can be overriden by attribute on base class with same name. See below.

    Read only parametrs can be still set by obj.__<name> variable.

    example:
    >>> @auto_attr_check
    >>> class Test(object):
    >>>     params = {
    >>>         "type_1": (np.uint32, 0),
    >>>         "type_1_def": (np.uint32, 0),
    >>>         "type_2": (bool, False, False),  # None won't be valid value
    >>>         "type_2_ex2": (bool, False, True),  # None will be valid value
    >>>         "type_2_def": (bool, False, False),
    >>>         "type_3": False, # Read only with default None
    >>>         "type_3_def": False, # Read only
    >>>         "type_4": (False, 42),  # Read only with default 42
    >>>         "type_4_def": (False, 21),
    >>>         "type_5": np.uint8,  # Default will be None
    >>>         "type_5_def": bool,
    >>>     }
    >>>     type_1_def = 2
    >>>     type_2_def = True
    >>>     type_3_def = 0x55555555  # set default for type_3
    >>>     type_4_def = False  # set default for type_3
    >>>     type_5_def = False  # set default for type_5_def
    """
    def getter_setter_gen(name, type_, can_be_None=True, read_only=False):
        def getter(self):
            return getattr(self, "__" + name)

        def setter(self, value):
            if read_only:
                raise TypeError("Attribute %s is read only." % name)
            if not can_be_None and value is None:
                raise ValueError("Attribute %s can't be None." % name)
            if not isinstance(value, type_) and value is not None:
                value = type_(value)
            setattr(self, "__" + name, value)
        return property(getter, setter)

    new_dict = dict(cls.__dict__)
    if not hasattr(cls, "params"):
        raise AttributeError("Params dictionary is missing")
    for key, value in cls.params.items():
        if isinstance(value, tuple):
            if isinstance(value[0], type) and len(value) == 2:  # case 1
                val = getter_setter_gen(key, value[0])
                new_dict["__" + key] = value[1] if key not in cls.__dict__ else cls.__dict__[key]
            elif isinstance(value[0], type) and len(value) == 3:  # case 2
                val = getter_setter_gen(key, value[0], value[2])
                new_dict["__" + key] = value[1] if key not in cls.__dict__ else cls.__dict__[key]
            elif value[0] == False and len(value) == 2:  # case 4
                val = getter_setter_gen(key, None, read_only=True)
                new_dict["__" + key] = value[1] if key not in cls.__dict__ else cls.__dict__[key]
            else:
                raise AttributeError("Params improperly configured for key '%s'" % key)
        elif isinstance(value, type):  # case 5
            val = getter_setter_gen(key, value)
            new_dict["__" + key] = None if key not in cls.__dict__ else cls.__dict__[key]
        elif value is False:  # case 3
            val = getter_setter_gen(key, None, read_only=True)
            new_dict["__" + key] = None if key not in cls.__dict__ else cls.__dict__[key]
        else:
            raise AttributeError("Params improperly configured for key '%s'" % key)
        new_dict[key] = val
    new_dict["__params"] = new_dict["params"]
    del new_dict["params"]
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls)(cls.__name__, cls.__bases__, new_dict)
