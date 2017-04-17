# -*- coding:utf-8 -*-


class Item(dict):
    __doc__ = '''
    A class which explains the data structure of the data spider gotten
    '''

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        for k in [i for i in self.__class__.__dict__.keys() if i not in dir(Item)]:
            value = self.__class__.__dict__[k]
            if not isinstance(value, Item.Field):
                raise RuntimeError('unknown type %s, not Item.Field' % type(value))
            self[k] = value

    class Field(object):
        pass
