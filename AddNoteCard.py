#製作加入目前資料庫中已有的markdown的卡片
import Database
from bs4 import BeautifulSoup
import chardet
deleteIcon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAArpJREFUeF7tnNFRwzAMQOMuUnsSyiYwCWUS2IQySZxFas4fvaP9aKpKqkJ4/GLJ6nuR7PQ40sBPKIEUujubDwgIfggQgIBgAsHb0wEICCYQvD0dgIBgAsHb0wEICCYQvD0dgIBzArXW5skk57yoh25RxXTwCPB8/G7IjYAbIHkuQYCQrjcwYTkPX649U9RnAAJ0hzoClD1DBygBasMRoCWojEeAEqA2HAFagsp4BCgBasPDBVx+gLlrqbZgLbC5+EfXr76GImBO6fXfI+CCDx2ge6DU0QhQI9QlQICOnzoaAWqEugQI0PFTR/97AVoA0fHSJ2Bx19BogNr9ETDzVxVzb+IICAaIAARIp9j5eu0T9NfjpfQ4hPkuaF0dRAcEnyEIQMD1v272vodHH+J0AB1AB0i6gGso11CuoZKOmV0bfQhG7z8L6GIBI4gRxAiSds3V9dEjIHp/KUxGECOIESTtGkaQITFGECOIEWTYUPP/aoBvQ89xM4IYQYwgRtAvAtoXOSlMRhAjiBEk7RpexAyJMYIYQYwgw4biRUwKkxHECGIESbvG9RZkWswdyf79i9gdzExDEGCKU54MAXJmphEIMMUpT4YAOTPTCASY4pQnQ4CcmWnEGgSMwzBkUyrLSVZzzsWyHI+vIr6GYdhZFrmgXIec87NlPeYCpmn6aK29WBa5lFwppf12u323rMdcwDiOOaXUu2B1Y6i1VkopddECenHTNL211vaWhUbn8nj6+2cy74ATqFrrms4C89l/4uQm4Fcn9PPgz46j1tprKeXTqwNdBfSix3HcbTabp9Zavxl1EYuXkVLqwOvxePwupRy84LuOIM+i15TbvQPWBMvjsyDAg6ogJwIEsDyWIsCDqiAnAgSwPJYiwIOqICcCBLA8liLAg6ogJwIEsDyWIsCDqiAnAgSwPJb+AIYML44PWikOAAAAAElFTkSuQmCC"
ExportIcon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAA3FJREFUeF7tnVFS2zAQhqVwgk4gkDeOAicBTlJ6ktCTkJs0b4EMmZ6gUUfTuk3d2L/t3fXKmZ9XWbvS92ml2GScGPjnSiC6ZmfyQAHOi4ACKMCZgHN6VgAFOBNwTs8KODcB2+332zA7PMSY7kKId87zCymF5+X1/Iv3OJryq1bA9n3/OcbwXNpkS5agJuBt9/Fawopvkl+qBBUB293HYwxxVdrKr4+nRAliAXnPjxeHb6XDr8ZXmgS5gEL3/bYFUZIEsYD33X6VQnicSgWUVgliAW+7fd5+bqcmII+3hErQEJDa4N8s5uIcfeS+7fat4yntYBbDQRMuXYB3JVDA75Lw2o4o4GhP8pBAAbVDYWwJFHDihB9TAgU0fMQaSwIFtHzGHUMCBYCbDGsJFNDhLs9SAgV0EGB5s0YBHQVYSaCAHgIsJFBATwHaEihggABNCRQwUICWBAoQCMhdpY/bKYAChARq3dE/iHSzsQL+40kBNSTSPVJ7xfaNh4RK53d2Z0BfwOh6CkCEjNspwBgwCk8BiJBxOwUYA0bhKQARMm6nAGPAKDwFIELG7RRgDBiFpwBEyLidAowBo/AUgAgZt1OAMWAUngIQIeN2CjAGjMJTACJk3E4BxoBReApAhIzbKcAYMApfvAA0gam3U4CzQQqgAGcCzulZARTgTMA5PSuAApwJOKefRAVYvjVL+t1LqT8KGPmFT3VhFEABuIi5BWFGTVeIv56eA1MABQwnAHryDOAZgBcXtyDMyPQMQOkl75fmfQCiC9ol8HNoChAIkMKnAGf4FDBQgMbKr1JzC+opQRM+K8AYfoqH+5hmr21pWAEdJfRd+Rn+8upqbX2n2XH4jZdZj0/lWdBQ+HnW0gmi/lIBqL+0QsUCJPCnLiCG8HK9mD8hSW3tIgFS+FMXoPFCV5GAPuVf7fn11YBioBJH/SWrE/VtmhPqd9w+WMDf34zEP13YNlAEsFQBKaSn5eLypQ/sU9cOFpCDdZGAVsk0BaT1zeLyXgo/9xcJqCTEix+rU78jieDn/vlRdttE0CGHBGpAOo6hse+rbEHHQX4dxv9K6AJfA84IAjYhpE1KcR0Os6/L5aeNxrirGOIKqAIdSxgLviYIr1hqAv6cCSEE7VXiBWeMvKoCxhjwueWgAGejFEABzgSc07MCKMCZgHP6n2fLBY5Bcu3KAAAAAElFTkSuQmCC"
EditIcon = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAAzJJREFUeF7t21FS2zAQxnGJnqATMPEbvQk5SZuTtD0JuUndm+QtNAPDCYg6TuIGhjReSbte2fvxBDOKbX7/yHZsxzv8qAp41bVj5Q4BlN8ECIAAygLKq8cMQABlAeXVYwYggLKA8uoxAxBAWUB59ZgBCKAs8Gb1mz/P39s/vQ/3zvm7/e/ONTsXftfV9UpiSzEDnHObzcud//T64Jy/v4C8Dq9Xi7r+vOYMYT7AZvv0zTv/QERdh+BW9e3sJ3F87zDTASLxO0zWCGYDJOKzRzAZIBP/FMHvlvXNTdO7n7kwwFwAJny2CKYCMOOzRDATQAj/FCHxFNVEAGH8Y4TQzKvrRezxYPIBhsE/sAcXlrGfmCcdYEj8Y4LoWTDZAMPj7+cAArQMOvj7ObCeV7MvMceByc0ARXwEUMZvL12vbqvZ0uQM0MY3fRZUAn7K/v94wydmwpQ3thB8F/xukXJhbtQH4Tj80ITgG+/dD+63UcoHsG4bRhsgFr+9TNDeenRXu6+cEXLwR7sLSsHv3nGcEXLxRxkgB58zAgf+6AJw4HNE4MIfVQBO/JwInPijCSCB30V43D796nke6N9JEzf+KAJMGb/4AFPHLzqABfxiA1jBLzKAJfziAljDLyqARfxiAljFLyKAZXz1ANbxVQMA/3CFQ+WGDPBP9+QGDwD89zdEBw0A/I93owcLAPzzjwIMEgD4/38OQzwA8C8/BCMaAPiX8UVPQ4Hfjy8WAPg0fJEAwKfjswcAfhw+awDgx+OzBQB+Gj5LAOCn42cHAH4eflYA4OfjJwcAPg9+UgDg8+EnBXjcPgfaJsR9bV/7KWXa/8Q/KvpiHC0A8KmpBAIAn4ovsguaVzNyVKu7nbeByFjdi/p2QdQAwD+IqgQA/mkODB4A+O+PEIMGAP7Hw/NgAYB//tyIPUDMKdi5sRJfBc3dJsnXFxXAGr7IWVDqu8UifjEBrOIXEcAyvnoA6/iqAYAvdCmCchAGfsalCAowxtAFoj8H0BeNkRQBBKAoCY5BAEFcyqIRgKIkOAYBBHEpi0YAipLgGAQQxKUsGgEoSoJjEEAQl7JoBKAoCY5BAEFcyqL/Av6z/n/vS6TuAAAAAElFTkSuQmCC"
def MakeOption(md_id, soup, option_class, span_text, form_action, form_class):
    ##製作按鈕
    outer_card_option = soup.new_tag('div', **{'class': 'card-more-options'})
    card_option = soup.new_tag('div', **{'class': 'tooltip'})
        
    option_img = soup.new_tag('img', **{'class': option_class, })
    option_img['onclick'] = "this.parentNode.querySelector('" + "." + form_class + "').submit()"
    card_option.append(option_img)

    option_span = soup.new_tag('span', **{'class':'tooltiptext'})
    option_span.string = span_text
    card_option.append(option_span)

    new_form = soup.new_tag('form', action= form_action, method="post", **{'class': form_class}, style="display: none;")
    new_textarea = soup.new_tag('textarea')
    new_textarea['name'] = 'filename'
    new_textarea['type'] = "text"
    new_textarea.string = md_id
    new_form.append(new_textarea)
    card_option.append(new_form)
    outer_card_option.append(card_option)
    return outer_card_option  


def AddElement(path):
    html_str = ''
    with open(path, 'rb') as file:
        encoding = chardet.detect(file.read())
    print("encoding = ", encoding['encoding'])
    with open(path, mode='r', encoding = encoding['encoding'], errors='ignore') as file:
        html_str = file.read()
    soup = BeautifulSoup(html_str, 'html.parser')
    container = soup.find('ul',  {'id':'card-box-ul'})
    datas = Database.GetAllHtml()
    for data in datas:
        #print("data", data)
        li = soup.new_tag('li', **{'class': 'list card'})

        options = soup.new_tag('div', **{'class': 'option-list'})
        ## 製作編輯按鈕
        export_option = MakeOption(data[0], soup, 'edit-img', "編輯", "./editmd", 'EditMd')
        options.append(export_option)

        ## 製作匯出按鈕
        export_option = MakeOption(data[0], soup, 'export-img', "匯出", "./exportmd", 'ExportMd')
        options.append(export_option)

        ##製作刪除按鈕
        card_option = MakeOption(data[0], soup, 'delete-img', "刪除", "./deletefile", 'DeleteFile')
        options.append(card_option)

        li.append(options)

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
    scriptContents = ""
    scriptContents += "const EditIcon = " + '"' + EditIcon + '";\n'
    scriptContents += "card_edit = document.querySelectorAll('.edit-img');\ncard_edit.forEach(img => img.src = EditIcon)\n"
    scriptContents += "const ExportIcon = " + '"' + ExportIcon + '";\n'
    scriptContents += "card_export = document.querySelectorAll('.export-img');\ncard_export.forEach(img => img.src = ExportIcon)\n"
    scriptContents += "const DeleteIcon = " + '"' + deleteIcon + '";\n'
    scriptContents += "card_imgs = document.querySelectorAll('.delete-img');\ncard_imgs.forEach(img => img.src = DeleteIcon)\n"
    script_tag.string = scriptContents
    soup.body.append(script_tag)
    return str(soup)


if __name__ == '__main__':
    AddElement(r'./templates/home.html')