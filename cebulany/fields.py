from flask_restful import marshal
from flask_restful.fields import Raw, MarshallingException


class Dict(Raw):

    def __init__(self, cls_or_instance, **kwargs):
        super(Dict, self).__init__(**kwargs)
        error_msg = ("The type of the dict elements must be a subclass of "
                     "flask_restful.fields.Raw")
        if isinstance(cls_or_instance, type):
            if not issubclass(cls_or_instance, Raw):
                raise MarshallingException(error_msg)
            self.container = cls_or_instance()
        else:
            if not isinstance(cls_or_instance, Raw):
                raise MarshallingException(error_msg)
            self.container = cls_or_instance

    def format(self, value):
        return {
            str(key): self.container.format(obj)
            for key, obj in value.items()
            if key is not None
        }

