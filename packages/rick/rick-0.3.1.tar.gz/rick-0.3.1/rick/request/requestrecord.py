from typing import Any, List

from rick.mixin import Translator
from rick.validator import Validator
from rick.form import Field
import inspect

import inspect
from rick.form import Field


class SetOf(Field):
    type = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not inspect.isclass(self.type):
            raise ValueError("SetOf(): type is mandatory and must be a class")

        if not issubclass(self.type, RequestRecord):
            raise ValueError("SetOf(): type is mandatory and must inherit RequestRecord")

        # add list validator, if no validators specified
        if len(self.validators) == 0:
            self.validators = {'list': None}


class RequestRecord:
    _errors = {}

    def clear(self):
        """
        :return: self
        """
        self._errors = {}
        return self

    def is_valid(self, data: dict, t: Translator = None) -> bool:
        """
        Validate fields

        Fields are validated in groups:
        - defined fields are validaded first, using specified validators
        - if defined fields pass validation, SetOf fields are validated next
        - if defined fields pass validation, optional custom validator methods are executed next

        Please consider SetOf support experimental

        :param data: dict of values to validate
        :param t: Optional translator mixin
        :return: True if dict is valid, False otherwise
        """
        self._errors = {}
        if t is None:
            t = Translator()
        validator = Validator()
        field_names = []
        set_names = {}
        for field_name in dir(self):
            field = getattr(self, field_name)
            if not field_name.startswith('_') and not callable(field):
                # try to process only attributes
                if isinstance(field, SetOf):
                    set_names[field_name] = []
                elif isinstance(field, Field):
                    field_names.append(field_name)
                else:
                    raise ValueError("is_valid(): invalid class type for field %s" % field_name)
                if len(field.validators) > 0:
                    validator.add_field(field_name, field.validators, field.messages)

        if validator.is_valid(data, t):
            # run set validators, if exist
            if len(set_names) > 0:
                # it may happen set is defined, but field is not required
                for field_name, _ in set_names.items():
                    # it may happen set is defined, but field is not required
                    # required validation, as well as list count is already validated via explicit validators
                    if field_name in data.keys():
                        if type(data[field_name]) not in (tuple, list):
                            self.add_error(field_name, 'invalid data type', t)
                        else:
                            field = getattr(self, field_name, None)
                            idx = 0
                            results = []
                            for item in data[field_name]:
                                rr_obj = field.type()
                                if not rr_obj.is_valid(item, t):
                                    if field_name in self._errors.keys():
                                        if '_' in self._errors[field_name].keys():
                                            self._errors[field_name]['_'][str(idx)] = rr_obj.get_errors()
                                        else:
                                            self._errors[field_name]['_'] = {str(idx): rr_obj.get_errors()}
                                    else:
                                        self._errors[field_name] = {'_': {str(idx): rr_obj.get_errors()}}
                                results.append(rr_obj)
                                idx = idx + 1
                            # override initial values
                            set_names[field_name] = results

            # set values for fields
            for field_name in field_names:
                field = getattr(self, field_name, None)
                # attempt to find a method called validator_<field_id>() in the current object
                method_name = "_".join(['validator', field_name.replace('-', '_')])
                custom_validator = getattr(self, method_name, None)
                # if exists and is method
                if custom_validator and callable(custom_validator):
                    # execute custom validator method
                    if not custom_validator(data, t):
                        # note: errors are added inside the custom validator method
                        return False

                if field_name in set_names.keys():
                    field.value = set_names[field_name]
                elif field_name in data.keys():
                    if field.filter is None:
                        field.value = data[field_name]
                    else:
                        field.value = field.filter.transform(data[field_name])
                else:
                    field.value = None

            return len(self._errors) == 0

        self._errors = validator.get_errors()
        return False

    def get_errors(self) -> dict:
        """
        Get validation errors
        :return:
        """
        return self._errors

    def clear_errors(self):
        """
        Clean the error collection
        :return: none
        """
        self._errors = {}

    def add_error(self, id: str, error_message: str, t: Translator = None):
        """
        Adds or overrides a validation error to a field
        if field already have errors, they are removed and replaced by a wildcard error
        :param id field id
        :param error_message error message
        :param t: optional Translator object
        :return self
        """
        field = getattr(self, id, None)
        if not isinstance(field, Field):
            raise ValueError("invalid field id %s" % (id,))

        if t is not None:
            error_message = t.t(error_message)

        self._errors[id] = {'*': error_message}
        return self

    def get(self, id: str) -> Any:
        """
        Retrieve field value by id
        :param id: field id
        :return: Any
        """
        field = getattr(self, id, None)
        if isinstance(field, Field):
            return field.value
        return None

    def get_data(self) -> dict:
        """
        Retrieve all data as a dict
        :return: dict
        """
        result = {}
        for field_name in dir(self):
            if not field_name.startswith('_'):
                f = getattr(self, field_name, None)
                if isinstance(f, Field):
                    result[field_name] = f.value
        return result

    def set(self, id: str, value: Any):
        """
        Set field value
        :param id: field id
        :param value: value
        :return: self
        """
        field = getattr(self, id, None)
        if isinstance(field, Field):
            field.value = value
        return self
