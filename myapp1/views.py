from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import tabula, os
import pandas as pd

def home(request):
    return render(request, 'base.html')

def extractpdf(request):
    if True:
        root = 'uploads'
        filingpdf = request.FILES['filingpdf']
        filepath = os.path.join(root,str(filingpdf.name))
        fs = FileSystemStorage()
        filename = fs.save(filepath, filingpdf)
        pages = request.POST['prange']
        df = tabula.read_pdf(filepath, pages=pages,multiple_tables=False)
        # outpath = 'myapp1/downloads/RateFiling - equity.csv'
        # tabula.convert_into(filepath, outpath, output_format="csv", pages=pages)
        uppath=os.path.join(os.getcwd(), 'uploads')
        for f in os.listdir(uppath):
            os.remove(os.path.join(root, f))
        outpath = os.path.join(os.getcwd(), 'downloads')
        os.chdir(outpath)
        for i in range(len(df)):
            df[i].to_excel('table_' + str(i) + '.xlsx')
        return render(request, 'myapp1/base.html')

def combineexcls(request):
    outpath = os.path.join(os.getcwd(), 'downloads')
    os.chdir(outpath)
    url = os.getcwd()

    files = os.listdir(url)
    df_dict = {}
    for f in files:
        if f.endswith('.xlsx'):
            excel = pd.ExcelFile(f)
            sheets = excel.sheet_names
            for s in sheets:
                df = excel.parse(s)
                df_name = df['Item'][0]
                df_dict[df_name] = df

    with pd.ExcelWriter('output.xlsx') as writer:
        for k in df_dict.keys():
            df_dict[k].to_excel(writer, sheet_name=k, index=False)
