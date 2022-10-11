import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
import pandas as pd


def listtables(request):
    root = 'uploads'
    file = 'ca initial rate manual.xlsx'
    filepath = os.path.join(root,Path(file))
    xl = pd.ExcelFile(filepath)
    sheets = xl.sheet_names  
    #xl.parse(sheet_name)    
    return render(request,'myapp3/exhlist.html',{'sheets': sheets , 'title':file,'heading':'Select an Exhibit'})

def openfiling(request,data):
    root = 'uploads'
    shtname = data
    #filepath = request.META['PATH_INFO']
    file = 'ca initial rate manual.xlsx'
    filepath = os.path.join(root,Path(file))
    request.session['fp'] = str(filepath)
    request.session['sn'] = str(shtname)
    return render(request,'myapp3/rates.html',{ 'title':file,'heading':shtname})

def opentable(request):
    try: 
        root = ''
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir('../')
        file =request.session['fp'] 
        sheet =request.session['sn']
        filepath=os.path.join(root, file)
        out =pd.read_excel(filepath, sheet_name= sheet)
        out =out.sort_values (out.columns[0]) 
        out.columns =out.columns.str.replace('','')
        out =out.fillna(" ")
        out =out.dropna()
        json_records=out.reset_index(drop=True).to_json(orient='records') 
        data =json.loads(json_records)
        mylist =[]
        for x in data:
            mylist.append(x)
        cols =mylist[0].keys()
        columns =[] 
        for i in cols:
            columns.append({ 
                'data': i,
                'name': i
        })
        response ={
        "data": mylist, 'columns': columns
        } 
        return HttpResponse(JsonResponse(response)) 
    except Exception as err:
        response = HttpResponse(json.dumps({'Error': err}), content_type='application/json')
        response.status_code =400
        return response
