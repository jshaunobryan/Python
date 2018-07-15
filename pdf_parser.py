from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter

rsrcmgr =  PDFResourceManager()
pdf = r"C:\Users\user\Desktop\Scripts\SRR_ROUTE_LIST Monday.pdf"
# Open a PDF document.

# Set parameters for analysis.
laparams = LAParams()
# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
for page in PDFPage.create_pages(document):
    output = StringIO()
    converter = TextConverter(rsrcmgr, output, laparams=LAParams())


    print page
    interpreter.process_page(page)
    print output.getvalue()
    # receive the LTPage object for the page.
    #layout = device.get_result()