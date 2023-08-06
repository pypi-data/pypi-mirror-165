from typing import Any, List
from rick.mixin import Translator
from rick.validator import Validator
from deprecated import deprecated
from .field import Field


class FieldRecord:

    def __init__(self, translator: Translator = None):
        self.fields = {}
        self.validator = Validator()
        self.errors = {}
        if translator is None:
            self._translator = Translator()
        else:
            self._translator = translator

    def clear(self):
        """
        Removes all fields and errors
        :return: self
        """
        self.fields = {}
        self.errors = {}
        return self

    def field(self, field_id: str, **kwargs):
        """
        Adds a field to the form

        :param field_id:
        :param kwargs:
        :return: self
        """
        if field_id in self.fields.keys():
            raise RuntimeError("duplicated field id '%s'" % (id,))

        field = Field(**kwargs)
        self.add_field(field_id, field)
        return self

    def add_field(self, id: str, field: Field):
        """
        Add a field object to the internal collection
        :param id: field id
        :param field: field object
        :return: self
        """
        self.fields[id] = field
        if len(field.validators) > 0:
            self.validator.add_field(id, field.validators, field.messages)
        return self

    def is_valid(self, data: dict) -> bool:
        """
        Validate fields
        :param data: dict of values to validate
        :return: True if dict is valid, False otherwise
        """
        self.clear_errors()
        if self.validator.is_valid(data, self._translator):
            # set values for fields
            for field_name, field in self.fields.items():
                # attempt to find a method called validator_<field_id>() in the current object
                method_name = "_".join(['validator', field_name.replace('-', '_')])
                custom_validator = getattr(self, method_name, None)
                # if exists and is method
                if custom_validator and callable(custom_validator):
                    # execute custom validator method
                    if not custom_validator(data, self._translator):
                        # note: errors are added inside the custom validator method
                        return False

                if field_name in data.keys():
                    if field.filter is None:
                        field.value = data[field_name]
                    else:
                        field.value = field.filter.transform(data[field_name])
                else:
                    field.value = None
            return True

        self.errors = self.validator.get_errors()
        return False

    @deprecated('replaced by function get_errors()')
    def error_messages(self) -> dict:
        """
        Get validation error messages
        :return: dict
        """
        return self.errors

    def get_errors(self) -> dict:
        """
        Alias for self.error_messages()
        :return:
        """
        return self.errors

    def clear_errors(self):
        """
        Clean the error collection
        :return: none
        """
        self.errors = {}

    def add_error(self, id: str, error_message: str):
        """
        Adds or overrides a validation error to a field
        if field already have errors, they are removed and replaced by a wildcard error
        :param id field id
        :param error_message error message
        :return self
        """
        if id not in self.fields.keys():
            raise ValueError("invalid field id %s" % (id,))
        if self._translator is not None:
            error_message = self._translator.t(error_message)
        self.errors[id] = {'*': error_message}
        return self

    def get(self, id: str) -> Any:
        """
        Retrieve field value by id
        :param id: field id
        :return: Any
        """
        if id in self.fields.keys():
            return self.fields[id].value
        return None

    def get_data(self) -> dict:
        """
        Retrieve all data as a dict
        :return: dict
        """
        result = {}
        for id, f in self.fields.items():
            result[id] = f.value
        return result

    def set(self, id: str, value: Any):
        """
        Set field value
        :param id: field id
        :param value: value
        :return: self
        """
        if id in self.fields.keys():
            self.fields[id].value = value
        return self

    def get_translator(self) -> Translator:
        return self._translator
