#!/usr/bin/env python3

# BoBoBo

class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConstError, 'Can not change const % s' % name)
        if not name.isupper():
            raise (self.ConstCaseError,
                   'Const name [%s] is not all uppercase' % name)
        self.__dict__[name] = value
