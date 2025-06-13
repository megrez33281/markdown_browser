import mistune
from bs4 import BeautifulSoup
import re
import base64
import chardet

import requests

def image_to_base64(image_path):
    # 圖片會被轉成base64的格式內嵌入html中
    print(image_path)
    if image_path.find("http://") == -1 and image_path.find("https://") == -1:
        # 從路徑中抓取圖片格式
        format = GetFormat(image_path)

        #將圖片讀取成base64
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        base64_format = "data:image/" + format + ";base64," + encoded_string
    
    else:
        #抓取網路圖片並轉成Base64
        response = requests.get(image_path)
        if response.status_code == 200:
            # 將圖片儲存為本地檔案
            image_content = response.content
            # 將二進位內容轉換為 Base64 編碼
            base64_code = base64.b64encode(image_content).decode('utf-8')
            base64_format = "data:image/" + 'png' + ";base64," + base64_code

        else:
            print(f"圖片下載失敗")
            return -1
    return base64_format

def MakeMarkdownContainer(contents, scriptContents, title):
    #創建一個 HTML 結構
    soup = BeautifulSoup('', 'html.parser')

    # 設定 <html> 標籤的屬性
    html_tag = soup.new_tag('html', lang='zh')
    soup.append(html_tag)

    # 添加 <head> 標籤及其內容
    head_tag = soup.new_tag('head')
    html_tag.append(head_tag)

    # <meta charset="UTF-8">
    meta_charset = soup.new_tag('meta', charset='UTF-8')
    head_tag.append(meta_charset)

    new_title = soup.new_tag('title')
    new_title.string = title
    head_tag.append(new_title)

    #<link rel="shortcut icon" href="../static/favicon.ico">
    ico_link_stylesheet = soup.new_tag('link', rel='shortcut icon', href='../static/favicon.ico')
    head_tag.append(ico_link_stylesheet)

    # <meta name="viewport" content="width=device-width, initial-scale=1.0">
    meta_viewport = soup.new_tag('meta', content='width=device-width, initial-scale=1.0, name=viewport')
    head_tag.append(meta_viewport)

    # <link rel="stylesheet" href="../static/markdownStyles.css">
    link_stylesheet = soup.new_tag('link', rel='stylesheet', href='../static/markdownStyles.css')
    head_tag.append(link_stylesheet)

    # 添加 <body> 標籤及其內容
    body_tag = soup.new_tag('body')
    html_tag.append(body_tag)

    # <div class="title-region">
    div_title_region = soup.new_tag('div', **{'class': 'title-region'})
    body_tag.append(div_title_region)
    div_title_region['onclick'] = 'location.href = this.querySelector("a").href;'

    # <h1>MarkDown 空間</h1>
    h1_tag = soup.new_tag('p', **{'class': 'title-href'})
    h1_tag.string = "MarkDown 空間"
    div_title_region.append(h1_tag)
    a_tag = soup.new_tag('a', href='../home', **{'class': 'title-href'})
    a_tag.append(h1_tag)
    div_title_region.append(a_tag)

    # <div id="markdown-content scrollable">
    div_markdown_content = soup.new_tag('div', id='markdown-content', **{'class': 'scrollable'})
    body_tag.append(div_markdown_content)

    for element in contents:
        div_markdown_content.append(element)

    #放置script
    script_tag = soup.new_tag('script')
    script_tag.string = scriptContents
    # 將 <script> 標籤添加到 <body> 的結尾
    soup.body.append(script_tag)

    
    return f"<!DOCTYPE html>\n{soup.prettify()}"

def getRoot(path):
    index = 0
    for ch in range(0, len(path)):
        if path[len(path)-ch-1] == '/':
            index = len(path)-ch-1
            break
    return path[:index+1]

def get_name(path):
    index = 0
    for ch in range(0, len(path)):
        if path[len(path)-ch-1] == '/':
            index = len(path)-ch-1
            break
    return path[index+1:]

def CatchPic(md_str, path):
    markdown_image_re = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(markdown_image_re, md_str)
    root_path = getRoot(path)
    pic_path = {}
    for match in matches:
        relatively_path = match[1]
        if relatively_path.find("http://") == -1 and relatively_path.find("https://") == -1:
            if not re.match('[A-Za-z]:/', relatively_path):
                '''if root_path[-1] == "/" and relatively_path[0] == "/":
                    root_path = root_path[:-1]'''
                pic_path[relatively_path] = root_path + relatively_path
                
            else:
                pic_path[relatively_path] = relatively_path
        else:
            # 網路圖片
            pic_path[relatively_path] = relatively_path
    #print(pic_path)
    return pic_path

def MakeJavascriptVar(name, data):
    return 'var ' + name + ' = ' + '"' + data  + '"' + ';\r\n'

def MakeJavascriptQuerySelector(name, target):
    return 'var ' + name + ' = ' + 'document.querySelectorAll(' + '"' + target + '"'  + ');\r\n'

def MakeJavascriptSetSrc(name, base64Img):
    
    return name + '.forEach(function(img) {\n\t\timg.src = ' +  base64Img + ';\n\t' +'});\r\n'

def GetFormat(FileName):

    if FileName.find("http://") != -1 or FileName.find("https://") != -1:
        # 網路圖片暫定為png
        return 'png'
    index = 0
    for i in range(0, len(FileName)):
        if FileName[len(FileName) - 1 - i] == '.':
            index = len(FileName) - 1 - i
            break
    return FileName[index+1:]

def getInnerRoot(line):
    # 從一行md的圖片引入提取其中的路徑
    temp = line.split("(")[-1]
    temp = temp.split(")")[0]
    return temp

def ReplaceSrc(md_str, pic_id:dict):
    md_list = md_str.split('\n')
    #print(md_list)
    new_md = ""
    new_md_to_save = ""
    for line in md_list:
        if re.findall(r'!\[(.*?)\]\((.*?)\)', line) != []:
            new_line = line
            new_line_to_save = line
            
            for key in pic_id.keys():
                if getInnerRoot(line) == key:
                    #print(line)
                    #print("original line", new_line)
                    new_line = new_line.replace(key, pic_id.get(key))
                    format = GetFormat(key)
                    new_line_to_save = new_line_to_save.replace(key, "/img/" + pic_id.get(key) + "." + format)
                    #print("new line", new_line)
            new_md += new_line + "\n"
            new_md_to_save += new_line_to_save + "\n"

        else:
            new_md += line + "\n"
            new_md_to_save += line + "\n"
    #print(new_md)
    return new_md, new_md_to_save

def makeScriptContent(pic_paths, pic_id):
    #在html中新增對應變數儲存base64，並動態配置img的src
    scriptContent = ""
    count = 1
    pic_base64 = {}
    for path in pic_paths.keys():
        file_path = pic_paths.get(path)
        # path為在markdown中寫的路徑
        # file_path為檔案真實路徑
        base64 = image_to_base64(file_path)
        if base64 != -1:
            pic_base64[pic_id[path]] = base64
            scriptContent += MakeJavascriptVar('Base64_Img' + str(count), base64)
            scriptContent += MakeJavascriptQuerySelector('Img' + str(count), '.' + pic_id[path])
            scriptContent += MakeJavascriptSetSrc('Img' + str(count), 'Base64_Img' + str(count))
            #print(MakeJavascriptSetSrc('Img' + str(count), 'Base64_Img' + str(count)))
            count += 1
        else:
            del pic_id[path]
            count += 1

    return scriptContent, pic_base64, pic_id

def reNamePic(pic_paths:dict):
    #將pic_paths內所有圖片重新命名(格式為 Image+序號)
    pic_id = {}
    count = 0
    for key in pic_paths.keys():
        #print(key)
        pic_id[key] = "Image" + str(count)
        count += 1
    return pic_id
        
def FindKeyFromValue(a_dict:dict, value):
    ##此處由於圖片重新命名的值皆不同，故可以直接從值找到key
    #print("Value = ", value)
    for key in a_dict.keys():
        if a_dict[key] == value:
            #print("Value = ", value, "Key = ", key)
            return True
    return False

def MdToHtml(md_str, path):
    pic_paths = CatchPic(md_str, path)
    pic_id = reNamePic(pic_paths)
    #print(pic_paths)
    #print(pic_id)
    #在html中新增對應變數儲存base64，並動態配置img的src
    scriptContent, pic_base64, pic_id = makeScriptContent(pic_paths, pic_id)
    md_str, new_md_to_save = ReplaceSrc(md_str, pic_id)

    #print(new_md_to_save)
    md_transfer = re.sub('[\t ]*\n', '\n', md_str)
    md_transfer = md_transfer.replace("\n", "  \n")
    html = mistune.html(md_transfer)
    soup = BeautifulSoup(html, 'lxml')
    # 找到所有包含 href 屬性的 <a> 標籤
    for a_tag in soup.find_all('a', href=True):
        # 添加 target="_blank" 和 rel="noopener noreferrer"
        a_tag['target'] = '_blank'
        a_tag['rel'] = 'noopener noreferrer'

    for tag in soup.body.find_all(True):  # find_all(True) 找到所有標籤
        # 如果元素已經有 class，則附加新 class；如果沒有，則創建 class
        if 'class' in tag.attrs:
            tag['class'].append('markdown-body')
        else:
            tag['class'] = ['markdown-body']

    #將html中的圖片改為內嵌
    for img in soup.find_all('img'):
        #刪除img中src的圖片存在於pic_paths的src
        #print(img['src'])
        if img.has_attr('src') and FindKeyFromValue(pic_id, img['src']):
            # 新增相同名稱的class
            new_class = img['src']
            #print("Src = ", img['src'], "Pic_ID = ", pic_id[img['src']])
            del img['src'] 
            if img.has_attr('class'):
                # 如果已經有 class，則添加新 class
                img['class'].append(new_class)
            else:
                # 如果沒有 class，則直接設置新 class
                img['class'] = [new_class]

    #print(scriptContent)

    #print(soup)
    return soup.body.contents, scriptContent, pic_base64, new_md_to_save

def ReadMd(path):
    with open(path, 'rb') as file:
        encoding = chardet.detect(file.read())
    
    #print("encoding = ", encoding['encoding'])
    md = ''
    with open(path, mode='r', encoding=encoding['encoding'], errors='ignore') as file:
        md = file.read()
    return md

def MarkdownTohtml(path):
    md = ReadMd(path)
    md_html, scriptContent, pic_base64, new_md_to_save = MdToHtml(md, path)
    title = get_name(path)
    the_html = MakeMarkdownContainer(md_html, scriptContent, title.replace('.md', ''))
    #print(the_html)
    return the_html, pic_base64, new_md_to_save

if __name__ == '__main__':
    path = "C:/Users/apple/Downloads/爬蟲/爬蟲.md"
    #print(generate_html())
    the_html, pic_base64, new_md_to_save = MarkdownTohtml(path)
    {}
