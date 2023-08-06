import json
import yaml
import csv
import xlrd

def getFromJson(jsonFilePath):
    return json.load(open(jsonFilePath,'r'))

def getFromYaml(yamlFilePath):
    with open(yamlFilePath,'r') as f:
        return list(yaml.safe_load_all(f))

def getFromCsv(csvFilePath):
    data=[]
    with open(csvFilePath,'r') as f:
        reader=csv.reader(f)
        next(reader)
        for one in reader:
            data.append(one)
    return data

def getFromExcel(excelFilePath):
    data=[]
    book=xlrd.open_workbook(excelFilePath)
    sheet=book.sheet_by_index(0)
    for one in range(1,sheet.nrows):
        data.append(sheet.row_values(one))
    return data