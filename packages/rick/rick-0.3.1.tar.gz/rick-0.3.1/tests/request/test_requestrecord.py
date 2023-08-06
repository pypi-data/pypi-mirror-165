import pytest
from rick.form import Field
from rick.request import RequestRecord
from rick.mixin import Translator
from rick.filter import Filter
from typing import Any


class RequestRecordSample(RequestRecord):
    name = Field(validators="required|minlen:4|maxlen:8")
    age = Field(validators="required|numeric|between:9,125")
    phone = Field(validators="numeric|minlen:8|maxlen:16")

    def validator_name(self, data, t: Translator):
        # this validator is only run if standard form validation is successful
        if data['name'] == 'dave':
            self.add_error('name', 'Dave is not here, man', t)
            return False
        return True


class DudeFilter(Filter):
    MESSAGE = "Hey Dude"

    def transform(self, src: Any) -> Any:
        return self.MESSAGE


class RequestRecordFilter(RequestRecord):
    name = Field(validators="required|minlen:4|maxlen:8")
    age = Field(validators="required|numeric|between:9,125", filter='int')
    phone = Field(validators="numeric|minlen:8|maxlen:16", filter=DudeFilter)


requestrecord_fixture = {
    'no_error': {'name': 'john', 'age': 32},
    'no_error_2': {'name': 'john', 'age': '32'},
    'no_error_3': {'name': 'sarah', 'age': '14', 'phone': '900400300'},
    'custom_validator': {'name': 'dave', 'age': '17', 'phone': '900320400'},

    'missing_field': {'name': 'john'},
    'minlen_error': {'name': 'j', 'age': 32},
    'maxlen_error': {'name': 'john_connor', 'age': 32},
    'no_numeric_error': {'name': 'john', 'age': 'abc'},
}
requestrecord_result = {
    'no_error': {},
    'no_error_2': {},
    'no_error_3': {},
    'custom_validator': {'name': {'*': 'Dave is not here, man'}},
    'missing_field': {'age': {'required': 'value required'}},
    'minlen_error': {'name': {'minlen': 'minimum allowed length is 4'}},
    'maxlen_error': {'name': {'maxlen': 'maximum allowed length is 8'}},
    'no_numeric_error': {'age': {'between': 'must be between 9 and 125', 'numeric': 'only digits allowed'}},
}

requestrecord_filter_fixture = {
    'no_error': {'name': 'john', 'age': 32},
    'no_error_2': {'name': 'john', 'age': '32'},
    'no_error_3': {'name': 'sarah', 'age': '14', 'phone': '900400300'},
    'missing_field': {'name': 'john'},
    'minlen_error': {'name': 'j', 'age': 32},
    'maxlen_error': {'name': 'john_connor', 'age': 32},
    'no_numeric_error': {'name': 'john', 'age': 'abc'},
}
requestrecord_filter_result = {
    'no_error': {},
    'no_error_2': {},
    'no_error_3': {},
    'missing_field': {'age': {'required': 'value required'}},
    'minlen_error': {'name': {'minlen': 'minimum allowed length is 4'}},
    'maxlen_error': {'name': {'maxlen': 'maximum allowed length is 8'}},
    'no_numeric_error': {'age': {'between': 'must be between 9 and 125', 'numeric': 'only digits allowed'}},
}


@pytest.mark.parametrize("fixture", [(requestrecord_fixture, requestrecord_result)])
def test_requestrecord_validator(fixture):
    form_data = fixture[0]
    errors = fixture[1]
    frm = RequestRecordSample()
    for id, data in form_data.items():
        expected_errors = errors[id]
        assert frm.is_valid(data) == (len(expected_errors) == 0)
        assert frm.get_errors() == expected_errors


def test_requestrecord_misc():
    frm = RequestRecordSample()
    assert frm.is_valid({}) is False
    assert len(frm.get_errors()) > 0
    frm.clear()
    assert len(frm.get_errors()) == 0


@pytest.mark.parametrize("fixture", [(requestrecord_filter_fixture, requestrecord_filter_result)])
def test_requestrecord_filter_1(fixture):
    form_data = fixture[0]
    errors = fixture[1]
    frm = RequestRecordFilter()
    for id, data in form_data.items():
        expected_errors = errors[id]
        assert frm.is_valid(data) == (len(expected_errors) == 0)
        assert frm.get_errors() == expected_errors


def test_requestrecord_filter_2():
    pass
