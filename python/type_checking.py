"""In this module is everythng connected with strict typpe checking."""

def auto_attr_check(cls):
    """Class decorator attribute checker.

    Ensure that specific fields have certain type or None.

    Usage:

    Add attribute params which will be dictionary. Key in dictionary is the name of attribute.
    The value is tuple where first element is type and second is default value.

    example:
    >>> class Test(object):
    >>>     params = {
    >>>         "foo": (np.uint32, 0),
    >>>         "data": (bytes, bytes(32)),
    >>>     }
    """
    def getter_setter_gen(name, type_):
        def getter(self):
            return getattr(self, "__" + name)
        def setter(self, value):
            if not isinstance(value, type_) and value is not None:
                value = type_(value)
            setattr(self, "__" + name, value)
        return property(getter, setter)

    new_dict = dict(cls.__dict__)
    for key, value in cls.params.items():
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], type):
            val = getter_setter_gen(key, value[0])
            new_dict["__" + key] = value[1]
        else:
            val = value
        new_dict[key] = val
    new_dict["__params"] = new_dict["params"]
    del new_dict["params"]
    # Creates a new class, using the modified dictionary as the class dict:
    return type(cls)(cls.__name__, cls.__bases__, new_dict)
