import pytest
from rick.form import FieldRecord, Field
from rick.mixin import Translator


class FieldRecord_A(FieldRecord):

    def init(self):
        self.field('name', validators="required|minlen:4|maxlen:8") \
            .field('age', validators="required|numeric|between:9,125") \
            .field('phone',validators="numeric|minlen:8|maxlen:16")
        return self

    def validator_name(self, data, t:Translator):
        # this validator is only run if standard form validation is successful
        if data['name'] == 'dave':
            self.add_error('name', 'Dave is not here, man')
            return False
        return True

fieldrecord_simple_fixture = {
    'no_error': {'name': 'john', 'age': 32},
    'no_error_2': {'name': 'john', 'age': '32'},
    'no_error_3': {'name': 'sarah', 'age': '14', 'phone': '900400300'},
    'custom_validator': {'name': 'dave', 'age': '17', 'phone': '900320400'},

    'missing_field': {'name': 'john'},
    'minlen_error': {'name': 'j', 'age': 32},
    'maxlen_error': {'name': 'john_connor', 'age': 32},
    'no_numeric_error': {'name': 'john', 'age': 'abc'},
}
fieldrecord_simple_result = {
    'no_error': {},
    'no_error_2': {},
    'no_error_3': {},
    'custom_validator': {'name': {'*': 'Dave is not here, man'}},
    'missing_field': {'age': {'required': 'value required'}},
    'minlen_error': {'name': {'minlen': 'minimum allowed length is 4'}},
    'maxlen_error': {'name': {'maxlen': 'maximum allowed length is 8'}},
    'no_numeric_error': {'age': {'between': 'must be between 9 and 125', 'numeric': 'only digits allowed'}},
}

@pytest.mark.parametrize("fixture", [(fieldrecord_simple_fixture, fieldrecord_simple_result)])
def test_fieldrecord_validator(fixture):
    form_data = fixture[0]
    errors = fixture[1]
    frm = FieldRecord_A().init()
    for id, data in form_data.items():
        expected_errors = errors[id]
        assert frm.is_valid(data) == (len(expected_errors) == 0)
        assert frm.get_errors() == expected_errors

def test_fieldrecord():
    frm = FieldRecord_A().init()
    assert len(frm.fields) > 0
    frm.clear()
    assert len(frm.fields) == 0
    assert len(frm.errors) == 0

    # set value for existing field
    frm = FieldRecord_A().init()
    frm.set('name', 'abc')
    assert frm.get_data()['name'] == 'abc'

    # set value for non-existing field (should ignore)
    frm = FieldRecord_A().init()
    frm.set('address', 'abc')
    assert 'address' not in frm.fields.keys()
    assert 'address' not in frm.get_data().keys()

