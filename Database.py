import sqlite3

name = "MarkdownData"

def InitialDatabase():
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cursor=conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markdowns (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            html TEXT NOT NULL
        )
    ''')

def ExecuteCommand(command):
    assert isinstance(command, str) and len(command) > 0
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    cur.execute(command)
    conn.commit()
    conn.close()


def QueryCommand(command):
    assert isinstance(command, str) and len(command) > 0
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    print(command)
    cur.execute(command)
    datas = cur.fetchall()
    assert len(datas) > 0
    #print(datas)
    conn.commit()
    conn.close()
    return datas

def MakeString(a_str):
    if not a_str:
        raise ValueError('輸入的a_str不存在')
    return "'" + str(a_str) + "'"

def InsertMarkdown(md_id, html_name, html):
    assert isinstance(html_name, str)
    assert isinstance(html, str)
    conn=sqlite3.connect ('./' + name.replace('.db', '') +  '.db')
    cur=conn.cursor()
    cur.execute('INSERT INTO markdowns (id, name, html) VALUES (?, ?, ?)', (str(md_id), html_name, html))
    conn.commit()
    conn.close()

def GetHtml(md_id):
    command = 'select name, html from markdowns where id = ' + MakeString(md_id)
    query_html = QueryCommand(command)
    if len(query_html) == 1:
        return query_html[0]
    #print(command)
    return ['', '']

def GetAllHtml():
    command = 'select id, name from markdowns'
    datas = QueryCommand(command)
    return datas

def DeleteHtml(md_id):
    command = 'delete from markdowns where id = ' + MakeString(md_id)
    ExecuteCommand(command)

def clear():
    ExecuteCommand('delete from markdowns')

if __name__ == '__main__':
    clear()
