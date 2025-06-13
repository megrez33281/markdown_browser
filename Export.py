import Database
import os
import base64

def MakeForder(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        return
    return

def Base64ToPic(path, name, pic_base64):
    
    header, base64_body = pic_base64.split(",", 1)
    image_data = base64.b64decode(base64_body)
    mime_type = header.split(";")[0].split(":")[1]
    format = mime_type.split("/")[-1]
    file_path = path + "/" + name + "." + format
    with open(file_path, "wb") as file:
        file.write(image_data)

def ExportMarkDown(md_id, path="./"):
    # 將md檔案從資料庫匯出
    name, md = Database.GetMd(md_id)
    md = md.replace("\r", "") #sqlite在存入text時會將\n變成\r
    if path[-1] != "/":
        path += "/"
    file_root = path + name
    print(file_root)
    MakeForder(file_root)
    image_root = file_root + "/" + "img"
    MakeForder(image_root)
    md_path = file_root + "/" + name + ".md"
    with open(md_path, mode='w', encoding='utf-8') as file:
        file.write(md) 
    pics = Database.GetPictures(md_id)
    for pic in pics:
        Base64ToPic(image_root, pic[0], pic[1])
    #print(pics[0][0])
    return 0



if __name__ == '__main__':
    ExportMarkDown("20241205231518")
    
