from flask import Flask, render_template, request, redirect
from MarkdownToHtml import MarkdownTohtml, get_name, ReadMd
from ReadFile import ChooseMd, ChooseSavePath
from datetime import datetime
import base64
import Database
from AddNoteCard import AddElement
import HackMd_Backup
import Export
import EditMarkDown
from SaveEditMarkdown import SaveEditMarkdown


def SaveIntoDatabase(md_path):
    md_id = datetime.now().strftime('%Y%m%d%H%M%S')
    the_html, pic_base64, new_md_to_save = MarkdownTohtml(md_path)
    file_name = get_name(md_path).replace(".md", "")
    string_bytes = the_html.encode('utf-8')
    base64_bytes = base64.b64encode(string_bytes)
    Database.InsertMarkdown(md_id, file_name, base64_bytes, new_md_to_save)
    Database.InsertPictures(md_id, pic_base64)
    return md_id


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def intinal():
    Database.InitialDatabase()
    return AddElement(r'./templates/home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return AddElement(r'./templates/home.html')

@app.route('/downloadMd', methods=['POST'])
def downloadMd():
   if request.method == 'POST':
        #print("request url = ", request.values['download_url'])
        path = ChooseSavePath()
        if path == 0:
            return redirect('/home')  

        md_path = HackMd_Backup.MakeMarkDown(request.values['download_url'], path)
        if md_path == "":
            return redirect('/home') 
        md_id = SaveIntoDatabase(md_path)
        return redirect('/mdfile/' + md_id)


   return redirect('/home')

@app.route("/readfile", methods=['POST'])
def readfile():
    print("request method", request.method)
    if request.method == 'POST':
        path = ChooseMd()
        if path == 0:
            #若沒有選擇檔案，則重新定向
            return redirect('/home') #重定向到主頁
        #若選擇了md file，則將其轉為html file、存入資料庫後，導向該md file的頁面
        md_id = SaveIntoDatabase(path)
        return redirect('/mdfile/' + md_id)
    
#SaveEditMd
@app.route("/SaveEditMd", methods=['POST'])
def SaveEditMd():
    md_name = request.form.get('md_name')
    md_name = md_name.replace("\r", "")
    md_content = request.form.get('md_content')
    md_content = md_content.replace("\r", "")
    md_id = request.form.get('md_id')
    SaveEditMarkdown(md_id, md_name, md_content)
    '''
    with open("./log.txt", mode='w', encoding='utf-8') as file:
        file.write(md_name+"\n")
        file.write(md_content+"\n")
        file.write(md_id)'''
    return redirect('/home')  

@app.route("/editmd", methods=['POST'])
def EditMD():
    md_id = request.form.get('filename')
    edit_html = EditMarkDown.getMarkdownEditor(md_id)
    return str(edit_html)

@app.route("/deletefile", methods=['POST'])
def DeleteFile():
    html_id = request.form.get('filename')
    Database.DeleteHtml(html_id)
    return redirect('/home') #重定向到主頁


@app.route("/exportmd", methods=['POST'])
def exportmd():
    md_id = request.form.get('filename')
    path = ChooseSavePath()
    if path != 0:
        Export.ExportMarkDown(md_id, path)
    return redirect('/home') #重定向到主頁

@app.route('/mdfile/<md_id>', methods=['GET'])
def queryDataMessageByName(md_id):
    print("md_id : ", md_id)
    html_name, html_content = Database.GetHtml(md_id)
    decoded_bytes = base64.b64decode(html_content)
    # 將 bytes 轉回原始的字符串
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string


if __name__ == '__main__':
    app.debug = True
    app.run()  