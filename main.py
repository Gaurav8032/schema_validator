import json
import jsonschema
from jsonschema import validate
import ijson
import datetime

#using jsonschema validate json event file with corresponding schema file object
def validateJson(jsonData,errorFile,schema):
    try:
        validate(instance=jsonData, schema=schema)
    except Exception as err:
        error_arr = str(err).split("\n")
        errorFile.write(error_arr[0] + "input record: {0} \n".format(jsonData))

        return False

    #default condition to return true if no exception happens.
    return True

#reading schema at a time from schema.json files assumin git cannot fit into memory
def getSchema(fileobject,identifier):
    schema = ""
    fileobject.seek(0, 0)
    for line in fileobject:
        schema_arr = line.split("|")
        if schema_arr[0].upper() == identifier.upper():
            schema = schema_arr[1]

    if schema == "":
        raise ValueError('schema not found')
    else:
        return schema

#iterate through all relevant events in events data file and compare schema of iterative object with files schema.
def itrRecords(record, errorfile,schemaFileObj):
    jsonData = json.loads(record)
    schema= ""

    #Mapping for lookup
    if record.find("rollnumber") != -1:
        schema = json.loads(getSchema(schemaFileObj,"studentSchema"))
        print("processing student record")
        print(schema)

    if record.find("empname") != -1 :
        schema = json.loads(getSchema(schemaFileObj,"empSchema"))
        print("processing emp record")
        print(schema)

    # validate it
    isValid = validateJson(jsonData ,errorfile ,schema)
    if isValid:
        print("Given JSON data is Valid")
    else:
        print("Given JSON data is InValid")

def process():

    #Error file location
    errorFile = open('/Users/igaurav/Documents/personal/taxfix/error/log','a+')
    errorFile.write("logging for the run {} \n".format(str(datetime.datetime.now())))
    errorFile.write("============================================================== \n")

    #Schema Location
    schemaFileObj = open("/Users/igaurav/Documents/personal/taxfix/schema/schema.csv")

    #Loop through input file
    with open("/Users/igaurav/Documents/personal/taxfix/input/input.json") as file:
        for line in file:
            if line != "":
                itrRecords(line,errorFile,schemaFileObj)

    errorFile.write("============================================================== \n")

if __name__ == "__main__":
    process()
