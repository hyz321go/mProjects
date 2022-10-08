import comtypes.client
from pdf2docx import Converter
import PySimpleGUI as sg


# pdf与word互转功能
# https://www.bilibili.com/read/cv15666579?spm_id_from=333.999.0.0 这里有把python打包成exe文件的教程，在干净的虚拟环境中打包使exe体积尽量小
# 其中的word转pdf功能需要操作系统安装有office软件才能配合使用，否则会闪退报错！！！！！！


# pdf转word
def pdf2word(file_path):
    file_name = file_path.split('.')[0]
    doc_file = f'{file_name}.docx'
    p2w = Converter(file_path)
    p2w.convert(doc_file, start=0, end=None)    # start=0表示从第一页开始转化
    p2w.close()
    return doc_file


# word转pdf
def word2pdf(file_path):
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = 0
    file_name = file_path.split('.')[0]
    pdf_file = f'{file_name}.pdf'
    w2p = word.Documents.Open(file_path)
    w2p.SaveAs(pdf_file, FileFormat=17)
    w2p.Close()
    return pdf_file


def main():
    # 选择主题
    sg.theme('LightBlue5')

    layout = [
        [sg.Text('PDF与WORD转换小工具', font=('微软雅黑', 12)),
         sg.Text('', key='filename', size=(50, 1), font=('微软雅黑', 10), text_color='blue')],
        [sg.Output(size=(80, 10), font=('微软雅黑', 10))],
        [sg.FilesBrowse('选择文件', key='file', target='filename'), sg.Button('pdf转word'), sg.Button('word转pdf'),
         sg.Button('退出')]]
    # 创建窗口
    window = sg.Window("Python工具", layout, font=("微软雅黑", 15), default_element_size=(50, 1))
    # 事件循环
    while True:
        # 窗口的读取，有两个返回值（1.事件；2.值）
        event, values = window.read()
        print(event, values)

        if event == 'pdf转word':
            if values['file'] and values['file'].split('.')[1] == 'pdf':
                pdf_filename = pdf2word(values['file'])
                print('pdf文件个数 ：1')
                print('\n' + '转换成功！' + '\n')
                print('文件保存位置：', pdf_filename)
            elif values['file'] and values['file'].split(';')[0].split('.')[1] == 'pdf':
                print('pdf文件个数 ：{}'.format(len(values['file'].split(';'))))
                for f in values['file'].split(';'):
                    pdf_filename = pdf2word(f)
                    print('\n' + '转换成功！' + '\n')
                    print('文件保存位置：', pdf_filename)
            else:
                print('请选择pdf格式的文件哦!')
        if event == 'word转pdf':
            if values['file'] and values['file'].split('.')[1] == 'docx':
                word_filename = word2pdf(values['file'])
                print('word文件个数 ：1')
                print('\n' + '转换成功！' + '\n')
                print('文件保存位置：', word_filename)
            elif values['file'] and values['file'].split(';')[0].split('.')[1] == 'docx':
                print('word文件个数 ：{}'.format(len(values['file'].split(';'))))
                for f in values['file'].split(';'):
                    filename = word2pdf(f)
                    print('\n' + '转换成功！' + '\n')
                    print('文件保存位置：', filename)
            else:
                print('请选择docx格式的文件哦!')
        if event in (None, '退出'):
            break

    window.close()


if __name__ == '__main__':
    main()
