
class Request:
    pass


class MyRequest(Request):
    field1 = Text('validation_rules')
    field2 = Int()
    field3 = Field(TypeClass, 'validation_rules', default=None) # <-- good approach

class MyOtherRequest(Request):
    field2 = SetOf(MyRequest, required=True, empty=False, count=5)





class MyRequest(Request):
    field1 = Field(TypeClass, 'validation_rules', default=None)
    field2 = Field(TypeClass, 'validation_rules', default=None)
    field3 = Field(TypeClass, 'validation_rules', default=None)