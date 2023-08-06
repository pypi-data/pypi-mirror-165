import pytest
from rick.form import Field
from rick.request import RequestRecord, SetOf
from rick.mixin import Translator
from rick.filter import Filter
from typing import Any

class TeamMember(RequestRecord):
    name = Field(validators="required|minlen:4|maxlen:8")
    age = Field(validators="required|numeric|between:9,125")

class TeamRecord(RequestRecord):
    title = Field(validators="required|minlen:2|maxlen:32")
    members = SetOf(type=TeamMember, validators="required|list")


    def validator_name(self, data, t: Translator):
        # this validator is only run if standard form validation is successful
        if data['title'] == 'runners':
            self.add_error('title', 'Runners are excluded', t)
            return False
        return True


team_record_values = {
    # invalid values
    'f1': {'title': 'Rugby Team'},
    'f2': {'title': 'Rugby Team', 'members': None},
    'f3': {'title': 'Rugby Team', 'members': [{'name':'abc'}]},
    'f4': {'title': None, 'members': [{'name': 'abcd', 'age': 12}]},
    'f5': {'title': 'Abcdef', 'members': [{'name': 'abcd', 'age': 8}, {'name': 'abcd', 'age': 12}]},

    # valid values
    'v1': {'title': 'Rugby Team', 'members': []},  # is is actually valid, as an empty list can be used as value
    'v2': {'title': 'Rugby Team', 'members': [{'name': 'abcd', 'age': 12}]},

}

team_record_results = {
    'f1': {'members': {'required': 'value required'}},
    'f2': {'members': {'required': 'value required'}},
    'f3': {'members': {'_': {'0': {'age': {'required': 'value required'}, 'name': {'minlen': 'minimum allowed length is 4'}}}}},
    'f4': {'title': {'required': 'value required'}},
    'f5': {'members': {'_': {'0': {'age': {'between': 'must be between 9 and 125'}}}}},
    'v1': {},
    'v2': {}
}

@pytest.mark.parametrize("fixture", [(team_record_values, team_record_results)])
def test_teamRecord_validator(fixture):
    fixture_values = fixture[0]
    fixture_results = fixture[1]

    for version, data in fixture_values.items():
        frm = TeamRecord()
        assert frm.is_valid(data) == (len(fixture_results[version]) == 0)
        assert frm.get_errors() == fixture_results[version]

