# 此處處理md檔案來源於資料庫的情形
import base64
import re

from bs4 import BeautifulSoup
import mistune
import Database
from MarkdownToHtml import FindKeyFromValue, MakeMarkdownContainer, ReplaceSrc, image_to_base64    

def MakeJavascriptVar(name, data):
    return 'var ' + name + ' = ' + '"' + data  + '"' + ';\r\n'

def MakeJavascriptQuerySelector(name, target):
    return 'var ' + name + ' = ' + 'document.querySelectorAll(' + '"' + target + '"'  + ');\r\n'

def MakeJavascriptSetSrc(name, base64Img):
    
    return name + '.forEach(function(img) {\n\t\timg.src = ' +  base64Img + ';\n\t' +'});\r\n'
def CatchPic(md_str):
    # 抓取圖片路徑
    markdown_image_re = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(markdown_image_re, md_str)
    pic_path = {}
    for match in matches:
        relatively_path = match[1]
        if relatively_path.find("http://") == -1 and relatively_path.find("https://") == -1:
            if not re.match('[A-Za-z]:/', relatively_path):
                # 從資料庫讀取的md檔案不支持使用相對路徑
                continue
                
            else:
                pic_path[relatively_path] = relatively_path
        else:
            # 網路圖片
            pic_path[relatively_path] = relatively_path
    #print(pic_path)
    return pic_path


def reNamePic(pic_paths:dict, pic_id:dict):
    #將pic_paths內所有圖片重新命名(格式為 Image+序號)
    count = len(pic_id)
    for key in pic_paths.keys():
        #print(key)
        if key not in pic_id:
            pic_id[key] = "Image" + str(count)
            count += 1
    return pic_id

def cleanLineBreaks(md_str):
    
    lines = re.split('[\t ]*\n', md_str)
    new_md_str = ""
    for line in lines:
        if len(line) == 0:
            continue
        new_md_str += line + "\n"
    return new_md_str

def makeScriptContent(pic_base64, pic_id):
   #在html中新增對應變數儲存base64，並動態配置img的src
    scriptContent = ""
    new_pic_base64 = {}
    count = 1
    delete_list = []
    for file_path in pic_id.keys():
        if pic_id.get(file_path) not in pic_base64:
            # 為網路圖片，嘗試進行下載
            base64_code = image_to_base64(file_path)
            if base64_code == -1:
                delete_list.append(file_path)
                count += 1
                continue
            else:
                new_pic_base64[pic_id[file_path]] = base64_code
            scriptContent += MakeJavascriptVar('Base64_Img' + str(count), new_pic_base64[pic_id[file_path]])
        else:
            scriptContent += MakeJavascriptVar('Base64_Img' + str(count), pic_base64[pic_id[file_path]])
        scriptContent += MakeJavascriptQuerySelector('Img' + str(count), '.' + pic_id[file_path])
        scriptContent += MakeJavascriptSetSrc('Img' + str(count), 'Base64_Img' + str(count))
        
        #print(MakeJavascriptSetSrc('Img' + str(count), 'Base64_Img' + str(count)))
        count += 1
    #print(scriptContent)
    for delete_element in delete_list:
        del pic_id[delete_element]
    return scriptContent, new_pic_base64, pic_id

def MdToHtml(md_str, pic_id, pic_base64):
    #md_str = cleanLineBreaks(md_str)
    pic_paths = CatchPic(md_str)
    #print(pic_paths)

    pic_id = reNamePic(pic_paths, pic_id)
    #print(pic_id)
    #在html中新增對應變數儲存base64，並動態配置img的src
    scriptContent, new_pic_base64, pic_id = makeScriptContent(pic_base64, pic_id)
    #print(new_pic_base64)
    #print(pic_id)
    md_str, new_md_to_save = ReplaceSrc(md_str, pic_id)
    #print(md_str)
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



    #print(soup)
    return soup.body.contents, scriptContent, pic_base64, cleanLineBreaks(new_md_to_save), new_pic_base64



def SaveEditMarkdown(md_id, new_md_name, new_md_content):
    pics = Database.GetPictures(md_id)

    # 取得已有的圖片
    pic_id = {}
    pic_base64 = {}
    for pic in pics:
        pic_name, pic_base64_data = pic
        header, base64_body = pic_base64_data.split(",", 1)
        mime_type = header.split(";")[0].split(":")[1]
        format = mime_type.split("/")[-1]
        key = "/img/" + pic_name + "." + format
        pic_id[key] = pic_name
        pic_base64[pic_name] = pic_base64_data

    # md轉html
    md_html, scriptContent, pic_base64, new_md_to_save, new_pic_base64 = MdToHtml(new_md_content, pic_id, pic_base64)
    the_html = MakeMarkdownContainer(md_html, scriptContent, new_md_name)

    # 存入資料庫
    string_bytes = the_html.encode('utf-8')
    base64_bytes = base64.b64encode(string_bytes)

    Database.UpdateMarkdown(md_id, new_md_name, base64_bytes, new_md_to_save)
    Database.UpdatePictures(md_id, pic_base64)
    Database.InsertPictures(md_id, new_pic_base64)
    return 0


if __name__ == '__main__':
    md = """"""
    SaveEditMarkdown("20241220123803", "爬蟲", md)