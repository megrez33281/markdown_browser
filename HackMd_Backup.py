import requests
from bs4 import BeautifulSoup
import os
import re

def download_image(image_url, save_path):
    try:
        # 發送GET請求來下載圖片
        response = requests.get(image_url)
        
        # 如果請求成功，則下載圖片
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return 0
        else:
            print(f"無法下載圖片，狀態碼: {response.status_code}")
            print("重新下載中......")
            for i in range(3):
                # 發送GET請求來下載圖片
                response = requests.get(image_url)
                # 如果請求成功，則下載圖片
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    return 0
            return -1
    
    except Exception as e:
        print(f"發生錯誤: {e}")

def getMarkDown(link):
    if link.find("?view") != -1:
        link = link.replace("?view", "?edit")
    elif link.find("?both") != -1:
         link = link.replace("?both", "?edit")
    elif link.find("?edit") == -1:
        link = link + "?edit"

    url = requests.get(link)
    soup = BeautifulSoup(url.content, "html.parser")
    linker = soup.find("div", {'id': 'doc'})
    title = soup.find("title").getText().replace(" - HackMD", "")
    if linker:
        MarkDownContent = linker.getText()
        #print(title)
        return title, MarkDownContent
    else:
        print("找不到MarkDown內容")
    
    return "", ""

def MakeForder(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        return
    return


def getImageLink(markDown):
    lines = markDown.split("\n")
    links = []
    for line in lines:
        if re.match(r'.*!\[.*\]\(.*\).*', line):
            link = line.split("](")[1].split(")")[0]
            links.append(link)
    return links

def MakeMarkDown(link, path="./"):
    MarkDownForderName, markDown = getMarkDown(link)
    if MarkDownForderName == "" and markDown == "":
        #爬蟲沒有抓到內容
        return ""
    MakeForder(path + "/" + MarkDownForderName)
    imagePath = path + "/" +MarkDownForderName + "/image"
    MakeForder(imagePath)
    image_links = getImageLink(markDown)
    for i in range(0, len(image_links)):
        format = image_links[i].split(".")[-1]
        save_path =  imagePath + "/" + str(i) + "." + format
        result = download_image(image_links[i], save_path)
        if result == 0:
            markDown = markDown.replace(image_links[i], "image/" + str(i) + "." + format)
    
    FullPath = path + "/" + MarkDownForderName + "/" + MarkDownForderName + ".md"
    outputFile = open(path + "/" + MarkDownForderName + "/" + MarkDownForderName + ".md", mode='w', encoding='utf-8')
    print(markDown, file=outputFile)
    outputFile.close()
    return FullPath

if __name__ == '__main__':

    links = input("請輸入HackMD網址，並確保該HackMD允許任何人訪問：\n網址：")
    MakeMarkDown(links)



