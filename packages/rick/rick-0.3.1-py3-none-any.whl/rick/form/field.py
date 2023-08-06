from rick.filter import registry as filter_registry, Filter
import inspect

class Field:
    type = ""
    label = ""
    value = None
    required = False
    readonly = False
    validators = ""
    messages = None
    select = []
    filter = None
    attributes = {}
    options = {}

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        # pass direct read-only mapping to options
        if self.readonly:
            self.options['readonly'] = True

        # pass direct options read-only to main scope
        if 'readonly' in self.options.keys():
            self.readonly = self.options['readonly']

        # fetch/build filter object if any
        if self.filter is not None:
            if isinstance(self.filter, str):
                # self.filter has a filter name, use it to fetch the object
                if not filter_registry.has(self.filter):
                    raise ValueError("Invalid filter name '{}'".format(self.filter))
                self.filter = filter_registry.get(self.filter)
            elif inspect.isclass(self.filter):
                # build object
                self.filter = self.filter()
                if not isinstance(self.filter, Filter):
                    raise ValueError("Field filter must be either a string or a class")

        if self.required:
            # add required validator
            if len(self.validators) == 0:
                self.validators = {'required': None}
            else:
                if isinstance(self.validators, str):
                    self.validators = "required|" + self.validators
                elif isinstance(self.validators, dict):
                    self.validators['required'] = None