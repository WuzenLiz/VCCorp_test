#json function
def json_get_data():
    with open(json_File) as outData:
        jData = json.loads(outData)
        return jData
        
def json_get_data_WK(keyword):
    result_table = []
    with open(json_File) as outData:
        jData = json.loads(outData)
        for key in jData.key():
            for value in jData[key]:
                if keyword in value:
                    result_table.append(list(filter(lambda d:d['id']==jData['id'].value(),jData)))
    return result_table

def json_add_data(name="",sex="",DoB="",Class=""):
    #anycodehere
    return 
