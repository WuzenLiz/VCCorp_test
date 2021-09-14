from datetime import datetime
from uuid import uuid4

from marshmallow.decorators import post_load
from marshmallow.utils import EXCLUDE
from model.Student import Student
from marshmallow import fields, Schema
from dateutil.parser import parse

def Date_fields_format(obj):
        Oj = parse(obj).date()
        return datetime.strptime(str(Oj), '%Y-%m-%d').strftime('%d/%m/%Y')

class StudentSchema(Schema):
    id = fields.UUID(dump_only=True)
    Name = fields.Str(required=True)
    Sex = fields.Str()
    Dob = fields.Str()
    Class = fields.Str()
  

    @post_load
    def CreateStudent(self, data, **kwargs):
        data['Dob'] = Date_fields_format(data['Dob'])
        if data['id'] is not None:
            return Student(**data)
        else:
            id_ = uuid4().int
            return Student(id=id_,**data)

    class Meta:
        model = Student
        type_ = 'people'
        strict = True
        unknown = EXCLUDE
        
