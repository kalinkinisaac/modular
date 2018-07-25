class TypesSupported(object):

    supported = {int, float}

    @classmethod
    def types_support(cls, func):
        def wrapped(*args):

            new_args = []
            for arg in args:
                if type(arg) in cls.supported:
                    new_args.append(cls(arg))
                else:
                    new_args.append(arg)
            return func(*new_args)

        return wrapped


