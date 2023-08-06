from PyPDF2 import PdfFileReader, PdfFileWriter
def len_pdf(file_name,):
    '''
    param file_name:待操作的pdf文件名
    '''
    input_file = PdfFileReader(file_name, strict=False)
    return input_file.getNumPages()
def split_pdf(file_name, start_page, end_page, output_pdf):
    '''
    param file_name:待分割的pdf文件名
    param start_page: 执行分割的开始页数
    param end_page: 执行分割的结束位页数
    param output_pdf: 保存切割后的文件名
    '''
    # 读取待分割的pdf文件
#     input_file = PdfFileReader(open(file_name, 'rb'))   # there are some bugs...by wjx:2022-8-29
    input_file = PdfFileReader(file_name, strict=False)

    # 实例一个 PDF文件编写器
    output_file = PdfFileWriter()
    # 把分割的文件添加在一起
    for i in range(start_page, end_page):
        output_file.addPage(input_file.getPage(i))
    # 将分割的文件输出保存
    with open(output_pdf, 'wb') as f:
        output_file.write(f)
def merge_pdf(merge_list, output_pdf):
    """
    merge_list: 需要合并的pdf列表
    output_pdf：合并之后的pdf名
    """
    # 实例一个 PDF文件编写器
    output = PdfFileWriter()
    for ml in merge_list:
#         pdf_input = PdfFileReader(open(ml, 'rb'))    # there are some bugs...by wjx:2022-8-29
        pdf_input = PdfFileReader(ml, strict=False)
        page_count = pdf_input.getNumPages()
        for i in range(page_count):
            output.addPage(pdf_input.getPage(i))
 
    output.write(open(output_pdf, 'wb'))