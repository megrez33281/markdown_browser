import sqlite3

name = "MarkdownData"

def InitialDatabase():
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markdowns (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            html TEXT NOT NULL,
            md TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pictures (
            id TEXT NOT NULL,
            name TEXT NOT NULL,
            pic TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    return 0

def ExecuteCommand(command):
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    cur.execute(command)
    conn.commit()
    conn.close()
    

def QueryCommand(command):
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    print(command)
    cur.execute(command)
    datas = cur.fetchall()
    #print(datas)
    conn.commit()
    conn.close()
    return datas

def MakeString(a_str):
    return "'" + str(a_str) + "'"

def InsertPictures(md_id, pic_base64:dict):
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    for key in pic_base64.keys():
        cur.execute('INSERT INTO pictures (id, name, pic) VALUES (?, ?, ?)', (str(md_id), key, pic_base64.get(key)))
    conn.commit()
    conn.close()
    return 0

def InsertMarkdown(md_id, html_name, html, md):
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    cur.execute('INSERT INTO markdowns (id, name, html, md) VALUES (?, ?, ?, ?)', (str(md_id), html_name, html, md))
    conn.commit()
    conn.close()

def UpdateMarkdown(md_id, html_name, html, md):
    conn = sqlite3.connect('./' + name.replace('.db', '') + '.db')
    cur = conn.cursor()
    # 更新資料
    cur.execute('''
        UPDATE markdowns 
        SET name = ?, html = ?, md = ? 
        WHERE id = ?
    ''', (html_name, html, md, str(md_id)))
    conn.commit()
    conn.close()

def UpdatePictures(md_id, pic_base64: dict):
    conn = sqlite3.connect('./' + name.replace('.db', '') + '.db')
    cur = conn.cursor()
    
    # 更新圖片資料
    for key, value in pic_base64.items():
        cur.execute('''
            UPDATE pictures 
            SET pic = ? 
            WHERE id = ? AND name = ?
        ''', (value, str(md_id), key))
    
    conn.commit()
    conn.close()
    return 0

def GetHtml(md_id):
    command = 'select name, html from markdowns where id = ' + MakeString(md_id)
    #print(command)
    return QueryCommand(command)[0]

def GetPictures(md_id):
    command = 'select name, pic from pictures where id = ' + MakeString(md_id)
    #print(command)
    return QueryCommand(command)

def GetMd(md_id):
    command = 'select name, md from markdowns where id = ' + MakeString(md_id)
    #print(command)
    return QueryCommand(command)[0]

def GetAllHtml():
    command = 'select id, name from markdowns'
    datas = QueryCommand(command)
    return datas

def DeleteHtml(md_id):
    command = 'delete from markdowns where id = ' + MakeString(md_id)
    ExecuteCommand(command)
    command = 'delete from pictures where id = ' + MakeString(md_id)
    ExecuteCommand(command)

def clear():
    ExecuteCommand('delete from markdowns')

if __name__ == '__main__':
    clear()
