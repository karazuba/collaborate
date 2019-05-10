class CurrentValueDefault:
    key = None

    def __init__(self, *args, **kwargs):
        assert self.key, 'Key must be set.'

    def set_context(self, serializer_field):
        self.value = serializer_field.context[self.key]

    def __call__(self):
        return self.value

    def __repr__(self):
        return f'{self.__class__.__name__}()'