from PyPDF2 import PdfFileReader, PdfFileWriter
def len_pdf(input_pdf,):
    '''
    param input_pdf: 待操作的pdf文件名
    '''
    input_file = PdfFileReader(input_pdf, strict=False)
    return input_file.getNumPages()
def split_pdf(input_pdf, pages=None, output_file=None, merge=False):
    '''
    param input_pdf: 待分割的pdf文件名
    param pages: 执行分割的页数, 支持整型，列表，元组，序列，集合等类型
    param output_file: 新建文件夹用于保存操作后的pdf，缺省时为"当前目录//_pdf"
    param merge: 是否将分割后的pdf合并保存
    '''
    # 读取待分割的pdf文件
#     input_file = PdfFileReader(open(file_name, 'rb'))   # there are some bugs...by wjx:2022-8-29
    page_number=len_pdf(input_pdf)
    if pages==None:
        pages=range(page_number)
    elif type(pages) not in [list, tuple, set, range]:
        pages=[pages]
    else:
        raise Exception("Please give a right type for parameter pages!")
    input_file = PdfFileReader(input_pdf, strict=False)
    
    # 拆分/合并的文件存放在新建的文件夹里
    if output_file==None:
        output_file=os.path.join(os.path.dirname(input_pdf), '_pdf')   # 新建文件夹
    else:
        output_file=os.path.join(os.path.dirname(input_pdf), output_file) # 新建文件夹
    os.makedirs(output_file, exist_ok=1)
    
    output = PdfFileWriter()
    for i in pages:
        output_i = PdfFileWriter()
        output_i.addPage(input_file.getPage(i))
        output_i.write(open(output_file+'\\'+str(i)+'.pdf', 'wb'))
        output.addPage(input_file.getPage(i))
    if merge==True:
        output.write(open(output_file+'\\merge.pdf', 'wb'))
def merge_pdf(input_pdfs, output_file=None,):
    """
    input_pdfs: 需要合并的pdf列表
    output_file：新建文件夹用于保存操作后的pdf，缺省时为"当前目录//_pdf"
    """
    # 拆分/合并的文件存放在新建的文件夹里
    if output_file==None:
        output_file=os.path.join(os.path.dirname(input_pdfs[0]), '_pdf')   # 新建文件夹
    else:
        output_file=os.path.join(os.path.dirname(input_pdfs[0]), output_file) # 新建文件夹
    os.makedirs(output_file, exist_ok=1)  
    
    # 实例一个 PDF文件编写器
    output = PdfFileWriter()
    for input_pdfs_i in input_pdfs:
#         pdf_input = PdfFileReader(open(ml, 'rb'))    # there are some bugs...by wjx:2022-8-29
        pdf_input = PdfFileReader(input_pdfs_i, strict=False)
        page_count = pdf_input.getNumPages()
        for i in range(page_count):
            output.addPage(pdf_input.getPage(i))
    output.write(open(output_file+'\\merge.pdf', 'wb'))