from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from collections import OrderedDict

# define function for extracting text from PDF

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text
    

pdf = r"C:\Users\user\Desktop\Scripts\SRR_ROUTE_LIST Monday.pdf" #source data
b = convert(pdf) # run function

# write source data text to file

f = open(r"C:\Users\user\Desktop\Scripts\Output\results.txt", 'w') 

f.write(b)

f.close()

f = open(r"C:\Users\user\Desktop\Scripts\Output\results.txt", 'r')

# create list from source data

lines = []

for i in f.readlines():
    lines.append(i)

keys = map(lambda s: s.strip(), lines) #gets rid of escapes \n 

valList = OrderedDict() #keeps route and acoount order in dictionary

for k in keys:
    if len(k) > 0: # prevents empty characters from being added to values
        if k[0].isdigit() and k[-1].isalpha() and ' ' not in k and k not in valList.keys(): #looks for route numbers in format ###A not currently in route list
            valList[k] = []
        try:
            if int(k) > 100000: #finds accoutn numbers
                try:
                    valList[valList.keys()[-1]].append(k)
                except ValueError:
                    valList[valList.keys()[-1]] = k
        except ValueError:
            continue

# make final output text file to be imported into excel

f = open(r"C:\Users\user\Desktop\Scripts\Output\accts_by_rts.txt", 'w')

for k in valList.items():
    f.writelines(str(k))

f.close()












