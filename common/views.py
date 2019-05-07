from django.shortcuts import get_object_or_404


class UrlMixin:
    model_class = None
    lookup = None
    attr_name = None
    url_kwarg = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.model_class, 'Model class must be set.'
        if not self.lookup:
            self.lookup = 'pk'
        if not self.attr_name:
            self.attr_name = self.model_class.__name__.lower()
        if not self.url_kwarg:
            self.url_kwarg = f'{self.attr_name}_{self.lookup}'
        setattr(self, self.attr_name, None)

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        if self.url_kwarg in self.kwargs:
            value = self.kwargs[self.url_kwarg]
            setattr(self, self.attr_name,
                    self.model_class.objects.get(**{self.lookup: value}))

        return request

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context[self.attr_name] = getattr(self, self.attr_name)
        return context
