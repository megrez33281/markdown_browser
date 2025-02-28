from flask import Flask, render_template, request, redirect
from MarkdownToHtml import MarkdownTohtml, get_name
from ReadFile import ChooseMd
from datetime import datetime
import base64
import Database
from AddNoteCard import AddElement


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def intinal():
    Database.InitialDatabase()
    return AddElement(r'./templates/home.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return AddElement(r'./templates/home.html')


@app.route("/readfile", methods=['POST'])
def readfile():
    print("request method", request.method)
    if request.method == 'POST':
        path = ChooseMd()
        if path == 0:
            #若沒有選擇檔案，則重新定向
            return redirect('/home') #重定向到主頁
        
        #若選擇了md file，則將其轉為html file、存入資料庫後，導向該md file的頁面
        md_id = datetime.now().strftime('%Y%m%d%H%M%S')
        the_html = MarkdownTohtml(path)
        file_name = get_name(path).replace(".md", "")
        string_bytes = the_html.encode('utf-8')
        base64_bytes = base64.b64encode(string_bytes)
        Database.InsertMarkdown(md_id, file_name, base64_bytes)
        #print("File name = ", file_name)
        #print("Now md_id = ", md_id)
        return redirect('/mdfile/' + md_id)



@app.route("/deletefile", methods=['POST'])
def DeleteFile():
    html_id = request.form.get('filename')
    Database.DeleteHtml(html_id)
    return redirect('/home') #重定向到主頁


@app.route('/mdfile/<md_id>', methods=['GET'])
def queryDataMessageByName(md_id):
    print("md_id : ", md_id)
    assert md_id != None
    html_name, html_content = Database.GetHtml(md_id)
    if html_name == '' and html_content == '':
        #在沒有成功讀取的情況下重定向回主頁
        return redirect('/home')
    decoded_bytes = base64.b64decode(html_content)
    # 將 bytes 轉回原始的字符串
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string


if __name__ == '__main__':
    app.debug = True
    app.run()  