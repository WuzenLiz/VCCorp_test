from flask import Flask,app,jsonify,request,redirect
import json,os,math
from flask.helpers import url_for
from marshmallow.exceptions import ValidationError
from marshmallow.utils import INCLUDE
from model.Student import Student
from schema.StudenSchema import StudentSchema
from uuid import uuid4


#App define
app = Flask(__name__)
json_File = os.path.abspath('./local_data/data.json')
app_db = any


#Debug
'''
student1 = {
    'Name' :'Julie',
    'Sex' : 'Female',
    'Dob' : "20/01/2014",
    'Class' : "3C"
}
student2 = {
    "Name" : 'Julia',
    "Sex":'Male',
    "Dob": '20/01/2016',
    "Class" : "3C"
}
app_db = []
testSch = StudentSchema()
try:
    test = testSch.load(student1)
    test2 = testSch.load(student2)
    app_db.append(testSch.dump(test))
    app_db.append(testSch.dump(test2)) 
except ValidationError as ex:
    print(ex.messages)
print(app_db)
'''

#Function
def J(*args, **kwargs):
    response = jsonify(*args, **kwargs)
    response.mimetype = "application/vnd.api+json"
    return response

#json function
def json_get_data():
    with open(json_File) as outData:
        jData = json.load(outData)
        return jData

def json_dump_data(Data):
    with open(json_File,'w') as inData:      
        json.dump(Data,inData,indent=4,sort_keys=True,default=str)
        return       
app_db = json_get_data()   

def json_paging(Data,curpage=1,filt_key = None, filt_val = None):
    if filt_key is not None and filt_val is not None:
        Data = list(filter(lambda x:x[str(filt_key).capitalize()] == str(filt_val), Data))
    NumOfPage = math.ceil(len(Data)/10)
    TotalPage = len(Data)//10
    result = []
    if curpage >= 1 and curpage < TotalPage:
        hNext = True
        hPrev = False
        for i in range(curpage*10-1,(curpage+1)*10):
            result.append(Data[i])    
        items = len(result)
    elif curpage == TotalPage:
        hNext = False
        hPrev = True
        for i in range(curpage*10-1,curpage*10+len(Data)%10):
            result.append(Data[i])
        items = len(result)
    else:
        hNext = False
        hPrev = False
        result = [i for i in Data]
        items = len(result)
    
    return {
        'Page_info':{
            'Current Page'  : curpage,
            'Have_Next'     : hNext,
            'Have_Prev'     : hPrev,
            'Pages'         : NumOfPage,
            'Items'         : items,
            'Result':result
        }       
    }


#App route
@app.route('/')
def index():
    return ("We got your request <3\nHere gonna be the usage page") , 200

@app.route('/student',methods=['GET'],strict_slashes=False)
def get_many_Student():
    if request.values.get('id'):
        id = request.values.get('id')
        return redirect(url_for('one_Student_function',id = id))
    if request.values.get('page',default=1) is not None and request.values.get('sex') is not None or request.values.get('class') is not None:
        if request.values.get('sex') is not None:
            data=json_paging(app_db,request.values.get('page',default=1),'Sex',request.values.get('sex'))
            return J(data)
        if request.values.get('class') is not None:
            data=json_paging(app_db,request.values.get('page',default=1),'Class',request.values.get('class'))
            return J(data)
        if request.values.get('sex') is not None and request.values.get('class') is not None:
            data=json_paging(app_db,request.values.get('page',default=1),'Sex',request.values.get('sex'))
            data=json_paging(data,request.values.get('page',default=1),'Class',request.values.get('class'))
            return J(data)
    else:
        data=json_paging(app_db)
        return J(data)

@app.route('/student/<int:id>',methods=['GET','POST','DELETE'])
def one_Student_function(id):
    if str(id) == '' or id is None:
        return redirect('/Student')
    else:
        if request.method == 'GET':
            return J(list(filter(lambda x : x['id'] == str(id),app_db)))
        elif request.method == 'POST':
            based_data_pos = [i for i, j in enumerate(app_db) if j['id'] == str(id)]
            data = request.values
            for key in data:
                if key.capitalize() in app_db[based_data_pos[0]] and key.lower()!= 'id':
                    app_db[based_data_pos[0]][key.capitalize()]=data[key]
            json_dump_data(app_db)
            return J(app_db)
        elif request.method == 'DELETE':
            deldata = [i for i, j in enumerate(app_db) if j['id'] == str(id)]
            app_db.pop(deldata[0])
            json_dump_data(app_db)
            return J(app_db)
        else:
            return 'METHOD NOT ALLOWED', 405


@app.route('/addnew',methods=['POST'])
def add_new_Student():
    schema = StudentSchema(unknown=INCLUDE)
    if request.values:
        input_data = request.values
    elif request.json:
        input_data = request.json
    else:
        return 'Data not supported or nothing provides',400
    try:
        data = schema.load(input_data)
        app_db.append(schema.dump(data))
    except ValidationError as vE:
        return J(vE.messages), 422
    json_dump_data(app_db)
    return J(app_db)    

#YEP
if __name__ == '__main__':
    app.run(host='localhost',debug=True)    