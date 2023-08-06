import copy
from typing import Any, Union

from rick.mixin import Translator
from rick.validator.rules import registry


class ValidatorState:
    """
    Wrapper for Validator sleep() configuration
    This class should be treated as read-only, as Validator will reference ValidatorState attributes on wakeup()
    """

    def __init__(self, rules: dict, messages: dict):
        self.rules = copy.deepcopy(rules)
        self.messages = copy.deepcopy(messages)


class Validator:
    RULE_BAIL = 'bail'
    RULE_REQUIRED = 'required'

    def __init__(self, rules: dict = None, messages: dict = None):
        """
        Validator constructor
        :param rules: optional field rules dict
        :param messages: optional error messages list
        """
        self._errors = {}
        self._rules = {}
        self._rule_messages = {}
        if not messages:
            messages = {}
        if rules:
            for field_name, rules in rules.items():
                if field_name in messages.keys():
                    self.add_field(field_name, rules, messages[field_name])
                else:
                    self.add_field(field_name, rules)

    def sleep(self) -> ValidatorState:
        """
        Serializes internal configuration
        :return: ValidatorState
        """
        return ValidatorState(self._rules, self._rule_messages)

    def wakeup(self, state: ValidatorState):
        """
        Restores configuration from a previous sleep()
        :param state: saved state
        :return:
        """
        self._errors = {}
        self._rules = state.rules
        self._rule_messages = state.messages

    def _parse_rules(self, field_name: str, field_rules: str) -> dict:
        """
        Parse laravel-style validator chain

        :param field_name: field name
        :param field_rules: rules to parse
        :return: dict with traditional rules
        """
        result = {}
        for token in field_rules.split('|'):
            rule_params = token.split(':')
            rule_name = rule_params.pop(0)
            if len(rule_name) == 0 or len(rule_params) > 1:
                raise ValueError("invalid rule format for field %s" % (field_name,))

            params = rule_params.pop().split(',') if len(rule_params) > 0 else None
            result[rule_name] = params
        return result

    def add_field(self, field_name: str, field_rules: Union[dict, str], rule_messages=None):
        """
        Adds a field to be validated

        field_rules format:
        {
            'rule_name': [options],
            ...
        }
        or laravel-style format:
            'rule|rule:1,2|rule'

        rule_messages format:
        {
            'rule_name': 'message',
            ...
        }

        :param field_name: field name
        :param field_rules: rule dict
        :param rule_messages: optional message dict
        :return: self
        """
        if field_name in self._rules.keys():
            raise ValueError("Validator.add_field(): field '%s' already exists" % field_name)

        # parse laravel-style rules
        if isinstance(field_rules, str):
            field_rules = self._parse_rules(field_name, field_rules)

        # check if rules exist
        for rule_name in field_rules.keys():
            if not registry.has(rule_name):
                raise ValueError("Validator.add_field(): rule '%s' does not exist in registry" % rule_name)

        self._rules[field_name] = field_rules
        if rule_messages:
            self._rule_messages[field_name] = rule_messages
        return self

    def field_names(self):
        """
        Return list of field names
        :return: list
        """
        return list(self._rules.keys())

    def field_rules(self, name: str):
        """
        Get rule list for specified field

        Note: keep in mind, returned dict should *not* be changed

        :param name: field name
        :return: dict
        """
        if name in self._rules.keys():
            return self._rules[name]
        raise ValueError("Validator.field_rules(): field '%s' does not exist" % name)

    def clear(self):
        """
        Clear all validation rules
        :return:
        """
        self._rules = {}
        self._rule_messages = {}

    def reset(self):
        """
        Clear all validation errors
        :return:
        """
        self._errors = {}

    def get_errors(self, field_name=None):
        """
        Get validation errors (either all or for a specific field)

        format for all fields:
        {
          'field_name': {
            'rule': 'message',
            ...
          },
          ...
        }

        format for single field:
        {
            'rule': 'message',
            ...
        }

        :param field_name: optional field name
        :return: dict
        """
        if field_name is None:
            return self._errors
        if field_name in self._errors.keys():
            return self._errors[field_name]
        return {}

    def is_valid(self, fields_values: dict, translator: Translator = None) -> bool:
        """
        Validate a dict of field:values

        :param fields_values: values to validate
        :param translator: optional translator object
        :return: bool
        """
        if translator:
            if not issubclass(type(translator), Translator):
                raise ValueError("translator parameter must extend Translator mixin")

        self.reset()
        for field_name in self._rules.keys():
            value = None
            if field_name in fields_values.keys():
                value = fields_values[field_name]

            field_errors = self.validate_field(field_name, value, translator)

            if len(field_errors.keys()) > 0:
                self._errors[field_name] = field_errors

        return len(self._errors) == 0

    def validate_field(self, field_name: str, value: Any, translator: Translator = None) -> dict:
        """
        Validate a single field, and returns validation errors, if any;
        If validation passes, result is empty dict

        :param field_name: field to validate
        :param value: field value
        :param translator: optional translator object
        :return: dict
        """
        if field_name not in self._rules.keys():
            raise ValueError("Validator.validate_field(): field '%s' not found" % field_name)

        field_rules = self._rules[field_name]
        rule_names = list(field_rules.keys())
        bail = self.RULE_BAIL in rule_names
        required = self.RULE_REQUIRED in rule_names
        result = {}

        # always check if value actually exists first
        if required:
            rule_names.remove(self.RULE_REQUIRED)
        r_name = registry.get(self.RULE_REQUIRED)
        error_msg = self._field_error(field_name, self.RULE_REQUIRED)
        valid, error = r_name.validate(value, error_msg=error_msg, translator=translator)

        # field is either optional and value doesn't exist, or is required and should return error
        if not valid:
            if required:
                result[self.RULE_REQUIRED] = error
            return result

        for r_name in rule_names:
            rule_opts = field_rules[r_name]
            if not isinstance(rule_opts, (list, tuple,)):
                rule_opts = [rule_opts, ]

            rule = registry.get(r_name)
            error_msg = self._field_error(field_name, r_name)
            valid, error = rule.validate(value, options=rule_opts, error_msg=error_msg, translator=translator)
            if not valid:
                result[r_name] = error
                if bail:
                    return result
        return result

    def _field_error(self, field_name: str, rule_name: str) -> Union[str, None]:
        """
        Determine optional field error message, if exists

        :param field_name: field name
        :param rule_name: rule name
        :return: str|None
        """
        if field_name in self._rule_messages.keys():
            rule_messages = self._rule_messages[field_name]
            if '*' in rule_messages.keys():
                return rule_messages['*']
            if rule_name in rule_messages.keys():
                return rule_messages[rule_name]
        return None
