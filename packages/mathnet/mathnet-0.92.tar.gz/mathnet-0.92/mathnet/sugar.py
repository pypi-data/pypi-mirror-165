from PyPDF2 import PdfFileReader, PdfFileWriter
def len_pdf(input_pdf,):
    '''
    param file_name:待操作的pdf文件名
    '''
    input_file = PdfFileReader(input_pdf, strict=False)
    return input_file.getNumPages()
def split_pdf(input_pdf, pages=None, output_pdf=None, merge=False):
    '''
    param file_name:待分割的pdf文件名
    param start_page: 执行分割的开始页数
    param end_page: 执行分割的结束位页数
    param output_pdf: 保存切割后的文件名
    '''
    # 读取待分割的pdf文件
#     input_file = PdfFileReader(open(file_name, 'rb'))   # there are some bugs...by wjx:2022-8-29
    page_number=len_pdf(input_pdf)
    if pages==None:
        pages=[i for i in range(page_number)]
    elif str(pages)[0] not in ['[', '(','{']:
        pages=[pages]
    else:
        True
    input_file = PdfFileReader(input_pdf, strict=False)
    if output_pdf==None:
        output_pdf=input_pdf.split('\\')[-1].split('.')[0]
    if merge==False:
        for i in pages:
            output = PdfFileWriter()
            output.addPage(input_file.getPage(i))
            output.write(open(output_pdf+'_'+str(i)+'.pdf', 'wb'))
    else:
        output = PdfFileWriter()
        for i in pages:
            output.addPage(input_file.getPage(i))
        output.write(open(output_pdf+'_merge.pdf', 'wb'))
def merge_pdf(merge_list, output_pdf=None):
    """
    merge_list: 需要合并的pdf列表
    output_pdf：合并之后的pdf名
    """
    if output_pdf==None:
        output_pdf='_merge.pdf'
    # 实例一个 PDF文件编写器
    output = PdfFileWriter()
    for ml in merge_list:
#         pdf_input = PdfFileReader(open(ml, 'rb'))    # there are some bugs...by wjx:2022-8-29
        pdf_input = PdfFileReader(ml, strict=False)
        page_count = pdf_input.getNumPages()
        for i in range(page_count):
            output.addPage(pdf_input.getPage(i))
    output.write(open(output_pdf, 'wb'))