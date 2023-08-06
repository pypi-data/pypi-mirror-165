import pytest
from rick.mixin import Translator
from rick.validator import Validator

validator_case1 = [
    {
        'field1': {
            'required': None,
            'maxlen': 3,
        },
        'field2': {
            'minlen': 4,
        },
        'field3': {
            'required': None,
            'bail': None,
            'numeric': None,
            'len': [2, 4],
        }
    },
    {
        'field1': 'required|maxlen:3',
        'field2': 'minlen:4',
        'field3': 'bail|required|numeric|len:2,4',
    }
]

messages_case1 = {
    'field2': {
        'minlen': 'custom message for field 2'
    },
    'field3': {
        '*': 'custom message for field 3'
    }
}


class ManaManaTranslator(Translator):

    def t(self, text: str):
        return "mana mana"


@pytest.mark.parametrize("data", validator_case1)
def test_validator(data):
    v = Validator(data)

    for field, opts in data.items():
        r = v.field_rules(field)
        if type(opts) is dict:
            assert len(r) == len(opts)

    with pytest.raises(ValueError):
        v.field_rules('non-existing-field')

    values = {}
    # simple test - required
    valid = v.is_valid(values)
    assert valid is False
    errors = v.get_errors()
    assert len(errors) == 2
    for field in ['field1', 'field3']:
        assert field in errors.keys()


@pytest.mark.parametrize("data", validator_case1)
def test_validator_field1(data):
    v = Validator(data)

    values = {
        'field1': 'abcd'  # error maxlen
    }
    valid = v.is_valid(values)
    assert valid is False

    errors = v.get_errors('field1')
    assert len(errors) == 1
    assert 'maxlen' in errors.keys()
    values = {
        'field1': 'abc'  # no error
    }
    assert v.is_valid(values) is False  # field1 is ok, but other fields fail
    errors = v.get_errors('field1')
    assert len(errors) == 0  # no error


@pytest.mark.parametrize("data", validator_case1)
def test_validator_field2(data):
    v = Validator(data)

    values = {
        'field2': 'ab'  # error minlen
    }
    valid = v.is_valid(values)
    assert valid is False

    errors = v.get_errors('field2')
    assert len(errors) == 1
    assert 'minlen' in errors.keys()
    values = {
        'field2': 'abcd'  # no error
    }
    assert v.is_valid(values) is False  # field1 is ok, but other fields fail
    errors = v.get_errors('field2')
    assert len(errors) == 0  # no error


@pytest.mark.parametrize("data", validator_case1)
def test_validator_field3(data):
    v = Validator(data)

    # test bail
    values = {
        'field3': 'a'  # fails 2 validation rules
    }
    valid = v.is_valid(values)
    assert valid is False
    errors = v.get_errors('field3')
    assert len(errors) == 1  # because bail, only 1 rule should appear
    assert 'numeric' in errors.keys()

    # test len
    values = {
        'field3': '1'  # fails 1 validation rule
    }
    valid = v.is_valid(values)
    assert valid is False
    errors = v.get_errors('field3')
    assert len(errors) == 1  # because bail, only 1 rule should appear
    assert 'len' in errors.keys()


@pytest.mark.parametrize("data", validator_case1)
def test_validator_messages(data):
    v = Validator(data, messages_case1)

    # wildcard custom message for field 3
    field3_error = messages_case1['field3']['*']
    values = {
        'field3': 'a'  # fails 2 validation rules
    }
    valid = v.is_valid(values)
    assert valid is False
    errors = v.get_errors('field3')
    assert len(errors) == 1  # because bail, only 1 rule should appear
    assert 'numeric' in errors.keys()
    assert errors['numeric'] == field3_error

    # test len
    values = {
        'field3': '1'  # fails 1 validation rule
    }
    valid = v.is_valid(values)
    assert valid is False
    errors = v.get_errors('field3')
    assert len(errors) == 1  # because bail, only 1 rule should appear
    assert errors['len'] == field3_error

    # custom message for field2
    field2_error = messages_case1['field2']['minlen']
    values = {
        'field2': 'abc'  # fails validation
    }
    valid = v.is_valid(values)
    assert valid is False
    errors = v.get_errors('field2')
    assert len(errors) == 1
    assert 'minlen' in errors.keys()
    assert errors['minlen'] == field2_error


@pytest.mark.parametrize("data", validator_case1)
def test_validator_translation(data):
    v = Validator(data)
    t = ManaManaTranslator()
    values = {}
    assert v.is_valid(values, translator=t) is False
    errors = v.get_errors()
    assert len(errors) == 2
    for field, err_dict in errors.items():
        for validator, error in err_dict.items():
            assert error == "mana mana"
