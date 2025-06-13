from bs4 import BeautifulSoup
import Database
from MarkdownToHtml import ReadMd

def readHtml():
    root = "./templates/EditBoard.html"

    with open(root, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    return soup

def getMarkdownEditor(md_id):
    name, md = Database.GetMd(md_id)
    name = name.replace("\r", "")
    md = md.replace("\r", "") #sqlite在存入text時會將\n變成\r
    soup = readHtml()
    namearea = soup.find("input", {"id":"markdown-name"})
    namearea['value'] = name
    id_area = soup.find("input", {"id":"markdown-id"})
    id_area['value'] = md_id
    textarea = soup.find("textarea", {"id":"markdown-edit-area"})
    textarea.string = md
    return soup

if __name__ == '__main__':
    #md = ReadMd("C:/Users/apple/Downloads/Linux作業系統 Project2/Linux作業系統 Project2.md")
    #print([md])
    soup = getMarkdownEditor("20241220132357")
    #print(soup.find("textarea"))