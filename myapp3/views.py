import json
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from django.db import connection
import pandas as pd



def uploadexhibit(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM states" )
        states = [ dict(zip([col[0] for col in cursor.description], row)) 
            for row in cursor.fetchall()  ] 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM company_naics" )
        comp = [ dict(zip([col[0] for col in cursor.description], row)) 
            for row in cursor.fetchall()  ] 
    return render(request, 'myapp3/uploadexhibit.html', {'heading':'Upload Exhibits file','states':states , 'comp':comp}) 


def uploadexhibitfile(request):
    try:
        upfile= request.FILES['file']
        root ='uploads'
        path = os.path.realpath(os.path.join(root,str(upfile.name)))
        fileexists = False
        if not fileexists:
            filstg = FileSystemStorage()
            upldfl = filstg.save(path,upfile)
            upldfl_url = filstg.url(upldfl)
        return render(request,'message.html',{'msg':'File uplaoded'})
    except Exception as err:
        return render(request,'message.html',{'msg':'File not uplaoded'})
    

def exhibitlist(request):
    root = 'uploads'
    file = 'ca initial rate manual.xlsx'
    #file = 'CA Farmers Rating Factors.xlsx'
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
    return render(request,'myapp3/exhibit.html',{ 'title':file.strip('xlsx'),'heading':shtname})

def openexhibit(request):
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
