#製作加入目前資料庫中已有的markdown的卡片
import Database
from bs4 import BeautifulSoup
import chardet
deleteIcon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAArpJREFUeF7tnNFRwzAMQOMuUnsSyiYwCWUS2IQySZxFas4fvaP9aKpKqkJ4/GLJ6nuR7PQ40sBPKIEUujubDwgIfggQgIBgAsHb0wEICCYQvD0dgIBgAsHb0wEICCYQvD0dgIBzArXW5skk57yoh25RxXTwCPB8/G7IjYAbIHkuQYCQrjcwYTkPX649U9RnAAJ0hzoClD1DBygBasMRoCWojEeAEqA2HAFagsp4BCgBasPDBVx+gLlrqbZgLbC5+EfXr76GImBO6fXfI+CCDx2ge6DU0QhQI9QlQICOnzoaAWqEugQI0PFTR/97AVoA0fHSJ2Bx19BogNr9ETDzVxVzb+IICAaIAARIp9j5eu0T9NfjpfQ4hPkuaF0dRAcEnyEIQMD1v272vodHH+J0AB1AB0i6gGso11CuoZKOmV0bfQhG7z8L6GIBI4gRxAiSds3V9dEjIHp/KUxGECOIESTtGkaQITFGECOIEWTYUPP/aoBvQ89xM4IYQYwgRtAvAtoXOSlMRhAjiBEk7RpexAyJMYIYQYwgw4biRUwKkxHECGIESbvG9RZkWswdyf79i9gdzExDEGCKU54MAXJmphEIMMUpT4YAOTPTCASY4pQnQ4CcmWnEGgSMwzBkUyrLSVZzzsWyHI+vIr6GYdhZFrmgXIec87NlPeYCpmn6aK29WBa5lFwppf12u323rMdcwDiOOaXUu2B1Y6i1VkopddECenHTNL211vaWhUbn8nj6+2cy74ATqFrrms4C89l/4uQm4Fcn9PPgz46j1tprKeXTqwNdBfSix3HcbTabp9Zavxl1EYuXkVLqwOvxePwupRy84LuOIM+i15TbvQPWBMvjsyDAg6ogJwIEsDyWIsCDqiAnAgSwPJYiwIOqICcCBLA8liLAg6ogJwIEsDyWIsCDqiAnAgSwPJb+AIYML44PWikOAAAAAElFTkSuQmCC"
def AddElement(path):
    print("path = ", path)
    html_str = ''
    assert path != ''
    with open(path, 'rb') as file:
        # 偵測檔案編碼
        encoding = chardet.detect(file.read())
    #print("encoding = ", encoding['encoding'])
    with open(path, mode='r', encoding = encoding['encoding'], errors='ignore') as file:
        html_str = file.read()
    soup = BeautifulSoup(html_str, 'html.parser')
    container = soup.find('ul',  {'id':'card-box-ul'})
    datas = Database.GetAllHtml()
    for data in datas:
        #print("data", data)
        li = soup.new_tag('li', **{'class': 'list card'})

        ##製作刪除按鈕
        card_option = soup.new_tag('div', **{'class': 'card-more-options tooltip'})
        delete_img = soup.new_tag('img', **{'class': 'delete-img'})
        delete_img['onclick'] = "this.parentNode.querySelector('.DeleteFile').submit()"
        card_option.append(delete_img)

        delete_span = soup.new_tag('span', **{'class':'tooltiptext'})
        delete_span.string = "刪除"
        card_option.append(delete_span)

        new_form = soup.new_tag('form', action="./deletefile", method="post", **{'class': 'DeleteFile'}, style="display: none;")
        new_textarea = soup.new_tag('textarea')
        new_textarea['name'] = 'filename'
        new_textarea['type'] = "text"
        new_textarea.string = data[0]
        new_form.append(new_textarea)
        card_option.append(new_form)

        li.append(card_option)


        ##製作卡片內容
        card_content = soup.new_tag('div', **{'class': 'card-content'})
        card_content['onclick'] = "location.href = this.querySelector('a').href"
        new_a = soup.new_tag('a', href="./mdfile/" + data[0])
        new_h4 = soup.new_tag('h4', **{'class': 'card-title', 'title': data[1]})
        new_span = soup.new_tag('span', **{'class': 'card-title'})
        new_span.string = data[1]
        new_h4.append(new_span)
        new_a.append(new_h4)
        card_content.append(new_a)

        li.append(card_content)

        container.append(li)
        
    #print(container.prettify())
    
    #放置script
    script_tag = soup.new_tag('script')
    scriptContents = "const DeleteIcon = " + '"' + deleteIcon + '";\n'
    scriptContents += "card_imgs = document.querySelectorAll('.delete-img');\ncard_imgs.forEach(img => img.src = DeleteIcon)"
    script_tag.string = scriptContents
    soup.body.append(script_tag)
    return str(soup)


if __name__ == '__main__':
    AddElement(r'./templates/home.html')